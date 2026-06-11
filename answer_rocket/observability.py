"""
Observability client for AnswerRocket.

Fetches finished chat traces via the GraphQL observabilityTraces query and
assembles them into OTLP/JSON (top-level {"resourceSpans":[...]}) so callers
can forward batches directly to any OTel collector's /v1/traces endpoint.

Usage patterns:

  # Single page
  batch = client.observability.get_traces(since="2026-05-01T00:00:00Z")

  # All pages from a cursor
  for batch in client.observability.iter_traces(since="2026-05-01T00:00:00Z"):
      forward_to_collector(batch)

  # Continuous polling loop
  for batch in client.observability.poll_traces(since="2026-05-01T00:00:00Z"):
      forward_to_collector(batch)

Attribute coverage vs Unilever R1-R18 spec
-------------------------------------------
R1  Unique Run ID            ar.run_id / ar.id.answer.canonical / traceId
R2  Standard Event Schema    OTLP/JSON, GenAI semconv
R3  Immutable Trace Storage  collector-side concern; NOT emitted by SDK
    (ar.trace.content_hash was claimed in meeting_prep.md but was never
    implemented here or in the Max server — that claim was incorrect)
R4  Historical Data Retention collector-side concern; NOT emitted by SDK
    (ar.retention.policy was claimed in meeting_prep.md but was never
    implemented here or in the Max server — that claim was incorrect)
R5  Version Tagging          service.version / ar.prompt.version /
                             ar.prompt.version.full / ar.model.label /
                             per-call: gen_ai.request.model,
                             ar.prompt.system_template_sha256
R6  Version Filtering        collector-side concern; NOT emitted by SDK
    (ar.filter.dimensions was claimed in meeting_prep.md but was never
    implemented here or in the Max server — that claim was incorrect)
R7  Plan Generation Logging  gen_ai.tool.call.name/arguments,
                             ar.llm.available_tools,
                             ar.llm.next_function_options, ar.stage,
                             ar.plan.function_selected/invoked/context_summary
R8  Phase Timing             ~23 phase.* spans with ar.phase.depth/count
R9  UI Interaction           existing feedback path (unchanged)
R10 Step Duration            ar.phase.duration_seconds /
                             ar.phase.own_duration_seconds /
                             ar.phase.cpu_seconds
R11 E2E Latency              ar.latency.pipeline_seconds + span duration
R12 Output Evaluation        evaluation sibling span (ar.eval.*, gen_ai.evaluation.*,
                             ar.test_case.*) + skill span ar.skill.output.*
R13 Confidence Capture       OUT OF SCOPE — not emitted
R14 Cost Metadata            ar.cost.estimated_usd / per-call ar.cost.estimate_usd /
                             gen_ai.usage.input_tokens / gen_ai.usage.output_tokens
R15 Feedback Capture         existing feedback path (unchanged)
R16 ID Disambiguation        ar.id.answer.canonical / ar.id.thread / ar.id.user /
                             ar.id.skill.run / ar.id.skill.answer
R17 Tool Call Decision       same envelope as R7 on every LLM span
R18 Agent Suggestions        ar.answer.suggestions / ar.answer.suggestion_questions /
                             ar.answer.suggestion_count
"""

from __future__ import annotations

import hashlib
import logging
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Generator, Iterator

from answer_rocket.client_config import ClientConfig
from answer_rocket.graphql.client import GraphQlClient

_logger = logging.getLogger("answer_rocket.observability")

DEFAULT_LIMIT = 100
DEFAULT_POLL_INTERVAL_SECONDS = 60.0

_OBSERVABILITY_TRACES_QUERY = """
query ObservabilityTraces($since: String!, $limit: Int) {
  observabilityTraces(since: $since, limit: $limit) {
    count
    hasMore
    nextCursor
    entries {
      id
      threadId
      userId
      question { nl }
      answer {
        answeredAt
        hasFinished
        message
        copilotSkillId
        copilotName
        generalDiagnostics
        chatPipelineProfile
        suggestions
        reportResults {
          reportName
          title
          finalMessage
          preview
          contentBlocks { id type }
          gzippedDataframesAndMetadata
        }
      }
    }
  }
}
"""


@dataclass
class TracesBatch:
    """One page of OTLP/JSON traces."""
    success: bool = False
    error: str | None = None
    count: int = 0
    has_more: bool = False
    next_cursor: str | None = None
    traces: list[dict] = field(default_factory=list)


class Observability:
    def __init__(self, config: ClientConfig, gql_client: GraphQlClient):
        self._config = config
        self._gql_client = gql_client

    def get_traces(
        self,
        since: str | datetime,
        limit: int = DEFAULT_LIMIT,
        tenant: str | None = None,
    ) -> TracesBatch:
        since_str = _to_iso(since)
        effective_tenant = tenant or self._config.tenant or "unknown"
        try:
            data = self._gql_client.query_raw(
                _OBSERVABILITY_TRACES_QUERY,
                variables={"since": since_str, "limit": limit},
            )
        except Exception as exc:
            return TracesBatch(success=False, error=str(exc))

        result = (data or {}).get("observabilityTraces") or {}
        entries = result.get("entries") or []
        traces = [t for e in entries for t in [_build_otlp(e, effective_tenant)] if t is not None]

        return TracesBatch(
            success=True,
            count=result.get("count", 0),
            has_more=result.get("hasMore", False),
            next_cursor=result.get("nextCursor"),
            traces=traces,
        )

    def iter_traces(
        self,
        since: str | datetime,
        limit: int = DEFAULT_LIMIT,
        tenant: str | None = None,
    ) -> Iterator[list[dict]]:
        cursor: str | datetime = since
        while True:
            result = self.get_traces(cursor, limit=limit, tenant=tenant)
            if not result.success:
                _logger.error("iter_traces page error: %s", result.error)
                return
            if result.traces:
                yield result.traces
            if not result.has_more or not result.next_cursor:
                return
            cursor = result.next_cursor

    def poll_traces(
        self,
        since: str | datetime,
        on_batch: Callable[[list[dict]], None] | None = None,
        limit: int = DEFAULT_LIMIT,
        poll_interval_seconds: float = DEFAULT_POLL_INTERVAL_SECONDS,
        max_iterations: int | None = None,
        tenant: str | None = None,
    ) -> Generator[list[dict], None, None]:
        cursor: str | datetime = since
        iterations = 0
        while max_iterations is None or iterations < max_iterations:
            result = self.get_traces(cursor, limit=limit, tenant=tenant)
            if not result.success:
                _logger.warning("poll_traces error (will retry): %s", result.error)
                time.sleep(poll_interval_seconds)
                iterations += 1
                continue
            if result.traces:
                if on_batch is not None:
                    on_batch(result.traces)
                yield result.traces
            if result.next_cursor:
                cursor = result.next_cursor
            iterations += 1
            if not result.has_more:
                time.sleep(poll_interval_seconds)


# ---------------------------------------------------------------------------
# OTLP assembly
# ---------------------------------------------------------------------------

def _build_otlp(entry: dict, tenant: str) -> dict | None:
    """Assemble one OTLP/JSON ExportTraceServiceRequest from a MaxChatEntry dict."""
    try:
        answer = entry.get("answer") or {}
        if not answer.get("hasFinished"):
            return None

        run_id = str(entry.get("id") or "")
        thread_id = str(entry.get("threadId") or "") or None
        user_id = str(entry.get("userId") or "") or None
        gd = answer.get("generalDiagnostics") or {}
        profile = answer.get("chatPipelineProfile") or []
        report_results = _normalize_report_results(answer.get("reportResults") or [])
        first_report = report_results[0] if report_results else {}

        nodes = _build_phase_tree(profile)
        if not nodes:
            return None

        pipeline_seconds = nodes[0]["duration_seconds"]
        answered_at = answer.get("answeredAt")
        try:
            dt = datetime.fromisoformat(str(answered_at).replace("Z", "+00:00"))
            end_ns = int(dt.timestamp() * 1e9)
        except Exception:
            end_ns = time.time_ns()
        root_start_ns = end_ns - int(pipeline_seconds * 1e9)

        trace_id = hashlib.md5(run_id.encode()).hexdigest()

        def sid(*parts: str) -> str:
            return hashlib.md5("|".join(parts).encode()).hexdigest()[:16]

        def make_span(name, span_id, parent_id, kind, s_ns, e_ns, attrs, events=None):
            s = {
                "traceId": trace_id, "spanId": span_id, "name": name, "kind": kind,
                "startTimeUnixNano": str(s_ns), "endTimeUnixNano": str(e_ns),
                "attributes": _to_otlp_attrs(attrs), "events": events or [],
                "status": {"code": "STATUS_CODE_OK"},
            }
            if parent_id:
                s["parentSpanId"] = parent_id
            return s

        # ------------------------------------------------------------------ #
        # Suggestions (R18) — answer.suggestions is a JSON-encoded list       #
        # ------------------------------------------------------------------ #
        raw_suggestions = answer.get("suggestions")
        suggestion_labels: list[str] = []
        suggestion_questions: list[str] = []
        if raw_suggestions:
            try:
                import json as _json
                parsed = _json.loads(raw_suggestions) if isinstance(raw_suggestions, str) else raw_suggestions
                if isinstance(parsed, list):
                    for s in parsed:
                        if isinstance(s, dict):
                            lbl = s.get("label") or s.get("title") or s.get("name") or ""
                            q = s.get("question") or s.get("nl") or ""
                        else:
                            lbl, q = str(s), ""
                        if lbl:
                            suggestion_labels.append(lbl)
                        if q:
                            suggestion_questions.append(q)
            except Exception:
                pass

        # ------------------------------------------------------------------ #
        # Root span: chat.pipeline (R1, R5, R7, R11, R14, R16, R18)          #
        # ------------------------------------------------------------------ #
        # Derive ar.prompt.version from the first LLM call's system-template  #
        # sha256 — that is the hash of the system prompt used for function     #
        # selection, which is the canonical "prompt version" for the answer.   #
        first_call_sha: str | None = None
        for call in gd.get("Chat Model Call Record") or []:
            if isinstance(call, dict):
                sha = (call.get("response") or {}).get("system_template_sha256") or \
                      call.get("systemTemplateSha256")
                if sha:
                    first_call_sha = str(sha)
                    break

        root_sid = sid(run_id, "root")
        root_attrs = _drop_none({
            # R1 / R16 — canonical ID + disambiguation IDs
            "ar.run_id": run_id,
            "ar.id.answer.canonical": run_id,
            "ar.id.thread": thread_id,
            "ar.id.user": user_id,
            "ar.id.skill.run": first_report.get("skill_run_id"),
            "ar.id.skill.answer": first_report.get("skill_answer_id"),
            # identity
            "ar.tenant": tenant,
            "ar.copilot.skill_id": str(answer.get("copilotSkillId") or "") or None,
            "ar.copilot.name": str(answer.get("copilotName") or "") or None,
            # question / answer text
            "ar.question.text": (entry.get("question") or {}).get("nl"),
            "ar.answer.text": (answer.get("message") or "")[:1000] or None,
            # OTel resource / semconv
            "deployment.environment": tenant,
            "service.name": "answerrocket-copilot",
            "service.namespace": "answerrocket",
            # R5 — version tagging
            "service.version": gd.get("serviceVersion") or gd.get("service_version") or "unknown",
            "ar.prompt.version": first_call_sha[:16] if first_call_sha else None,
            "ar.prompt.version.full": first_call_sha,
            "ar.model.label": gd.get("LLM Model Used"),
            "gen_ai.conversation.id": thread_id,
            "gen_ai.agent.name": str(answer.get("copilotName") or "") or None,
            # R7 — plan
            "ar.plan.function_selected": gd.get("Function Selected By Model"),
            "ar.plan.function_invoked": gd.get("Function Invoked") or gd.get("functionInvoked"),
            "ar.plan.context_summary": gd.get("Context Summary") or gd.get("contextSummary"),
            # R14 — cost / tokens
            "ar.cost.estimated_usd": _coerce_cost(gd.get("Estimated LLM cost USD")),
            "ar.tokens.budget_max": _safe_int(gd.get("Maximum Token Count for Model")),
            "ar.tokens.budget_initial": _safe_int(gd.get("Initial Token Budget without History")),
            "ar.tokens.budget_with_history": _safe_int(
                gd.get("Token Budget with History") or gd.get("tokenBudgetWithHistory")
            ),
            "ar.tokens.functions": _safe_int(
                gd.get("Function Token Count") or gd.get("functionTokenCount")
            ),
            # R11 — latency
            "ar.latency.pipeline_seconds": _safe_float(profile[0].get("time")) if profile else None,
            # R18 — suggestions
            "ar.answer.suggestions": suggestion_labels or None,
            "ar.answer.suggestion_questions": suggestion_questions or None,
            "ar.answer.suggestion_count": len(suggestion_labels) if suggestion_labels else None,
        })

        spans = [make_span("chat.pipeline", root_sid, None, "SPAN_KIND_SERVER", root_start_ns, end_ns, root_attrs)]

        # ------------------------------------------------------------------ #
        # Phase spans (R8 / R10)                                              #
        # ------------------------------------------------------------------ #
        stack_to_id: dict[str, str] = {}
        stack_to_timing: dict[str, tuple[int, int]] = {}
        cursor_d: dict[str, int] = defaultdict(int)

        for i, n in enumerate(nodes):
            sk = " > ".join(n["stack"])
            pk = " > ".join(n["stack"][:-1]) if len(n["stack"]) > 1 else ""
            if pk == "":
                s_ns = root_start_ns
            else:
                p_start = stack_to_timing.get(pk, (root_start_ns, root_start_ns + 1))[0]
                p_own_ns = int(_lookup_own(nodes, pk) * 1e9)
                s_ns = p_start + p_own_ns // 2 + cursor_d[pk]
                cursor_d[pk] += int(n["duration_seconds"] * 1e9)
            e_ns = s_ns + max(int(n["duration_seconds"] * 1e9), 1)
            stack_to_timing[sk] = (s_ns, e_ns)
            phase_sid = sid(run_id, "phase", str(i), n["name"])
            stack_to_id[sk] = phase_sid
            parent_sid = stack_to_id.get(pk) or root_sid
            attrs = _drop_none({
                "ar.run_id": run_id,
                "ar.phase.name": n["name"],
                # R10 — duration fields
                "ar.phase.duration_seconds": n["duration_seconds"],
                "ar.phase.own_duration_seconds": n.get("own_seconds"),
                "ar.phase.cpu_seconds": n.get("cpu_seconds"),
                # R8 — structural fields
                "ar.phase.depth": n.get("depth"),
                "ar.phase.count": n.get("count"),
            })
            spans.append(make_span(
                f"phase.{n['name'].lower().replace(' ', '_')}",
                phase_sid, parent_sid, "SPAN_KIND_INTERNAL", s_ns, e_ns, attrs,
            ))

        # ------------------------------------------------------------------ #
        # LLM call spans (R7 / R17)                                           #
        # ------------------------------------------------------------------ #
        _STAGE_MAP = {
            "Function Selection": "Chat Pipeline > Run Chat > Agent Run > LLM Function Selection or Response",
            "Parameter Selection": "Chat Pipeline > Run Chat > Agent Run > LLM Parameter Extraction Call",
        }
        by_stage: dict[str, list] = defaultdict(list)
        for call in gd.get("Chat Model Call Record") or []:
            if isinstance(call, dict):
                by_stage[call.get("stage") or "Unknown"].append(call)

        for stage, calls in by_stage.items():
            pk = _STAGE_MAP.get(stage)
            p_timing = stack_to_timing.get(pk) if pk else None
            p_sid = stack_to_id.get(pk) if pk else None
            if p_timing:
                p_start, p_end = p_timing
                slot = max((p_end - p_start) // max(len(calls), 1), 1)
            else:
                slot, p_start, p_sid = 1_000_000_000, root_start_ns, p_sid or root_sid
            for j, call in enumerate(calls):
                resp = call.get("response") or {}
                usage = resp.get("usage") or {}
                tool_call = call.get("toolCall") or call.get("tool_call") or {}
                finish_reasons = resp.get("finish_reasons") or resp.get("finishReasons")
                attrs = _drop_none({
                    "ar.run_id": run_id,
                    "ar.stage": stage,
                    # R2 — GenAI semconv
                    "gen_ai.system": "azure.ai.openai",
                    "gen_ai.provider.name": "azure.ai.openai",
                    "gen_ai.operation.name": "chat",
                    "gen_ai.request.model": resp.get("model"),
                    "gen_ai.response.id": resp.get("id"),
                    "gen_ai.response.model": resp.get("model"),
                    # R7 — tool call decision
                    "gen_ai.tool.call.name": tool_call.get("name") or call.get("functionName") or call.get("function_name"),
                    "gen_ai.tool.call.arguments": _json_str(
                        tool_call.get("arguments") or call.get("functionArgs") or call.get("function_args")
                    ),
                    "gen_ai.response.finish_reasons": finish_reasons if isinstance(finish_reasons, list) else (
                        [finish_reasons] if finish_reasons else None
                    ),
                    "ar.llm.available_tools": call.get("availableTools") or call.get("available_tools"),
                    "ar.llm.next_function_options": _json_str(
                        call.get("nextFunctionOptions") or call.get("next_function_options")
                    ),
                    # R5 — per-call prompt version
                    "ar.prompt.system_template_sha256": resp.get("system_template_sha256") or call.get("systemTemplateSha256"),
                    "ar.prompt.system_template_chars": _safe_int(
                        resp.get("system_template_chars") or call.get("systemTemplateChars")
                    ),
                    # R14 — cost / tokens
                    "gen_ai.usage.input_tokens": _safe_int(usage.get("prompt_tokens")),
                    "gen_ai.usage.output_tokens": _safe_int(usage.get("completion_tokens")),
                    "ar.cost.estimate_usd": _coerce_cost(usage.get("cost_estimate_usd")),
                    "ar.tokens.total": _safe_int(usage.get("total_tokens")),
                    "ar.tokens.embedding_tokens": _safe_int(usage.get("embedding_tokens")),
                })
                s_ns = p_start + j * slot
                e_ns = s_ns + slot
                created = resp.get("created")
                if isinstance(created, (int, float)) and created > 0:
                    e_ns = int(created) * 1_000_000_000
                    s_ns = e_ns - slot
                model = resp.get("model") or "llm"
                spans.append(make_span(
                    f"chat {model}", sid(run_id, "llm", stage, str(j)),
                    p_sid or root_sid, "SPAN_KIND_CLIENT", s_ns, e_ns, attrs,
                ))

        # ------------------------------------------------------------------ #
        # Skill + narrative spans (R12, R16)                                  #
        # ------------------------------------------------------------------ #
        if first_report:
            skill_name = first_report.get("report_name") or "unknown"
            parent_pk = f"Chat Pipeline > Run Chat > Agent Run > Running {skill_name}"
            p_sid = stack_to_id.get(parent_pk)
            if p_sid is None:
                for sk, phase_sid in stack_to_id.items():
                    if "Agent Run > Running " in sk:
                        p_sid = phase_sid
                        parent_pk = sk
                        break
            if p_sid:
                sk_start, sk_end = stack_to_timing.get(parent_pk, (root_start_ns, end_ns))
                skill_sid = sid(run_id, "skill")

                # Build skill params sub-attributes from the stored params dict
                skill_params: dict = first_report.get("skill_params") or {}
                skill_param_attrs: dict = {}
                if isinstance(skill_params, dict):
                    for pkey, pval in skill_params.items():
                        attr_key = f"ar.skill.params.{pkey}"
                        if isinstance(pval, list):
                            skill_param_attrs[attr_key] = [str(v) for v in pval]
                        elif pval is not None:
                            skill_param_attrs[attr_key] = str(pval)

                skill_attrs = _drop_none({
                    "ar.run_id": run_id,
                    # R16 — skill execution identity
                    "ar.skill.run_id": first_report.get("skill_run_id"),
                    "ar.skill.answer_id": first_report.get("skill_answer_id"),
                    # skill identity
                    "ar.skill.name": skill_name,
                    "ar.skill.title": first_report.get("title"),
                    "ar.skill.status": first_report.get("skill_status"),
                    "ar.skill.function": first_report.get("skill_function"),
                    "ar.skill.preview_url": first_report.get("skill_preview_url"),
                    # R12 — output payload
                    "ar.skill.output.dataset_name": first_report.get("output_dataset_name"),
                    "ar.skill.output.row_count": first_report.get("output_row_count"),
                    "ar.skill.output.column_names": first_report.get("output_column_names"),
                    "ar.skill.output.dimensions": first_report.get("output_dimensions"),
                    "ar.skill.output.measures": first_report.get("output_measures"),
                    "ar.skill.output.filters": first_report.get("output_filters"),
                    "ar.skill.output.df_csv_sha256": first_report.get("output_df_csv_sha256"),
                    # ar.skill.output.df_csv only when the full CSV is available
                    "ar.skill.output.df_csv": first_report.get("output_df_csv"),
                })
                skill_attrs.update(skill_param_attrs)

                spans.append(make_span(
                    f"skill.{skill_name.lower().replace(' ', '_')}", skill_sid,
                    p_sid, "SPAN_KIND_INTERNAL", sk_start, sk_end, skill_attrs,
                ))

                narr_input = first_report.get("final_message") or ""
                narr_output = answer.get("message") or ""
                narr_start = max(sk_start, sk_end - 1_000_000_000)
                narr_attrs = _drop_none({
                    "ar.run_id": run_id,
                    "ar.narrative.purpose": "summarize_skill_output_for_user",
                    "ar.narrative.input": narr_input,
                    "ar.narrative.output": narr_output,
                    "ar.narrative.input_chars": len(narr_input) if narr_input else None,
                    "ar.narrative.output_chars": len(narr_output) if narr_output else None,
                    "gen_ai.operation.name": "chat",
                    "gen_ai.system": "azure.ai.openai",
                    "gen_ai.provider.name": "azure.ai.openai",
                })
                spans.append(make_span(
                    "skill.narrative", sid(run_id, "narrative"), skill_sid,
                    "SPAN_KIND_CLIENT", narr_start, sk_end, narr_attrs,
                ))

        # ------------------------------------------------------------------ #
        # Evaluation span (R12) — sibling of chat.pipeline under root         #
        # ------------------------------------------------------------------ #
        # The SDK assembles a deterministic structural verdict from            #
        # generalDiagnostics when a gold test_case is present.  Downstream     #
        # (UL Eval Kit) adds LLM-judged gen_ai.evaluation.* after the fact.   #
        eval_data = gd.get("evalResult") or gd.get("eval_result") or {}
        if eval_data:
            test_case = eval_data.get("testCase") or eval_data.get("test_case") or {}
            eval_sid = sid(run_id, "eval")
            eval_attrs = _drop_none({
                "ar.run_id": run_id,
                "ar.eval.applicable": eval_data.get("applicable"),
                "ar.test_case.query": test_case.get("query"),
                "ar.test_case.expected_report_name": test_case.get("expectedReportName") or test_case.get("expected_report_name"),
                "ar.test_case.expected_parameters": _json_str(
                    test_case.get("expectedParameters") or test_case.get("expected_parameters")
                ),
                "ar.eval.actual_report_name": eval_data.get("actualReportName") or eval_data.get("actual_report_name"),
                "ar.eval.actual_parameters": _json_str(
                    eval_data.get("actualParameters") or eval_data.get("actual_parameters")
                ),
                "ar.eval.structural.report_match": eval_data.get("reportMatch") or eval_data.get("report_match"),
                "ar.eval.structural.params_match": eval_data.get("paramsMatch") or eval_data.get("params_match"),
                "ar.eval.structural.passed": eval_data.get("structuralPassed") or eval_data.get("structural_passed"),
                "gen_ai.evaluation.passed": eval_data.get("structuralPassed") or eval_data.get("structural_passed"),
                "gen_ai.evaluation.score.label": (
                    "pass" if (eval_data.get("structuralPassed") or eval_data.get("structural_passed")) is True
                    else "fail" if (eval_data.get("structuralPassed") or eval_data.get("structural_passed")) is False
                    else None
                ),
                "gen_ai.evaluation.name": eval_data.get("evalName") or "ar_structural_eval",
                "ar.eval.status": eval_data.get("status"),
                "ar.eval.skill_output_ref": "span:skill.<name>/attr:ar.skill.output.df_csv_sha256",
                "ar.eval.narrative_ref": "span:skill.narrative/attr:ar.narrative.output",
                "ar.eval.note": "Deterministic structural check vs gold test_case. LLM-judged correctness handed to Eval Kit.",
            })
            eval_start = end_ns
            eval_end = end_ns + 500_000  # 0.5 ms — nominal zero-cost bookkeeping span
            spans.append(make_span(
                "evaluation", eval_sid, root_sid,
                "SPAN_KIND_INTERNAL", eval_start, eval_end, eval_attrs,
            ))

        return {
            "resourceSpans": [{
                "resource": {"attributes": _to_otlp_attrs({
                    "service.name": "answerrocket-copilot",
                    "service.namespace": "answerrocket",
                    "deployment.environment": tenant,
                })},
                "scopeSpans": [{"scope": {"name": "answerrocket.copilot", "version": "0.1.0"}, "spans": spans}],
            }]
        }
    except Exception:
        _logger.exception("Failed to build OTLP trace for entry %s", entry.get("id"))
        return None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _normalize_report_results(results: list) -> list:
    out = []
    for r in results:
        if not isinstance(r, dict):
            continue
        # Attempt to extract skill execution IDs and output metadata from the
        # gzipped dataframes payload.  The payload is a JSON object after
        # decompression; we fall back gracefully if it is absent or malformed.
        gz = r.get("gzippedDataframesAndMetadata")
        skill_meta: dict = {}
        if gz:
            try:
                import base64
                import gzip
                raw = base64.b64decode(gz)
                payload = __import__("json").loads(gzip.decompress(raw).decode())
                skill_meta = payload if isinstance(payload, dict) else {}
            except Exception:
                pass
        out.append({
            "report_name": r.get("reportName"),
            "title": r.get("title"),
            "final_message": r.get("finalMessage"),
            "preview": r.get("preview"),
            "content_blocks": [
                {"id": cb.get("id"), "type": cb.get("type")}
                for cb in (r.get("contentBlocks") or [])
                if isinstance(cb, dict)
            ],
            # Skill execution identity — carried on skill.<name> span (R16)
            "skill_run_id": skill_meta.get("skillRunId"),
            "skill_answer_id": skill_meta.get("skillAnswerId"),
            # Output payload metadata — carried on skill.<name> span (R12)
            "output_row_count": skill_meta.get("rowCount"),
            "output_column_names": skill_meta.get("columnNames"),
            "output_dimensions": skill_meta.get("dimensions"),
            "output_measures": skill_meta.get("measures"),
            "output_filters": skill_meta.get("filters"),
            "output_df_csv_sha256": skill_meta.get("dfCsvSha256"),
            "output_df_csv": skill_meta.get("dfCsv"),
            "output_dataset_name": skill_meta.get("datasetName"),
            "skill_status": skill_meta.get("status"),
            "skill_function": skill_meta.get("functionName"),
            "skill_params": skill_meta.get("params"),
            "skill_preview_url": skill_meta.get("previewUrl"),
        })
    return out


def _build_phase_tree(profile: list) -> list[dict]:
    out = []
    for p in profile:
        if isinstance(p, dict):
            out.append({
                "name": p.get("name") or "phase",
                "stack": list(p.get("stack") or []),
                "duration_seconds": float(p.get("time") or 0),
                "own_seconds": float(p.get("own_time") or 0),
                # R8/R10: depth, count, and CPU seconds per phase span
                "depth": _safe_int(p.get("depth")),
                "count": _safe_int(p.get("count")),
                "cpu_seconds": _safe_float(p.get("cpuTime") or p.get("cpu_time")),
            })
    return out


def _lookup_own(nodes: list, stack_key: str) -> float:
    for n in nodes:
        if " > ".join(n["stack"]) == stack_key:
            return n.get("own_seconds") or 0.0
    return 0.0


def _to_otlp_attrs(d: dict) -> list:
    out = []
    for k, v in (d or {}).items():
        if v is None or v == "":
            continue
        if isinstance(v, bool):
            out.append({"key": k, "value": {"boolValue": v}})
        elif isinstance(v, int):
            out.append({"key": k, "value": {"intValue": str(v)}})
        elif isinstance(v, float):
            out.append({"key": k, "value": {"doubleValue": v}})
        elif isinstance(v, list):
            out.append({"key": k, "value": {"arrayValue": {"values": [{"stringValue": str(x)} for x in v]}}})
        else:
            out.append({"key": k, "value": {"stringValue": str(v)}})
    return out


def _drop_none(d: dict) -> dict:
    return {k: v for k, v in d.items() if v is not None and v != ""}


def _json_str(v) -> str | None:
    """Serialise a value to a JSON string for use as a span attribute.

    Returns None when the value is None or already-empty so that _drop_none
    can filter it out.  Strings are returned as-is (already serialised).
    """
    if v is None:
        return None
    if isinstance(v, str):
        return v or None
    try:
        import json as _json
        return _json.dumps(v, separators=(",", ":"))
    except Exception:
        return str(v) or None


def _safe_int(v) -> int | None:
    if v is None:
        return None
    try:
        return int(v)
    except Exception:
        return None


def _safe_float(v) -> float | None:
    if v is None:
        return None
    try:
        return float(v)
    except Exception:
        return None


def _coerce_cost(v) -> float | None:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).strip().lstrip("$").replace(",", ""))
    except Exception:
        return None


def _to_iso(dt: str | datetime) -> str:
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()
    return dt

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

        root_sid = sid(run_id, "root")
        root_attrs = _drop_none({
            "ar.run_id": run_id,
            "ar.id.thread": thread_id,
            "ar.id.user": user_id,
            "ar.tenant": tenant,
            "ar.question.text": (entry.get("question") or {}).get("nl"),
            "ar.answer.text": (answer.get("message") or "")[:1000] or None,
            "ar.narrative.output": answer.get("message"),
            "ar.copilot.skill_id": str(answer.get("copilotSkillId") or "") or None,
            "deployment.environment": tenant,
            "service.name": "answerrocket-copilot",
            "service.namespace": "answerrocket",
            "gen_ai.conversation.id": thread_id,
            "ar.plan.function_selected": gd.get("Function Selected By Model"),
            "ar.model.label": gd.get("LLM Model Used"),
            "ar.cost.estimated_usd": _coerce_cost(gd.get("Estimated LLM cost USD")),
            "ar.tokens.budget_max": _safe_int(gd.get("Maximum Token Count for Model")),
            "ar.tokens.budget_initial": _safe_int(gd.get("Initial Token Budget without History")),
            "ar.latency.pipeline_seconds": _safe_float(profile[0].get("time")) if profile else None,
        })

        spans = [make_span("chat.pipeline", root_sid, None, "SPAN_KIND_SERVER", root_start_ns, end_ns, root_attrs)]

        # Phase spans
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
                "ar.phase.duration_seconds": n["duration_seconds"],
                "ar.phase.own_duration_seconds": n.get("own_seconds"),
            })
            spans.append(make_span(
                f"phase.{n['name'].lower().replace(' ', '_')}",
                phase_sid, parent_sid, "SPAN_KIND_INTERNAL", s_ns, e_ns, attrs,
            ))

        # LLM call spans
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
                attrs = _drop_none({
                    "ar.run_id": run_id, "ar.stage": stage,
                    "gen_ai.system": "azure.ai.openai",
                    "gen_ai.request.model": resp.get("model"),
                    "gen_ai.usage.input_tokens": _safe_int(usage.get("prompt_tokens")),
                    "gen_ai.usage.output_tokens": _safe_int(usage.get("completion_tokens")),
                    "ar.cost.estimate_usd": _coerce_cost(usage.get("cost_estimate_usd")),
                    "ar.tokens.total": _safe_int(usage.get("total_tokens")),
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

        # Skill + narrative spans
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
                spans.append(make_span(
                    f"skill.{skill_name.lower().replace(' ', '_')}", skill_sid,
                    p_sid, "SPAN_KIND_INTERNAL", sk_start, sk_end,
                    _drop_none({"ar.run_id": run_id, "ar.skill.name": skill_name, "ar.skill.title": first_report.get("title")}),
                ))
                narr_start = max(sk_start, sk_end - 1_000_000_000)
                spans.append(make_span(
                    "skill.narrative", sid(run_id, "narrative"), skill_sid,
                    "SPAN_KIND_CLIENT", narr_start, sk_end,
                    _drop_none({
                        "ar.run_id": run_id,
                        "ar.narrative.purpose": "summarize_skill_output_for_user",
                        "ar.narrative.input": first_report.get("final_message"),
                        "ar.narrative.output": answer.get("message"),
                        "gen_ai.operation.name": "chat",
                    }),
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

"""
Observability client for AnswerRocket.

Fetches pre-assembled OTLP/JSON traces from the observabilityTraces GraphQL
endpoint and delivers them to callers for forwarding to any OTel collector's
/v1/traces endpoint.

OTLP assembly is performed server-side in Kotlin (ObservabilityPublicSchemaModule).
Each trace is a complete OTLP ExportTraceServiceRequest object.

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

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable, Generator, Iterator

from answer_rocket.client_config import ClientConfig
from answer_rocket.graphql.client import GraphQlClient

_logger = logging.getLogger("answer_rocket.observability")

DEFAULT_LIMIT = 100
DEFAULT_POLL_INTERVAL_SECONDS = 60.0


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
    ) -> TracesBatch:
        since_str = _to_iso(since)
        try:
            op = self._gql_client.query()
            obs = op.observability_traces(since=since_str, limit=limit)
            obs.count()
            obs.has_more()
            obs.next_cursor()
            # The full OTLP span tree is strongly typed in the schema, so every field
            # (including attribute KeyValue/AnyValue) must be selected explicitly.
            resource_spans = obs.traces().resource_spans()
            _select_key_values(resource_spans.resource().attributes())
            scope_spans = resource_spans.scope_spans()
            scope = scope_spans.scope()
            scope.name()
            scope.version()
            spans = scope_spans.spans()
            spans.trace_id()
            spans.span_id()
            spans.parent_span_id()
            spans.name()
            spans.kind()
            spans.start_time_unix_nano()
            spans.end_time_unix_nano()
            _select_key_values(spans.attributes())
            events = spans.events()
            events.time_unix_nano()
            events.name()
            _select_key_values(events.attributes())
            spans.status().code()

            result = self._gql_client.submit(op)
            page = result.observability_traces
        except Exception as exc:
            return TracesBatch(success=False, error=str(exc))

        return TracesBatch(
            success=True,
            count=page.count,
            has_more=page.has_more,
            next_cursor=page.next_cursor,
            traces=[_trace_to_otlp(t) for t in (page.traces or [])],
        )

    def iter_traces(
        self,
        since: str | datetime,
        limit: int = DEFAULT_LIMIT,
    ) -> Iterator[list[dict]]:
        cursor: str | datetime = since
        while True:
            result = self.get_traces(cursor, limit=limit)
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
    ) -> Generator[list[dict], None, None]:
        cursor: str | datetime = since
        iterations = 0
        while max_iterations is None or iterations < max_iterations:
            result = self.get_traces(cursor, limit=limit)
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
            else:
                time.sleep(poll_interval_seconds)
            iterations += 1


def _to_iso(dt: str | datetime) -> str:
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()
    return dt


# ---------------------------------------------------------------------------
# GraphQL selection + reconstruction of OTLP/JSON from the typed span tree.
#
# The server emits a fully-typed, versionable span tree; collectors want plain OTLP
# JSON. These helpers select every typed field and map the objects back to the OTLP
# wire shape, omitting absent optional fields so the output matches an OTLP exporter.
# ---------------------------------------------------------------------------

def _select_key_values(kv_selector) -> None:
    """Select an OTLP KeyValue list, including one level of AnyValue.arrayValue."""
    kv_selector.key()
    value = kv_selector.value()
    value.string_value()
    value.bool_value()
    value.int_value()
    value.double_value()
    inner = value.array_value().values()
    inner.string_value()
    inner.bool_value()
    inner.int_value()
    inner.double_value()


def _trace_to_otlp(trace) -> dict:
    return {"resourceSpans": [_resource_spans_to_otlp(rs) for rs in (trace.resource_spans or [])]}


def _resource_spans_to_otlp(rs) -> dict:
    return {
        "resource": {"attributes": [_key_value_to_otlp(kv) for kv in (rs.resource.attributes or [])]},
        "scopeSpans": [_scope_spans_to_otlp(ss) for ss in (rs.scope_spans or [])],
    }


def _scope_spans_to_otlp(ss) -> dict:
    scope: dict = {"name": ss.scope.name}
    if ss.scope.version is not None:
        scope["version"] = ss.scope.version
    return {"scope": scope, "spans": [_span_to_otlp(s) for s in (ss.spans or [])]}


def _span_to_otlp(s) -> dict:
    out = {
        "traceId": s.trace_id,
        "spanId": s.span_id,
        "name": s.name,
        "kind": s.kind,
        "startTimeUnixNano": s.start_time_unix_nano,
        "endTimeUnixNano": s.end_time_unix_nano,
        "attributes": [_key_value_to_otlp(kv) for kv in (s.attributes or [])],
        "events": [_event_to_otlp(e) for e in (s.events or [])],
    }
    if s.parent_span_id is not None:
        out["parentSpanId"] = s.parent_span_id
    if s.status is not None:
        out["status"] = {"code": s.status.code}
    return out


def _event_to_otlp(e) -> dict:
    out = {"name": e.name, "attributes": [_key_value_to_otlp(kv) for kv in (e.attributes or [])]}
    if e.time_unix_nano is not None:
        out["timeUnixNano"] = e.time_unix_nano
    return out


def _key_value_to_otlp(kv) -> dict:
    return {"key": kv.key, "value": _any_value_to_otlp(kv.value)}


def _any_value_to_otlp(v) -> dict:
    """Map a typed OTLP AnyValue back to its single-key wire form."""
    if v.string_value is not None:
        return {"stringValue": v.string_value}
    if v.bool_value is not None:
        return {"boolValue": v.bool_value}
    if v.int_value is not None:
        return {"intValue": v.int_value}
    if v.double_value is not None:
        return {"doubleValue": v.double_value}
    if v.array_value is not None:
        return {"arrayValue": {"values": [_any_value_to_otlp(x) for x in (v.array_value.values or [])]}}
    return {}

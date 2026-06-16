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
            obs.traces()
            result = self._gql_client.submit(op)
            page = result.observability_traces
        except Exception as exc:
            return TracesBatch(success=False, error=str(exc))

        return TracesBatch(
            success=True,
            count=page.count,
            has_more=page.has_more,
            next_cursor=page.next_cursor,
            traces=list(page.traces or []),
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

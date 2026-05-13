"""
Observability polling client for AnswerRocket.

Provides two usage patterns:

  1. Single page fetch:
       result = client.observability.get_traces(since="2026-05-01T00:00:00Z")

  2. Continuous polling loop:
       for batch in client.observability.poll_traces(since="2026-05-01T00:00:00Z"):
           forward_to_collector(batch)

Both return OTLP/JSON ExportTraceServiceRequest dicts — the same format the
live push path emits — so callers can forward them to any OTel collector's
/v1/traces endpoint unchanged.
"""

from __future__ import annotations

import json
import logging
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Callable, Generator, Iterator

from answer_rocket.auth import AuthHelper, init_auth_helper
from answer_rocket.client_config import ClientConfig

_logger = logging.getLogger("answer_rocket.observability")

DEFAULT_LIMIT = 100
DEFAULT_POLL_INTERVAL_SECONDS = 60.0


# ---------------------------------------------------------------------------
# Return types
# ---------------------------------------------------------------------------

@dataclass
class TracesBatch:
    """One page of OTLP/JSON traces returned by the pull endpoint."""
    success: bool = False
    error: str | None = None
    count: int = 0
    has_more: bool = False
    next_cursor: str | None = None
    traces: list[dict] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

class Observability:
    """
    Client for AnswerRocket's OTLP trace pull endpoint.

    Unilever (or any authorised caller) uses this to fetch stored OTLP/JSON
    traces from the AnswerRocket Mongo answer collection, either one page at
    a time or via a continuous polling loop.

    Parameters
    ----------
    config : ClientConfig
        Shared client configuration (url, token, tenant).
    """

    def __init__(self, config: ClientConfig):
        self._config = config
        self._auth_helper: AuthHelper = init_auth_helper(config)

    # ------------------------------------------------------------------
    # Single-page fetch
    # ------------------------------------------------------------------

    def get_traces(
        self,
        since: str | datetime,
        limit: int = DEFAULT_LIMIT,
        tenant: str | None = None,
    ) -> TracesBatch:
        """
        Fetch one page of OTLP/JSON traces from the pull endpoint.

        Parameters
        ----------
        since : str | datetime
            Lower bound for answer.answeredAt (exclusive). ISO-8601 string or
            a datetime object. Must be within the server's retention window
            (default 15 days).
        limit : int
            Maximum number of traces to return. Server caps at 500.
        tenant : str, optional
            Override the tenant from config.

        Returns
        -------
        TracesBatch
            Contains the list of OTLP/JSON dicts plus pagination metadata.
            Check .success before reading .traces.
        """
        since_str = _to_iso(since)
        params: dict[str, str] = {"since": since_str, "limit": str(limit)}
        if tenant:
            params["tenant"] = tenant

        url = self._build_url(params)
        try:
            req = urllib.request.Request(url, headers=self._auth_helper.headers())
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            body_text = _read_http_error(exc)
            return TracesBatch(success=False, error=f"HTTP {exc.code}: {body_text}")
        except Exception as exc:
            return TracesBatch(success=False, error=str(exc))

        return TracesBatch(
            success=True,
            count=body.get("count", 0),
            has_more=body.get("has_more", False),
            next_cursor=body.get("next_cursor"),
            traces=body.get("traces") or [],
        )

    # ------------------------------------------------------------------
    # Multi-page iterator (fetch all pages from a starting cursor)
    # ------------------------------------------------------------------

    def iter_traces(
        self,
        since: str | datetime,
        limit: int = DEFAULT_LIMIT,
        tenant: str | None = None,
    ) -> Iterator[list[dict]]:
        """
        Iterate over all OTLP/JSON traces from `since` until caught up.

        Follows pagination automatically — each iteration yields one batch
        (a list of OTLP/JSON dicts). Stops when has_more is False.

        Example
        -------
        for batch in client.observability.iter_traces(since="2026-05-01T00:00:00Z"):
            for trace in batch:
                post_to_collector(trace)
        """
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

    # ------------------------------------------------------------------
    # Continuous polling loop
    # ------------------------------------------------------------------

    def poll_traces(
        self,
        since: str | datetime,
        on_batch: Callable[[list[dict]], None] | None = None,
        limit: int = DEFAULT_LIMIT,
        poll_interval_seconds: float = DEFAULT_POLL_INTERVAL_SECONDS,
        max_iterations: int | None = None,
        tenant: str | None = None,
    ) -> Generator[list[dict], None, None]:
        """
        Continuously poll for new OTLP/JSON traces, advancing the cursor after
        each page.

        Can be used as a generator (``for batch in client.observability.poll_traces(...):``)
        or with the ``on_batch`` callback convenience argument.

        Parameters
        ----------
        since : str | datetime
            Starting cursor. Typically ``datetime.now(timezone.utc) - timedelta(days=1)``.
        on_batch : callable, optional
            Called with each list of OTLP/JSON dicts. If omitted, callers
            consume via the generator protocol.
        limit : int
            Traces per page. Server caps at 500.
        poll_interval_seconds : float
            Seconds to sleep between polls when there are no new traces.
            Ignored when has_more is True (immediately fetches next page).
        max_iterations : int, optional
            Stop after this many poll cycles. None = run forever.
        tenant : str, optional
            Override the tenant from config.

        Yields
        ------
        list[dict]
            Each yield is one page of OTLP/JSON ExportTraceServiceRequest dicts.

        Example
        -------
        for batch in client.observability.poll_traces(
            since=datetime.now(timezone.utc) - timedelta(hours=24),
            poll_interval_seconds=60,
        ):
            push_to_collector(batch)   # forward to your OTel collector
        """
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

            # If there are more pages, fetch immediately; otherwise wait.
            if not result.has_more:
                time.sleep(poll_interval_seconds)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _build_url(self, params: dict) -> str:
        base = self._config.url.rstrip("/")
        qs = urllib.parse.urlencode(params)
        return f"{base}/api/observability/traces?{qs}"


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------

def _to_iso(dt: str | datetime) -> str:
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()
    return dt


def _read_http_error(exc: urllib.error.HTTPError) -> str:
    try:
        body = exc.read().decode()
        data = json.loads(body)
        return data.get("error") or body
    except Exception:
        return str(exc)

"""
Tests for the Observability polling client.

Uses unittest.mock to avoid needing a live AnswerRocket instance.
Patches GraphQlClient.query_raw (the actual transport used by observability.py)
rather than urllib.request.urlopen (which the implementation never touches).
"""

import unittest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from answer_rocket.client import AnswerRocketClient
from answer_rocket.observability import Observability, TracesBatch, _to_iso


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_client() -> AnswerRocketClient:
    return AnswerRocketClient(url="http://localhost:4000", token="test-token")


# A minimal realistic entry that will produce a non-None OTLP trace.
# It must pass the hasFinished check and have at least one chatPipelineProfile node.
_SAMPLE_ENTRY = {
    "id": "run-abc123",
    "threadId": "thread-1",
    "userId": "user-1",
    "question": {"nl": "What are total sales?"},
    "answer": {
        "answeredAt": "2026-05-10T12:00:00Z",
        "hasFinished": True,
        "message": "Total sales are $1M.",
        "copilotSkillId": "skill-99",
        "generalDiagnostics": {
            "Function Selected By Model": "trend_skill",
            "LLM Model Used": "gpt-4",
            "Estimated LLM cost USD": 0.005,
            "Maximum Token Count for Model": 8192,
            "Initial Token Budget without History": 4096,
            "Chat Model Call Record": [
                {
                    "stage": "Function Selection",
                    "response": {
                        "model": "gpt-4",
                        "created": 1715342400,
                        "usage": {
                            "prompt_tokens": 800,
                            "completion_tokens": 200,
                            "total_tokens": 1000,
                            "cost_estimate_usd": 0.003,
                        },
                    },
                }
            ],
        },
        "chatPipelineProfile": [
            {
                "name": "Chat Pipeline",
                "stack": ["Chat Pipeline"],
                "time": 5.0,
                "own_time": 0.2,
            }
        ],
        "reportResults": [
            {
                "reportName": "trend_skill",
                "title": "Sales Trend",
                "finalMessage": "Trend analysis complete.",
                "preview": None,
                "contentBlocks": [{"id": "cb-1", "type": "chart"}],
                "gzippedDataframesAndMetadata": None,
            }
        ],
    },
}

# A pre-built OTLP trace shell used by tests that only care about count/pagination,
# not internal trace structure. The impl builds real OTLP from entries; tests that
# verify trace content use _SAMPLE_ENTRY and inspect the real output.
_EXPECTED_TRACE_KEYS = {"resourceSpans"}


def _gql_page(entries=None, count=None, has_more=False, next_cursor=None):
    """Build the dict that query_raw returns for observabilityTraces."""
    if entries is None:
        entries = [_SAMPLE_ENTRY]
    if count is None:
        count = len(entries)
    return {
        "observabilityTraces": {
            "count": count,
            "hasMore": has_more,
            "nextCursor": next_cursor,
            "entries": entries,
        }
    }


# ---------------------------------------------------------------------------
# Unit: _to_iso helper
# ---------------------------------------------------------------------------

def test_to_iso_string_passthrough():
    assert _to_iso("2026-05-01T00:00:00Z") == "2026-05-01T00:00:00Z"


def test_to_iso_datetime_utc():
    dt = datetime(2026, 5, 1, 12, 0, 0, tzinfo=timezone.utc)
    assert "2026-05-01" in _to_iso(dt)


def test_to_iso_datetime_naive_coerced_to_utc():
    dt = datetime(2026, 5, 1, 12, 0, 0)
    result = _to_iso(dt)
    assert "2026-05-01" in result


# ---------------------------------------------------------------------------
# Unit: client is attached at correct attribute
# ---------------------------------------------------------------------------

def test_client_has_observability_attr():
    client = _make_client()
    assert hasattr(client, "observability")
    assert isinstance(client.observability, Observability)


# ---------------------------------------------------------------------------
# Unit: get_traces success
# ---------------------------------------------------------------------------

def test_get_traces_success():
    client = _make_client()
    with patch.object(client.observability._gql_client, "query_raw",
                      return_value=_gql_page()) as mock_qr:
        result = client.observability.get_traces(since="2026-05-10T00:00:00Z")

    assert result.success is True
    assert result.count == 1
    assert result.has_more is False
    assert len(result.traces) == 1
    # Each trace must be a valid OTLP envelope
    assert _EXPECTED_TRACE_KEYS.issubset(result.traces[0].keys())
    mock_qr.assert_called_once()


def test_get_traces_pagination_fields():
    client = _make_client()
    entries = [_SAMPLE_ENTRY] * 100
    gql_data = _gql_page(
        entries=entries,
        count=100,
        has_more=True,
        next_cursor="2026-05-10T12:00:00+00:00",
    )
    with patch.object(client.observability._gql_client, "query_raw",
                      return_value=gql_data):
        result = client.observability.get_traces(since="2026-05-10T00:00:00Z", limit=100)

    assert result.has_more is True
    assert result.next_cursor == "2026-05-10T12:00:00+00:00"
    assert result.count == 100


# ---------------------------------------------------------------------------
# Unit: get_traces error handling
# ---------------------------------------------------------------------------

def test_get_traces_http_error():
    client = _make_client()
    with patch.object(client.observability._gql_client, "query_raw",
                      side_effect=Exception("HTTP 400: since param out of window")):
        result = client.observability.get_traces(since="2020-01-01T00:00:00Z")

    assert result.success is False
    assert "400" in result.error or "window" in result.error


def test_get_traces_connection_error():
    client = _make_client()
    with patch.object(client.observability._gql_client, "query_raw",
                      side_effect=ConnectionRefusedError("connection refused")):
        result = client.observability.get_traces(since="2026-05-10T00:00:00Z")

    assert result.success is False
    assert result.error is not None


# ---------------------------------------------------------------------------
# Unit: iter_traces follows pagination
# ---------------------------------------------------------------------------

def test_iter_traces_follows_pages():
    client = _make_client()
    page1 = _gql_page(
        entries=[_SAMPLE_ENTRY, _SAMPLE_ENTRY],
        count=2,
        has_more=True,
        next_cursor="2026-05-10T06:00:00+00:00",
    )
    page2 = _gql_page(
        entries=[_SAMPLE_ENTRY],
        count=1,
        has_more=False,
        next_cursor=None,
    )
    with patch.object(client.observability._gql_client, "query_raw",
                      side_effect=[page1, page2]):
        batches = list(client.observability.iter_traces("2026-05-10T00:00:00Z"))

    assert len(batches) == 2
    assert len(batches[0]) == 2
    assert len(batches[1]) == 1


def test_iter_traces_stops_on_empty():
    client = _make_client()
    gql_data = _gql_page(entries=[], count=0, has_more=False, next_cursor=None)
    with patch.object(client.observability._gql_client, "query_raw",
                      return_value=gql_data):
        batches = list(client.observability.iter_traces("2026-05-10T00:00:00Z"))

    assert batches == []


# ---------------------------------------------------------------------------
# Unit: poll_traces respects max_iterations
# ---------------------------------------------------------------------------

@patch("time.sleep")
def test_poll_traces_max_iterations(mock_sleep):
    client = _make_client()
    with patch.object(client.observability._gql_client, "query_raw",
                      return_value=_gql_page()):
        batches = list(client.observability.poll_traces(
            "2026-05-10T00:00:00Z",
            max_iterations=3,
            poll_interval_seconds=0,
        ))

    assert len(batches) == 3


@patch("time.sleep")
def test_poll_traces_on_batch_callback(mock_sleep):
    received = []
    client = _make_client()

    with patch.object(client.observability._gql_client, "query_raw",
                      return_value=_gql_page()):
        gen = client.observability.poll_traces(
            "2026-05-10T00:00:00Z",
            on_batch=received.append,
            max_iterations=2,
            poll_interval_seconds=0,
        )
        list(gen)  # drive the generator

    assert len(received) == 2
    assert all(isinstance(b, list) for b in received)


@patch("time.sleep")
def test_poll_traces_skips_empty_batches(mock_sleep):
    client = _make_client()
    gql_data = _gql_page(entries=[], count=0, has_more=False, next_cursor=None)
    with patch.object(client.observability._gql_client, "query_raw",
                      return_value=gql_data):
        batches = list(client.observability.poll_traces(
            "2026-05-10T00:00:00Z",
            max_iterations=2,
            poll_interval_seconds=0,
        ))

    # Empty pages should not yield
    assert batches == []


# ---------------------------------------------------------------------------
# Unit: GraphQL query variables are passed correctly
# ---------------------------------------------------------------------------

def test_get_traces_passes_correct_variables():
    """query_raw must receive the right since/limit variables."""
    client = _make_client()
    with patch.object(client.observability._gql_client, "query_raw",
                      return_value=_gql_page()) as mock_qr:
        client.observability.get_traces(since="2026-05-10T00:00:00Z", limit=50)

    _, kwargs = mock_qr.call_args
    variables = kwargs.get("variables") or mock_qr.call_args[0][1]
    assert variables["since"] == "2026-05-10T00:00:00Z"
    assert variables["limit"] == 50

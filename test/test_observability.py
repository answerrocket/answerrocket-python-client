"""Tests for the Observability client (GraphQL-backed, OTLP assembled server-side)."""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

from answer_rocket.observability import Observability, TracesBatch, DEFAULT_LIMIT
from answer_rocket.client_config import ClientConfig

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SAMPLE_OTLP_TRACE = {
    "resourceSpans": [{
        "resource": {"attributes": [{"key": "service.name", "value": {"stringValue": "answerrocket-copilot"}}]},
        "scopeSpans": [{"scope": {"name": "answerrocket.copilot"}, "spans": [
            {"traceId": "abc123", "spanId": "def456", "name": "chat.pipeline",
             "kind": "SPAN_KIND_SERVER", "startTimeUnixNano": "1000", "endTimeUnixNano": "2000",
             "attributes": [], "status": {"code": "STATUS_CODE_OK"}},
        ]}],
    }]
}


def _typed_span(s):
    """Mimic a typed sgqlc Span object built from an OTLP span dict."""
    m = MagicMock()
    m.trace_id = s["traceId"]
    m.span_id = s["spanId"]
    m.name = s["name"]
    m.kind = s["kind"]
    m.start_time_unix_nano = s["startTimeUnixNano"]
    m.end_time_unix_nano = s["endTimeUnixNano"]
    m.attributes = s.get("attributes", [])
    m.parent_span_id = s.get("parentSpanId")          # None when absent
    m.events = s.get("events")                        # None when absent
    if "status" in s:
        st = MagicMock(); st.code = s["status"]["code"]; m.status = st
    else:
        m.status = None
    return m


def _typed_scope_spans(ss):
    m = MagicMock()
    sc = MagicMock(); sc.name = ss["scope"]["name"]; sc.version = ss["scope"].get("version")
    m.scope = sc
    m.spans = [_typed_span(s) for s in ss["spans"]]
    return m


def _typed_resource_spans(rs):
    m = MagicMock()
    res = MagicMock(); res.attributes = rs["resource"]["attributes"]
    m.resource = res
    m.scope_spans = [_typed_scope_spans(ss) for ss in rs["scopeSpans"]]
    return m


def _typed_trace(otlp):
    """Mimic the typed sgqlc ObservabilityTrace tree built from an OTLP dict."""
    t = MagicMock()
    t.resource_spans = [_typed_resource_spans(rs) for rs in otlp["resourceSpans"]]
    return t


def _make_gql_page(traces=None, count=None, has_more=False, next_cursor=None):
    """Build a mock sgqlc result whose `traces` are typed objects (as the server returns)."""
    otlp = traces or []
    page = MagicMock()
    page.count = count if count is not None else len(otlp)
    page.has_more = has_more
    page.next_cursor = next_cursor
    page.traces = [_typed_trace(t) for t in otlp]
    return page


def _make_client():
    config = MagicMock(spec=ClientConfig)
    config.tenant = "test_tenant"
    gql_client = MagicMock()
    return config, gql_client, Observability(config, gql_client)


# ---------------------------------------------------------------------------
# Basic attribute tests
# ---------------------------------------------------------------------------

def test_client_has_observability_attr():
    _, _, obs = _make_client()
    assert isinstance(obs, Observability)


def test_to_iso_string_passthrough():
    from answer_rocket.observability import _to_iso
    assert _to_iso("2026-01-01T00:00:00Z") == "2026-01-01T00:00:00Z"


def test_to_iso_datetime_naive():
    from answer_rocket.observability import _to_iso
    dt = datetime(2026, 1, 1, 12, 0, 0)
    result = _to_iso(dt)
    assert "2026-01-01" in result
    assert "+00:00" in result or "UTC" in result


def test_to_iso_datetime_aware():
    from answer_rocket.observability import _to_iso
    dt = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    result = _to_iso(dt)
    assert "2026-01-01" in result


# ---------------------------------------------------------------------------
# get_traces
# ---------------------------------------------------------------------------

def test_get_traces_success():
    config, gql_client, obs = _make_client()
    mock_result = MagicMock()
    mock_result.observability_traces = _make_gql_page(
        traces=[_SAMPLE_OTLP_TRACE], count=1, has_more=False
    )
    gql_client.submit.return_value = mock_result

    batch = obs.get_traces("2026-01-01T00:00:00Z")

    assert batch.success is True
    assert batch.count == 1
    assert batch.has_more is False
    assert batch.next_cursor is None
    assert len(batch.traces) == 1
    assert batch.traces[0] == _SAMPLE_OTLP_TRACE


def test_get_traces_passes_correct_variables():
    config, gql_client, obs = _make_client()
    mock_result = MagicMock()
    mock_result.observability_traces = _make_gql_page()
    gql_client.submit.return_value = mock_result

    mock_op = MagicMock()
    mock_obs_field = MagicMock()
    mock_op.observability_traces.return_value = mock_obs_field
    gql_client.query.return_value = mock_op

    obs.get_traces("2026-05-01T00:00:00Z", limit=50)

    mock_op.observability_traces.assert_called_once_with(since="2026-05-01T00:00:00Z", limit=50)


def test_get_traces_pagination_fields():
    config, gql_client, obs = _make_client()
    mock_result = MagicMock()
    mock_result.observability_traces = _make_gql_page(
        traces=[_SAMPLE_OTLP_TRACE], count=1, has_more=True, next_cursor="2026-06-01T00:00:00Z"
    )
    gql_client.submit.return_value = mock_result

    batch = obs.get_traces("2026-01-01T00:00:00Z")

    assert batch.has_more is True
    assert batch.next_cursor == "2026-06-01T00:00:00Z"


def test_get_traces_connection_error():
    config, gql_client, obs = _make_client()
    gql_client.submit.side_effect = ConnectionError("timeout")

    batch = obs.get_traces("2026-01-01T00:00:00Z")

    assert batch.success is False
    assert "timeout" in batch.error
    assert batch.traces == []


def test_get_traces_empty_page():
    config, gql_client, obs = _make_client()
    mock_result = MagicMock()
    mock_result.observability_traces = _make_gql_page(traces=[], count=0, has_more=False)
    gql_client.submit.return_value = mock_result

    batch = obs.get_traces("2026-01-01T00:00:00Z")

    assert batch.success is True
    assert batch.count == 0
    assert batch.traces == []


# ---------------------------------------------------------------------------
# iter_traces
# ---------------------------------------------------------------------------

def test_iter_traces_follows_pages():
    config, gql_client, obs = _make_client()
    page1 = MagicMock()
    page1.observability_traces = _make_gql_page(
        traces=[_SAMPLE_OTLP_TRACE], count=1, has_more=True, next_cursor="cursor_1"
    )
    page2 = MagicMock()
    page2.observability_traces = _make_gql_page(
        traces=[_SAMPLE_OTLP_TRACE], count=1, has_more=False
    )
    gql_client.submit.side_effect = [page1, page2]

    batches = list(obs.iter_traces("2026-01-01T00:00:00Z"))

    assert len(batches) == 2
    assert gql_client.submit.call_count == 2


def test_iter_traces_stops_on_empty():
    config, gql_client, obs = _make_client()
    mock_result = MagicMock()
    mock_result.observability_traces = _make_gql_page(traces=[], has_more=False)
    gql_client.submit.return_value = mock_result

    batches = list(obs.iter_traces("2026-01-01T00:00:00Z"))

    assert batches == []


def test_iter_traces_stops_on_error():
    config, gql_client, obs = _make_client()
    gql_client.submit.side_effect = Exception("server error")

    batches = list(obs.iter_traces("2026-01-01T00:00:00Z"))

    assert batches == []


# ---------------------------------------------------------------------------
# poll_traces
# ---------------------------------------------------------------------------

def test_poll_traces_max_iterations():
    config, gql_client, obs = _make_client()
    mock_result = MagicMock()
    mock_result.observability_traces = _make_gql_page(
        traces=[_SAMPLE_OTLP_TRACE], count=1, has_more=False
    )
    gql_client.submit.return_value = mock_result

    with patch("time.sleep"):
        batches = list(obs.poll_traces("2026-01-01T00:00:00Z", max_iterations=3))

    assert len(batches) == 3


def test_poll_traces_skips_empty_batches():
    config, gql_client, obs = _make_client()
    mock_result = MagicMock()
    mock_result.observability_traces = _make_gql_page(traces=[], has_more=False)
    gql_client.submit.return_value = mock_result

    with patch("time.sleep"):
        batches = list(obs.poll_traces("2026-01-01T00:00:00Z", max_iterations=2))

    assert batches == []


def test_poll_traces_on_batch_callback():
    config, gql_client, obs = _make_client()
    mock_result = MagicMock()
    mock_result.observability_traces = _make_gql_page(
        traces=[_SAMPLE_OTLP_TRACE], count=1, has_more=False
    )
    gql_client.submit.return_value = mock_result

    received = []
    with patch("time.sleep"):
        for _ in obs.poll_traces("2026-01-01T00:00:00Z", on_batch=received.extend, max_iterations=1):
            pass

    assert len(received) == 1
    assert received[0] == _SAMPLE_OTLP_TRACE


# ---------------------------------------------------------------------------
# Cursor handling
# ---------------------------------------------------------------------------

def test_get_traces_converts_datetime_cursor_to_iso():
    config, gql_client, obs = _make_client()
    mock_result = MagicMock()
    mock_result.observability_traces = _make_gql_page()
    gql_client.submit.return_value = mock_result
    mock_op = MagicMock()
    gql_client.query.return_value = mock_op

    obs.get_traces(datetime(2026, 5, 1, 12, 0, 0, tzinfo=timezone.utc), limit=10)

    _, kwargs = mock_op.observability_traces.call_args
    assert kwargs["since"].startswith("2026-05-01T12:00:00")
    assert kwargs["limit"] == 10


def test_iter_traces_threads_next_cursor_as_since():
    """Page 2 must be requested with `since` == page 1's next_cursor (no re-scan, no gaps)."""
    config, gql_client, obs = _make_client()
    page1 = MagicMock()
    page1.observability_traces = _make_gql_page(
        traces=[_SAMPLE_OTLP_TRACE], has_more=True, next_cursor="2026-05-01T12:00:01Z"
    )
    page2 = MagicMock()
    page2.observability_traces = _make_gql_page(traces=[_SAMPLE_OTLP_TRACE], has_more=False)
    gql_client.submit.side_effect = [page1, page2]

    mock_op = MagicMock()
    gql_client.query.return_value = mock_op

    list(obs.iter_traces("2026-05-01T00:00:00Z"))

    calls = mock_op.observability_traces.call_args_list
    assert len(calls) == 2
    assert calls[0].kwargs["since"] == "2026-05-01T00:00:00Z"
    assert calls[1].kwargs["since"] == "2026-05-01T12:00:01Z"


# ---------------------------------------------------------------------------
# Contract: SDK faithfully passes server-assembled OTLP through (ties both PRs)
# ---------------------------------------------------------------------------

def _load_golden_trace():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures", "example_otlp_trace.json")
    with open(path) as f:
        return json.load(f)


def test_contract_reconstructs_real_server_trace_to_identical_otlp():
    config, gql_client, obs = _make_client()
    golden = _load_golden_trace()
    mock_result = MagicMock()
    mock_result.observability_traces = _make_gql_page(traces=[golden], count=1, has_more=False)
    gql_client.submit.return_value = mock_result

    batch = obs.get_traces("2026-05-01T00:00:00Z")

    assert batch.success is True
    assert batch.count == 1
    # The typed span tree must reconstruct byte-identically to the server's OTLP.
    assert batch.traces[0] == golden


def test_reconstruction_omits_absent_optional_span_fields():
    from answer_rocket.observability import _span_to_otlp
    full = _typed_span({
        "traceId": "t", "spanId": "s", "name": "n", "kind": "SPAN_KIND_INTERNAL",
        "startTimeUnixNano": "1", "endTimeUnixNano": "2", "attributes": [{"key": "k", "value": {"stringValue": "v"}}],
        "parentSpanId": "p", "events": [{"name": "e"}], "status": {"code": "STATUS_CODE_OK"},
    })
    assert _span_to_otlp(full) == {
        "traceId": "t", "spanId": "s", "name": "n", "kind": "SPAN_KIND_INTERNAL",
        "startTimeUnixNano": "1", "endTimeUnixNano": "2",
        "attributes": [{"key": "k", "value": {"stringValue": "v"}}],
        "parentSpanId": "p", "events": [{"name": "e"}], "status": {"code": "STATUS_CODE_OK"},
    }

    minimal = _typed_span({
        "traceId": "t", "spanId": "s", "name": "root", "kind": "SPAN_KIND_SERVER",
        "startTimeUnixNano": "1", "endTimeUnixNano": "2", "attributes": [],
    })
    out = _span_to_otlp(minimal)
    assert "parentSpanId" not in out
    assert "events" not in out
    assert "status" not in out
    assert out["attributes"] == []


def test_contract_returned_trace_is_valid_otlp():
    config, gql_client, obs = _make_client()
    golden = _load_golden_trace()
    mock_result = MagicMock()
    mock_result.observability_traces = _make_gql_page(traces=[golden], count=1)
    gql_client.submit.return_value = mock_result

    trace = obs.get_traces("2026-05-01T00:00:00Z").traces[0]

    spans = trace["resourceSpans"][0]["scopeSpans"][0]["spans"]
    names = [s["name"] for s in spans]
    assert "chat.pipeline" in names
    assert any(n.startswith("phase.") for n in names)
    assert "skill.narrative" in names
    # All spans share one traceId; every span has the required OTLP fields.
    trace_ids = {s["traceId"] for s in spans}
    assert len(trace_ids) == 1
    for s in spans:
        assert s["spanId"]
        assert s["startTimeUnixNano"] and s["endTimeUnixNano"]
        assert int(s["startTimeUnixNano"]) <= int(s["endTimeUnixNano"])

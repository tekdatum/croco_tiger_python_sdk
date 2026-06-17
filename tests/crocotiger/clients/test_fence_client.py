import pytest

from datetime import datetime

from crocotiger.clients.fence_client import FenceClient
from crocotiger.models.fence_correction import FenceCorrection
from crocotiger.models.fence_event import FenceEvent, FenceEventPage
from crocotiger.models.fence_validation import FenceValidation


@pytest.fixture
def mock_rest_client(mocker):
    """Fixture to provide a mocked RestClient."""
    return mocker.Mock()


def test_init(mock_rest_client):
    """Verifies __init__ sets the rest_client and internal endpoint."""
    client = FenceClient(mock_rest_client)
    assert client._rest_client == mock_rest_client
    assert client._endpoint == "/fence"


def test_validate(mock_rest_client):
    """Verifies validate calls post with full payload and returns FenceValidation."""
    client = FenceClient(mock_rest_client)

    # Mock data strictly matching FenceValidation fields
    mock_data = {
        "text": "Some text",
        "valid": True,
        "reason_code": "OK",
        "category": "IN_TOPIC",
        "duration": 0.5,
        "extra": {"accept_score": 0.91, "reject_score": 0.11},
    }
    mock_rest_client.post.return_value = mock_data

    project_id = 123
    text_to_validate = "Some text"

    result = client.validate(project_id, text_to_validate)

    assert isinstance(result, FenceValidation)
    assert result.text == mock_data["text"]
    assert result.valid == mock_data["valid"]
    assert result.category == "IN_TOPIC"
    assert result.extra["accept_score"] == 0.91

    expected_url = f"/fence/validate/{project_id}"
    mock_rest_client.post.assert_called_once_with(
        expected_url, data={"text": text_to_validate}
    )


def test_commit_corrections(mock_rest_client):
    """Verifies commit_corrections posts all corrections serialised as dicts."""
    client = FenceClient(mock_rest_client)
    mock_rest_client.post.return_value = None

    corrections = [
        FenceCorrection(text="bad text", valid=False, category="ATTACK"),
        FenceCorrection(text="good text", valid=True),
    ]

    client.commit_corrections(123, corrections)

    mock_rest_client.post.assert_called_once_with(
        "/fence/commit/123",
        data={
            "corrections": [
                {"text": "bad text", "valid": False, "category": "ATTACK"},
                {"text": "good text", "valid": True, "category": None},
            ]
        },
    )


def test_commit_corrections_empty_raises(mock_rest_client):
    """Verifies commit_corrections with an empty list still calls the endpoint."""
    client = FenceClient(mock_rest_client)
    mock_rest_client.post.return_value = None

    client.commit_corrections(123, [])

    mock_rest_client.post.assert_called_once_with(
        "/fence/commit/123", data={"corrections": []}
    )


SAMPLE_EVENT = {
    "id": 1,
    "project_id": 42,
    "text": "test",
    "valid": True,
    "reason_code": "accepted",
    "accept_score": 0.9,
    "accept_anomaly_score": 0.1,
    "accepted_nearest_neighbor": None,
    "accepted_nearest_neighbor_category": None,
    "reject_score": 0.1,
    "reject_anomaly_score": 0.0,
    "rejected_nearest_neighbor": None,
    "rejected_nearest_neighbor_category": None,
    "ip_address": None,
    "device_type": None,
    "duration": 0.05,
    "timestamp": "2026-06-10T14:00:00",
}


def test_find_events_default_params(mock_rest_client):
    """Verifies find_events calls get_paged with default limit/offset."""
    client = FenceClient(mock_rest_client)
    mock_rest_client.get_paged.return_value = {
        "total": 1,
        "offset": 0,
        "limit": 50,
        "data": [SAMPLE_EVENT],
    }

    result = client.find_events(project_id=42)

    mock_rest_client.get_paged.assert_called_once_with(
        "/fence/events/42", params={"limit": 50, "offset": 0}
    )
    assert isinstance(result, FenceEventPage)
    assert result.total == 1
    assert len(result.data) == 1
    assert isinstance(result.data[0], FenceEvent)


def test_find_events_with_pagination(mock_rest_client):
    """Verifies find_events passes custom limit and offset."""
    client = FenceClient(mock_rest_client)
    mock_rest_client.get_paged.return_value = {
        "total": 100,
        "offset": 20,
        "limit": 10,
        "data": [],
    }

    client.find_events(project_id=42, limit=10, offset=20)

    mock_rest_client.get_paged.assert_called_once_with(
        "/fence/events/42", params={"limit": 10, "offset": 20}
    )


def test_find_events_with_date_filters(mock_rest_client):
    """Verifies find_events includes ISO-formatted date params when provided."""
    client = FenceClient(mock_rest_client)
    mock_rest_client.get_paged.return_value = {
        "total": 0,
        "offset": 0,
        "limit": 50,
        "data": [],
    }
    start = datetime(2026, 6, 1, 0, 0, 0)
    end = datetime(2026, 6, 10, 23, 59, 59)

    client.find_events(project_id=42, start_date=start, end_date=end)

    call_params = mock_rest_client.get_paged.call_args[1]["params"]
    assert call_params["start_date"] == start.isoformat()
    assert call_params["end_date"] == end.isoformat()


def test_find_events_omits_none_dates(mock_rest_client):
    """Verifies find_events does not include date keys when not provided."""
    client = FenceClient(mock_rest_client)
    mock_rest_client.get_paged.return_value = {
        "total": 0,
        "offset": 0,
        "limit": 50,
        "data": [],
    }

    client.find_events(project_id=42)

    call_params = mock_rest_client.get_paged.call_args[1]["params"]
    assert "start_date" not in call_params
    assert "end_date" not in call_params

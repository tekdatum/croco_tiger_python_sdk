import pytest

from crocotiger.clients.fence_client import FenceClient
from crocotiger.models.fence_correction import FenceCorrection
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

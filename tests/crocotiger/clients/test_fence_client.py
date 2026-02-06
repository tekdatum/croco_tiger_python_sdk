import pytest

from crocotiger.clients.fence_client import FenceClient
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
        "duration": 0.5,
    }
    mock_rest_client.post.return_value = mock_data

    project_id = 123
    text_to_validate = "Some text"

    result = client.validate(project_id, text_to_validate)

    assert isinstance(result, FenceValidation)
    assert result.text == mock_data["text"]
    assert result.valid == mock_data["valid"]

    expected_url = f"/fence/validate/{project_id}"
    mock_rest_client.post.assert_called_once_with(
        expected_url, data={"text": text_to_validate}
    )

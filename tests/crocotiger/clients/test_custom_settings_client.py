import pytest
from datetime import datetime

from crocotiger.clients.custom_settings_client import CustomSettingsClient
from crocotiger.models.custom_settings import CustomSettings


@pytest.fixture
def mock_rest_client(mocker):
    """Fixture to provide a mocked RestClient."""
    return mocker.Mock()


@pytest.fixture
def sample_settings_data():
    """Returns a dict that matches CustomSettings schema."""
    return {
        "id": 1,
        "openai_key": "sk-123",
        "gemini_key": "gm-456",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }


def test_init(mock_rest_client):
    """Verifies __init__ sets the rest_client and base_path."""
    client = CustomSettingsClient(mock_rest_client)
    assert client._rest_client == mock_rest_client
    assert client.base_path == "/custom-settings"


def test_find_custom_settings(mock_rest_client, sample_settings_data):
    """Verifies find_custom_settings calls get and returns a CustomSettings object."""
    # Arrange
    client = CustomSettingsClient(mock_rest_client)
    mock_rest_client.get.return_value = sample_settings_data

    # Act
    result = client.find_custom_settings()

    # Assert
    mock_rest_client.get.assert_called_once_with("/custom-settings")
    assert isinstance(result, CustomSettings)
    assert result.id == sample_settings_data["id"]


def test_update_custom_settings(mock_rest_client, sample_settings_data):
    """Verifies update_custom_settings calls put with payload and returns the model."""
    # Arrange
    client = CustomSettingsClient(mock_rest_client)
    mock_rest_client.put.return_value = sample_settings_data
    payload = {"openai_key": "new-key", "gemini_key": None}

    # Act
    result = client.update_custom_settings(openai_key="new-key", gemini_key=None)

    # Assert
    mock_rest_client.put.assert_called_once_with("/custom-settings", data=payload)
    assert isinstance(result, CustomSettings)
    assert result.openai_key == "sk-123"  # Value from sample_settings_data


def test_clear_llms_keys(mock_rest_client, sample_settings_data):
    """Verifies clear_llms_keys calls the specific endpoint with empty data."""
    # Arrange
    client = CustomSettingsClient(mock_rest_client)
    # Simulate keys being cleared in the response
    cleared_data = sample_settings_data.copy()
    cleared_data["openai_key"] = None
    cleared_data["gemini_key"] = None
    mock_rest_client.put.return_value = cleared_data

    # Act
    result = client.clear_llms_keys()

    # Assert
    mock_rest_client.put.assert_called_once_with("/custom-settings/clear-keys", data={})
    assert isinstance(result, CustomSettings)
    assert result.openai_key is None
    assert result.gemini_key is None

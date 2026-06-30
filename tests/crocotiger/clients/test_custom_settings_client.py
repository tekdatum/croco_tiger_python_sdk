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
        "deepseek_key": "ds-789",
        "otlp_endpoint": "https://otlp.example.com",
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
    """Verifies update_custom_settings only sends the provided keys."""
    # Arrange
    client = CustomSettingsClient(mock_rest_client)
    mock_rest_client.put.return_value = sample_settings_data

    # Act
    result = client.update_custom_settings(openai_key="new-key", gemini_key=None)

    # Assert: gemini_key is None, so it is omitted from the payload
    mock_rest_client.put.assert_called_once_with(
        "/custom-settings", data={"openai_key": "new-key"}
    )
    assert isinstance(result, CustomSettings)
    assert result.openai_key == "sk-123"  # Value from sample_settings_data


def test_update_custom_settings_with_deepseek_and_otlp(
    mock_rest_client, sample_settings_data
):
    """Verifies deepseek_key and otlp_endpoint are forwarded when provided."""
    client = CustomSettingsClient(mock_rest_client)
    mock_rest_client.put.return_value = sample_settings_data

    result = client.update_custom_settings(
        deepseek_key="ds-789", otlp_endpoint="https://otlp.example.com"
    )

    mock_rest_client.put.assert_called_once_with(
        "/custom-settings",
        data={
            "deepseek_key": "ds-789",
            "otlp_endpoint": "https://otlp.example.com",
        },
    )
    assert isinstance(result, CustomSettings)
    assert result.deepseek_key == "ds-789"
    assert result.otlp_endpoint == "https://otlp.example.com"


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


def test_clear_llms_keys_returns_none_when_no_settings(mock_rest_client):
    """Verifies clear_llms_keys returns None when the server responds with null data."""
    # Arrange
    client = CustomSettingsClient(mock_rest_client)
    mock_rest_client.put.return_value = None

    # Act
    result = client.clear_llms_keys()

    # Assert
    mock_rest_client.put.assert_called_once_with("/custom-settings/clear-keys", data={})
    assert result is None


@pytest.mark.parametrize(
    "method_name, endpoint",
    [
        ("delete_openai_key", "/custom-settings/openai-key"),
        ("delete_gemini_key", "/custom-settings/gemini-key"),
        ("delete_deepseek_key", "/custom-settings/deepseek-key"),
        ("delete_otlp_endpoint", "/custom-settings/otlp-endpoint"),
    ],
)
def test_delete_single_setting(
    mock_rest_client, sample_settings_data, method_name, endpoint
):
    """Each individual clear route DELETEs its endpoint and parses the result."""
    client = CustomSettingsClient(mock_rest_client)
    mock_rest_client.delete.return_value = sample_settings_data

    result = getattr(client, method_name)()

    mock_rest_client.delete.assert_called_once_with(endpoint)
    assert isinstance(result, CustomSettings)


@pytest.mark.parametrize(
    "method_name, endpoint",
    [
        ("delete_openai_key", "/custom-settings/openai-key"),
        ("delete_gemini_key", "/custom-settings/gemini-key"),
        ("delete_deepseek_key", "/custom-settings/deepseek-key"),
        ("delete_otlp_endpoint", "/custom-settings/otlp-endpoint"),
    ],
)
def test_delete_single_setting_returns_none_when_no_settings(
    mock_rest_client, method_name, endpoint
):
    """Each individual clear route returns None when the server responds with null."""
    client = CustomSettingsClient(mock_rest_client)
    mock_rest_client.delete.return_value = None

    result = getattr(client, method_name)()

    mock_rest_client.delete.assert_called_once_with(endpoint)
    assert result is None

import pytest

from crocotiger.clients.llm_models_client import LLMModelsClient
from crocotiger.models.llm_model import LLMModels


@pytest.fixture
def mock_rest_client(mocker):
    """Fixture to provide a mocked RestClient."""
    return mocker.Mock()


@pytest.fixture
def sample_llm_models_data():
    """Returns a valid LLM models catalog payload."""
    return {
        "openai": [
            {
                "model": "gpt-4o",
                "label": "GPT-4o",
                "message": "Recommended",
                "recommended": True,
            }
        ],
        "gemini": [
            {
                "model": "gemini-2.0-flash",
                "label": "Gemini 2.0 Flash",
                "message": "",
                "recommended": False,
            }
        ],
        "deepseek": [
            {
                "model": "deepseek-chat",
                "label": "DeepSeek Chat",
                "message": "",
                "recommended": False,
            }
        ],
    }


def test_init(mock_rest_client):
    """Verifies __init__ sets the rest_client and endpoint."""
    client = LLMModelsClient(mock_rest_client)
    assert client._rest_client == mock_rest_client
    assert client._endpoint == "/llm-models"


def test_find_llm_models(mock_rest_client, sample_llm_models_data):
    """Verifies find_llm_models calls get and parses the catalog."""
    client = LLMModelsClient(mock_rest_client)
    mock_rest_client.get.return_value = sample_llm_models_data

    result = client.find_llm_models()

    mock_rest_client.get.assert_called_once_with("/llm-models")
    assert isinstance(result, LLMModels)
    assert result.openai[0].model == "gpt-4o"
    assert result.gemini[0].label == "Gemini 2.0 Flash"
    assert result.deepseek[0].model == "deepseek-chat"


def test_refresh_llm_models(mock_rest_client, sample_llm_models_data):
    """Verifies refresh_llm_models posts to the refresh endpoint with empty body."""
    client = LLMModelsClient(mock_rest_client)
    mock_rest_client.post.return_value = sample_llm_models_data

    result = client.refresh_llm_models()

    mock_rest_client.post.assert_called_once_with("/llm-models/refresh", data={})
    assert isinstance(result, LLMModels)
    assert result.openai[0].recommended is True

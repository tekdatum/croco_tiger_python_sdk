import zipfile
import pytest
from datetime import datetime

from crocotiger.clients.project_client import ProjectClient
from crocotiger.enums.build_step import BuildStep
from crocotiger.enums.project_status import ProjectStatus
from crocotiger.models.project import Project


@pytest.fixture
def mock_rest_client(mocker):
    """Fixture to provide a mocked RestClient."""
    return mocker.Mock()


@pytest.fixture
def sample_project_data():
    """Returns a valid dictionary to satisfy Project model validation."""
    return {
        "id": 1,
        "name": "Test Project",
        "topic": "AI",
        "restricted_topics": [],
        "context": "Context",
        "total_topic_questions": 5,
        "status": ProjectStatus.DONE,
        "last_build_step": BuildStep.DONE,
        "accept_threshold": 0.8,
        "reject_threshold": 0.2,
        "created_at": datetime.now(),
    }


def test_init(mock_rest_client):
    """Verifies __init__ sets the rest_client and internal endpoint."""
    client = ProjectClient(mock_rest_client)
    assert client._rest_client == mock_rest_client
    assert client._endpoint == "/project"


def test_create(mock_rest_client, sample_project_data):
    """Verifies create calls post with full payload and returns Project."""
    client = ProjectClient(mock_rest_client)
    mock_rest_client.post.return_value = sample_project_data
    payload = {
        "name": "New",
        "context": "Ctx",
        "topic": "T",
        "restricted_topics": [],
        "url": "/here",
        "total_topic_questions": 10,
        "zip": "",
    }
    result = client.create(**payload)

    assert isinstance(result, Project)
    mock_rest_client.post.assert_called_once_with("/project/create", data=payload)


def test_find_all(mock_rest_client, sample_project_data):
    """Verifies find_all returns a list of Project objects."""
    client = ProjectClient(mock_rest_client)
    mock_rest_client.get.return_value = [sample_project_data, sample_project_data]
    limit = 50
    offset = 0
    result = client.find_all(limit, offset)
    url = f"/project?limit={limit}&offset={offset}"

    assert len(result) == 2
    assert isinstance(result[0], Project)
    mock_rest_client.get.assert_called_once_with(url)


def test_update(mock_rest_client, sample_project_data):
    """Verifies update calls post with project_id in URL."""
    client = ProjectClient(mock_rest_client)
    mock_rest_client.post.return_value = sample_project_data
    payload = {
        "name": "New",
        "context": "Ctx",
        "topic": "T",
        "restricted_topics": [],
        "url": "/here",
        "total_topic_questions": 10,
        "zip": "",
    }

    result = client.update(project_id=99, **payload)

    mock_rest_client.post.assert_called_once_with("/project/update/99", data=payload)
    assert result.id == 1


def test_delete(mock_rest_client):
    """Verifies delete calls post to the delete endpoint."""
    client = ProjectClient(mock_rest_client)

    client.delete(project_id=123)

    mock_rest_client.post.assert_called_once_with("/project/delete/123", data={})


def test_find_one(mock_rest_client, sample_project_data):
    """Verifies find_one calls get with the project_id."""
    client = ProjectClient(mock_rest_client)
    mock_rest_client.get.return_value = sample_project_data

    result = client.find_one(456)

    mock_rest_client.get.assert_called_once_with("/project/456")
    assert isinstance(result, Project)


def test_upload_chained_zip(mock_rest_client, tmp_path):
    """Verifies upload_chained_zip uploads the file and returns response dict."""
    client = ProjectClient(mock_rest_client)

    d = tmp_path / "data"
    d.mkdir()
    zip_file = d / "test.zip"

    with zipfile.ZipFile(zip_file, "w") as zipf:
        zipf.writestr("test.txt", "This is a test file")

    api_response = {"name": "data.zip", "size": 1024}
    mock_rest_client.upload_file.return_value = api_response
    result = client.upload_chained_zip(1, str(zip_file), rewrite=False)

    assert result["name"] == "data.zip"
    assert isinstance(result["size"], int)
    assert result == api_response

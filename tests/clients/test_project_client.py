import pytest
from datetime import datetime
from clients.project_client import ProjectClient
from models.project import Project
from enums.ProjectStatus import ProjectStatus
from enums.BuildStep import BuildStep


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

    result = client.find_all()

    assert len(result) == 2
    assert isinstance(result[0], Project)
    mock_rest_client.get.assert_called_once_with("/project/all")


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


def test_upload_chained_zip(mock_rest_client):
    """Verifies upload_chained_zip raises NotImplementedError."""
    client = ProjectClient(mock_rest_client)

    with pytest.raises(NotImplementedError) as excinfo:
        client.upload_chained_zip(1, "path/to/file")

    assert "not implemented yet" in str(excinfo.value)

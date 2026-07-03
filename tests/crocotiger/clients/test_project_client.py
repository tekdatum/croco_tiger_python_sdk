import zipfile
import pytest
from datetime import datetime

from crocotiger.clients.project_client import ProjectClient
from crocotiger.enums.build_step import BuildStep
from crocotiger.enums.project_status import ProjectStatus
from crocotiger.models.project import Project
from crocotiger.models.project_build import ProjectBuild


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


@pytest.fixture
def sample_build_data():
    """Returns a valid dictionary to satisfy ProjectBuild model validation."""
    return {
        "id": 7,
        "project_id": 1,
        "build_number": 3,
        "status": ProjectStatus.DONE,
        "last_build_step": BuildStep.DONE,
        "accept_threshold": 0.8,
        "reject_threshold": 0.2,
        "is_active": True,
        "created_at": datetime.now(),
        "topic": "AI",
        "context": "Context",
        "restricted_topics": [],
        "total_topic_questions": 5,
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
    mock_rest_client.post.assert_called_once_with("/project", data=payload)


def test_create_minimal(mock_rest_client, sample_project_data):
    """Verifies create omits optional fields left as None from the payload."""
    client = ProjectClient(mock_rest_client)
    mock_rest_client.post.return_value = sample_project_data

    result = client.create(name="New", context="Ctx", topic="T")

    assert isinstance(result, Project)
    mock_rest_client.post.assert_called_once_with(
        "/project", data={"name": "New", "context": "Ctx", "topic": "T"}
    )


def test_create_with_config_fields(mock_rest_client, sample_project_data):
    """Verifies create sends the new optional config fields when provided."""
    client = ProjectClient(mock_rest_client)
    mock_rest_client.post.return_value = sample_project_data

    client.create(
        name="New",
        context="Ctx",
        topic="T",
        optimization_strategy="f_beta",
        openai_llm="gpt-4o",
        gemini_llm="gemini-2.0-flash",
        deepseek_llm="deepseek-chat",
    )

    mock_rest_client.post.assert_called_once_with(
        "/project",
        data={
            "name": "New",
            "context": "Ctx",
            "topic": "T",
            "optimization_strategy": "f_beta",
            "openai_llm": "gpt-4o",
            "gemini_llm": "gemini-2.0-flash",
            "deepseek_llm": "deepseek-chat",
        },
    )


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
    mock_rest_client.put.return_value = sample_project_data
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

    mock_rest_client.put.assert_called_once_with("/project/99", data=payload)
    assert result.id == 1


def test_update_partial(mock_rest_client, sample_project_data):
    """Verifies update only sends the fields the caller provides."""
    client = ProjectClient(mock_rest_client)
    mock_rest_client.put.return_value = sample_project_data

    result = client.update(project_id=99, name="New")

    mock_rest_client.put.assert_called_once_with("/project/99", data={"name": "New"})
    assert result.id == 1


def test_update_status(mock_rest_client, sample_project_data):
    """Verifies update can send the new status field on its own."""
    client = ProjectClient(mock_rest_client)
    mock_rest_client.put.return_value = sample_project_data

    client.update(project_id=99, status="archived")

    mock_rest_client.put.assert_called_once_with(
        "/project/99", data={"status": "archived"}
    )


def test_delete(mock_rest_client):
    """Verifies delete calls post to the delete endpoint."""
    client = ProjectClient(mock_rest_client)

    client.delete(project_id=123)

    mock_rest_client.delete.assert_called_once_with("/project/123")


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


def test_find_one_by_name(mock_rest_client, sample_project_data):
    """Verifies find_one_by_name calls get with the project_name."""
    client = ProjectClient(mock_rest_client)
    mock_rest_client.get.return_value = sample_project_data

    result = client.find_one_by_name("my-project")

    mock_rest_client.get.assert_called_once_with("/project/one-by-name/my-project")
    assert isinstance(result, Project)


def test_find_builds(mock_rest_client, sample_build_data):
    """Verifies find_builds returns a list of ProjectBuild objects."""
    client = ProjectClient(mock_rest_client)
    mock_rest_client.get.return_value = [sample_build_data, sample_build_data]

    result = client.find_builds(1)

    mock_rest_client.get.assert_called_once_with("/project/1/builds")
    assert len(result) == 2
    assert all(isinstance(build, ProjectBuild) for build in result)


def test_find_build(mock_rest_client, sample_build_data):
    """Verifies find_build returns a single ProjectBuild for the build_id."""
    client = ProjectClient(mock_rest_client)
    mock_rest_client.get.return_value = sample_build_data

    result = client.find_build(1, 7)

    mock_rest_client.get.assert_called_once_with("/project/1/builds/7")
    assert isinstance(result, ProjectBuild)
    assert result.id == 7


def test_activate_build(mock_rest_client, sample_build_data):
    """Verifies activate_build puts to the activate endpoint with an empty body."""
    client = ProjectClient(mock_rest_client)
    mock_rest_client.put.return_value = sample_build_data

    result = client.activate_build(1, 7)

    mock_rest_client.put.assert_called_once_with(
        "/project/1/builds/7/activate", data={}
    )
    assert isinstance(result, ProjectBuild)


def test_update_build_notes(mock_rest_client, sample_build_data):
    """Verifies update_build_notes puts the notes payload."""
    client = ProjectClient(mock_rest_client)
    mock_rest_client.put.return_value = sample_build_data

    result = client.update_build_notes(1, 7, "v3 notes")

    mock_rest_client.put.assert_called_once_with(
        "/project/1/builds/7/notes", data={"notes": "v3 notes"}
    )
    assert isinstance(result, ProjectBuild)


def test_update_build_notes_clear(mock_rest_client, sample_build_data):
    """Verifies update_build_notes sends an explicit null to clear the notes."""
    client = ProjectClient(mock_rest_client)
    mock_rest_client.put.return_value = sample_build_data

    client.update_build_notes(1, 7, None)

    mock_rest_client.put.assert_called_once_with(
        "/project/1/builds/7/notes", data={"notes": None}
    )

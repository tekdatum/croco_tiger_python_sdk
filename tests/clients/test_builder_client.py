import pytest
from clients.builder_client import BuilderClient


@pytest.fixture
def mock_rest_client(mocker):
    """Fixture to provide a mocked RestClient."""
    return mocker.Mock()


def test_init(mock_rest_client):
    """Verifies __init__ sets the rest_client and base_path."""
    client = BuilderClient(mock_rest_client)
    assert client._rest_client == mock_rest_client
    assert client.base_path == "/builder"


def test_build(mock_rest_client):
    """Verifies build calls put with correct URL and empty data."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.put.return_value = {True: "Success"}

    result = client.build(123)

    mock_rest_client.put.assert_called_once_with("/builder/build/123", data={})
    assert result == {True: "Success"}


def test_find_project_logs(mock_rest_client):
    """Verifies find_project_logs calls get and returns a list."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = ["log1", "log2"]

    result = client.find_project_logs(123)

    mock_rest_client.get.assert_called_once_with("/builder/logs/123")
    assert result == ["log1", "log2"]


def test_find_project_log_by_name(mock_rest_client):
    """Verifies find_project_log_by_name calls get_file."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get_file.return_value = b"log content"

    result = client.find_project_log_by_name(123, "test.log")

    mock_rest_client.get_file.assert_called_once_with("/builder/log/123/test.log")
    assert result == b"log content"


def test_find_project_accept_list(mock_rest_client):
    """Verifies find_project_accept_list calls get and returns a dict."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = {"item": "allowed"}

    result = client.find_project_accept_list(123)

    mock_rest_client.get.assert_called_once_with("/builder/generated/123/accept_list")
    assert result == {"item": "allowed"}


def test_find_project_reject_list(mock_rest_client):
    """Verifies find_project_reject_list calls get and returns a dict."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = {"item": "blocked"}

    result = client.find_project_reject_list(123)

    mock_rest_client.get.assert_called_once_with("/builder/generated/123/reject_list")
    assert result == {"item": "blocked"}


def test_find_project_testing_metrics(mock_rest_client):
    """Verifies find_project_testing_metrics calls get."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = ["testing_metrics"]

    result = client.find_project_testing_metrics(123)

    mock_rest_client.get.assert_called_once_with("/builder/metrics/testing/123")
    assert result == ["testing_metrics"]


def test_find_project_validation_metrics(mock_rest_client):
    """Verifies find_project_validation_metrics calls get."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = ["validation_metrics"]

    result = client.find_project_validation_metrics(123)

    mock_rest_client.get.assert_called_once_with("/builder/metrics/validation/123")
    assert result == ["validation_metrics"]


def test_find_project_testing_metrics_by_name(mock_rest_client):
    """Verifies find_project_testing_metrics_by_name calls get_file."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get_file.return_value = b"metrics_data"

    result = client.find_project_testing_metrics_by_name(123, "metrics.json")

    mock_rest_client.get_file.assert_called_once_with(
        "/builder/metrics/testing/123/metrics.json"
    )
    assert result == b"metrics_data"


def test_find_project_validation_metrics_by_name(mock_rest_client):
    """Verifies find_project_validation_metrics_by_name calls get_file."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get_file.return_value = b"validation_metrics_data"

    result = client.find_project_validation_metrics_by_name(123, "vmetrics.json")

    mock_rest_client.get_file.assert_called_once_with(
        "/builder/metrics/validation/123/vmetrics.json"
    )
    assert result == b"validation_metrics_data"


def test_find_project_testing_summary(mock_rest_client):
    """Verifies find_project_testing_summary calls get."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = ["testing_summary"]

    result = client.find_project_testing_summary(123)

    mock_rest_client.get.assert_called_once_with("/builder/summary/testing/123")
    assert result == ["testing_summary"]


def test_find_project_validation_summary(mock_rest_client):
    """Verifies find_project_validation_summary calls get."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = ["validation_summary"]

    result = client.find_project_validation_summary(123)

    mock_rest_client.get.assert_called_once_with("/builder/summary/validation/123")
    assert result == ["validation_summary"]

import pytest

from crocotiger.clients.builder_client import BuilderClient


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


def test_build_with_body(mock_rest_client):
    """Verifies build only sends the provided BuildRequest fields."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.put.return_value = {"success": True, "reason": ""}

    result = client.build(123, notes="v2 build", topic="AI")

    mock_rest_client.put.assert_called_once_with(
        "/builder/build/123", data={"notes": "v2 build", "topic": "AI"}
    )
    assert result == {"success": True, "reason": ""}


def test_stop_without_notes(mock_rest_client):
    """Verifies stop calls put with empty body when notes is not provided."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.put.return_value = {"success": True, "reason": ""}

    result = client.stop(123)

    mock_rest_client.put.assert_called_once_with("/builder/stop/123", data={})
    assert result == {"success": True, "reason": ""}


def test_stop_with_notes(mock_rest_client):
    """Verifies stop includes notes in the request body when provided."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.put.return_value = {"success": True, "reason": ""}

    result = client.stop(123, notes="Cancelled — wrong dataset selected")

    mock_rest_client.put.assert_called_once_with(
        "/builder/stop/123",
        data={"notes": "Cancelled — wrong dataset selected"},
    )
    assert result == {"success": True, "reason": ""}


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

    mock_rest_client.get.assert_called_once_with(
        "/builder/generated/123/accept_list", params=None
    )
    assert result == {"item": "allowed"}


def test_find_project_accept_list_with_list_response(mock_rest_client):
    """Verifies find_project_accept_list handles a list payload without TypeError."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = [{"word": "foo"}, {"word": "bar"}]

    result = client.find_project_accept_list(123)

    assert result == [{"word": "foo"}, {"word": "bar"}]


def test_find_project_accept_list_with_build_id(mock_rest_client):
    """Verifies find_project_accept_list passes build_id as a query param."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = {"item": "allowed"}

    result = client.find_project_accept_list(123, build_id=5)

    mock_rest_client.get.assert_called_once_with(
        "/builder/generated/123/accept_list", params={"build_id": 5}
    )
    assert result == {"item": "allowed"}


def test_find_project_reject_list(mock_rest_client):
    """Verifies find_project_reject_list calls get and returns a dict."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = {"item": "blocked"}

    result = client.find_project_reject_list(123)

    mock_rest_client.get.assert_called_once_with(
        "/builder/generated/123/reject_list", params=None
    )
    assert result == {"item": "blocked"}


def test_find_project_reject_list_with_list_response(mock_rest_client):
    """Verifies find_project_reject_list handles a list payload without TypeError."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = [{"word": "spam"}, {"word": "malicious"}]

    result = client.find_project_reject_list(123)

    assert result == [{"word": "spam"}, {"word": "malicious"}]


def test_find_project_reject_list_with_build_id(mock_rest_client):
    """Verifies find_project_reject_list passes build_id as a query param."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = {"item": "blocked"}

    result = client.find_project_reject_list(123, build_id=5)

    mock_rest_client.get.assert_called_once_with(
        "/builder/generated/123/reject_list", params={"build_id": 5}
    )
    assert result == {"item": "blocked"}


def test_find_project_testing_metrics(mock_rest_client):
    """Verifies find_project_testing_metrics calls get."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = ["testing_metrics"]

    result = client.find_project_testing_metrics(123)

    mock_rest_client.get.assert_called_once_with(
        "/builder/metrics/testing/123", params=None
    )
    assert result == ["testing_metrics"]


def test_find_project_testing_metrics_with_build_id(mock_rest_client):
    """Verifies find_project_testing_metrics passes build_id as a query param."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = ["testing_metrics"]

    result = client.find_project_testing_metrics(123, build_id=5)

    mock_rest_client.get.assert_called_once_with(
        "/builder/metrics/testing/123", params={"build_id": 5}
    )
    assert result == ["testing_metrics"]


def test_find_project_validation_metrics(mock_rest_client):
    """Verifies find_project_validation_metrics calls get."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = ["validation_metrics"]

    result = client.find_project_validation_metrics(123)

    mock_rest_client.get.assert_called_once_with(
        "/builder/metrics/validation/123", params=None
    )
    assert result == ["validation_metrics"]


def test_find_project_validation_metrics_with_build_id(mock_rest_client):
    """Verifies find_project_validation_metrics passes build_id as a query param."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = ["validation_metrics"]

    result = client.find_project_validation_metrics(123, build_id=5)

    mock_rest_client.get.assert_called_once_with(
        "/builder/metrics/validation/123", params={"build_id": 5}
    )
    assert result == ["validation_metrics"]


def test_find_project_testing_metrics_by_name(mock_rest_client):
    """Verifies find_project_testing_metrics_by_name calls get_file."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get_file.return_value = b"metrics_data"

    result = client.find_project_testing_metrics_by_name(123, "metrics.json")

    mock_rest_client.get_file.assert_called_once_with(
        "/builder/metrics/testing/123/metrics.json", params=None
    )
    assert result == b"metrics_data"


def test_find_project_testing_metrics_by_name_with_build_id(mock_rest_client):
    """Verifies find_project_testing_metrics_by_name passes build_id."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get_file.return_value = b"metrics_data"

    result = client.find_project_testing_metrics_by_name(
        123, "metrics.json", build_id=5
    )

    mock_rest_client.get_file.assert_called_once_with(
        "/builder/metrics/testing/123/metrics.json", params={"build_id": 5}
    )
    assert result == b"metrics_data"


def test_find_project_validation_metrics_by_name(mock_rest_client):
    """Verifies find_project_validation_metrics_by_name calls get_file."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get_file.return_value = b"validation_metrics_data"

    result = client.find_project_validation_metrics_by_name(123, "vmetrics.json")

    mock_rest_client.get_file.assert_called_once_with(
        "/builder/metrics/validation/123/vmetrics.json", params=None
    )
    assert result == b"validation_metrics_data"


def test_find_project_validation_metrics_by_name_with_build_id(mock_rest_client):
    """Verifies find_project_validation_metrics_by_name passes build_id."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get_file.return_value = b"validation_metrics_data"

    result = client.find_project_validation_metrics_by_name(
        123, "vmetrics.json", build_id=5
    )

    mock_rest_client.get_file.assert_called_once_with(
        "/builder/metrics/validation/123/vmetrics.json", params={"build_id": 5}
    )
    assert result == b"validation_metrics_data"


def test_find_project_testing_summary(mock_rest_client):
    """Verifies find_project_testing_summary calls get."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = ["testing_summary"]

    result = client.find_project_testing_summary(123)

    mock_rest_client.get.assert_called_once_with(
        "/builder/summary/testing/123", params=None
    )
    assert result == ["testing_summary"]


def test_find_project_testing_summary_with_build_id(mock_rest_client):
    """Verifies find_project_testing_summary passes build_id as a query param."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = ["testing_summary"]

    result = client.find_project_testing_summary(123, build_id=5)

    mock_rest_client.get.assert_called_once_with(
        "/builder/summary/testing/123", params={"build_id": 5}
    )
    assert result == ["testing_summary"]


def test_find_project_validation_summary(mock_rest_client):
    """Verifies find_project_validation_summary calls get."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = ["validation_summary"]

    result = client.find_project_validation_summary(123)

    mock_rest_client.get.assert_called_once_with(
        "/builder/summary/validation/123", params=None
    )
    assert result == ["validation_summary"]


def test_find_project_validation_summary_with_build_id(mock_rest_client):
    """Verifies find_project_validation_summary passes build_id as a query param."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.get.return_value = ["validation_summary"]

    result = client.find_project_validation_summary(123, build_id=5)

    mock_rest_client.get.assert_called_once_with(
        "/builder/summary/validation/123", params={"build_id": 5}
    )
    assert result == ["validation_summary"]


def test_quick_build_without_notes(mock_rest_client):
    """Verifies quick_build calls put with empty body when notes is not provided."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.put.return_value = {
        "success": True,
        "reason": "Quick build started",
    }

    result = client.quick_build(123)

    mock_rest_client.put.assert_called_once_with("/builder/quick-build/123", data={})
    assert result == {"success": True, "reason": "Quick build started"}


def test_quick_build_with_notes(mock_rest_client):
    """Verifies quick_build includes notes in the request body when provided."""
    client = BuilderClient(mock_rest_client)
    mock_rest_client.put.return_value = {
        "success": True,
        "reason": "Quick build started",
    }

    result = client.quick_build(
        123, notes="Refreshing benchmarks after threshold adjustment"
    )

    mock_rest_client.put.assert_called_once_with(
        "/builder/quick-build/123",
        data={"notes": "Refreshing benchmarks after threshold adjustment"},
    )
    assert result == {"success": True, "reason": "Quick build started"}

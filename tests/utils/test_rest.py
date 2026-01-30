import pytest
import requests
from utils.rest import RestClient  # Adjust based on your file structure


def test_init():
    """Verifies that __init__ correctly sets base_path and default headers."""
    client = RestClient("http://api.com/")
    assert client.base_path == "http://api.com"
    assert client.headers["Content-Type"] == "application/json"
    assert client.headers["Accept"] == "application/json"


def test_prepare_url():
    """Verifies that _prepare_url handles leading and trailing slashes."""
    client = RestClient("http://api.com/")
    url = client._prepare_url("/users")
    assert url == "http://api.com/users"


def test_handle_response_success_with_data(mocker):
    """Verifies that _handle_response extracts the 'data' key when present."""
    client = RestClient("http://api.com")
    mock_response = mocker.Mock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 1}, "status": "ok"}

    result = client._handle_response(mock_response)
    assert result == {"id": 1}


def test_handle_response_success_no_data(mocker):
    """Verifies that _handle_response returns the whole JSON if 'data' is missing."""
    client = RestClient("http://api.com")
    mock_response = mocker.Mock(spec=requests.Response)
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 1}

    result = client._handle_response(mock_response)
    assert result == {"id": 1}


def test_handle_response_api_error_json(mocker):
    """Verifies that _handle_response raises an Exception with JSON error details."""
    client = RestClient("http://api.com")
    mock_response = mocker.Mock(spec=requests.Response)
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": "bad request"}

    with pytest.raises(Exception) as excinfo:
        client._handle_response(mock_response)
    assert "API Error 400" in str(excinfo.value)
    assert "bad request" in str(excinfo.value)


def test_handle_response_api_error_not_json(mocker):
    """
    Verifies that _handle_response falls back to
    raise_for_status for non-JSON errors.
    """
    client = RestClient("http://api.com")
    mock_response = mocker.Mock(spec=requests.Response)
    mock_response.status_code = 500
    # Simulate JSON decoding failure
    mock_response.json.side_effect = ValueError("No JSON")

    client._handle_response(mock_response)
    mock_response.raise_for_status.assert_called_once()


def test_get(mocker):
    """Verifies the GET method calls requests.get with correct params."""
    client = RestClient("http://api.com")
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"data": "ok"}

    result = client.get("/test", params={"q": 1})

    mock_get.assert_called_once_with(
        "http://api.com/test", headers=client.headers, params={"q": 1}
    )
    assert result == "ok"


def test_get_file(mocker):
    """Verifies the get_file method returns the raw content bytes."""
    client = RestClient("http://api.com")
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.content = b"raw_data"

    result = client.get_file("/download")

    assert result == b"raw_data"
    mock_get.assert_called_once()


def test_post(mocker):
    """Verifies the POST method calls requests.post with json data."""
    client = RestClient("http://api.com")
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"data": "created"}

    result = client.post("/test", data={"name": "new"})

    mock_post.assert_called_once_with(
        "http://api.com/test", headers=client.headers, json={"name": "new"}
    )
    assert result == "created"


def test_put(mocker):
    """Verifies the PUT method calls requests.put with json data."""
    client = RestClient("http://api.com")
    mock_put = mocker.patch("requests.put")
    mock_put.return_value.status_code = 200
    mock_put.return_value.json.return_value = {"data": "updated"}

    result = client.put("/test", data={"id": 1})

    mock_put.assert_called_once_with(
        "http://api.com/test", headers=client.headers, json={"id": 1}
    )
    assert result == "updated"


def test_delete(mocker):
    """Verifies the DELETE method calls requests.delete."""
    client = RestClient("http://api.com")
    mock_delete = mocker.patch("requests.delete")
    mock_delete.return_value.status_code = 204
    mock_delete.return_value.json.return_value = {"status": "deleted"}

    result = client.delete("/test/1")

    mock_delete.assert_called_once_with("http://api.com/test/1", headers=client.headers)
    assert result == {"status": "deleted"}

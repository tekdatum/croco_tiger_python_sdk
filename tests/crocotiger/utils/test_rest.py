import pytest
import requests

from crocotiger.models.error import ApiErrorResponse
from crocotiger.utils.rest import RestClient  # Adjust based on your file structure


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


def test_handle_response_null_json_body(mocker):
    """Verifies _handle_response handles a 200 with a null body without TypeError."""
    client = RestClient("http://api.com")
    mock_response = mocker.Mock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = None

    result = client._handle_response(mock_response)
    assert result is None


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
    mock_response.reason = "Bad Request"
    mock_response.json.return_value = {"status": "fail", "message": "invalid input"}

    with pytest.raises(ApiErrorResponse) as excinfo:
        client._handle_response(mock_response)

    assert excinfo.value.code == 400
    assert excinfo.value.status == "fail"
    assert "invalid input" in excinfo.value.message
    assert str(excinfo.value) == "<ApiErrorResponse 400: invalid input>"


def test_handle_response_api_error_not_json(mocker):
    """
    Verifies that _handle_response falls back to
    raise_for_status for non-JSON errors.
    """
    client = RestClient("http://api.com")
    mock_response = mocker.Mock(spec=requests.Response)
    mock_response.status_code = 500
    mock_response.reason = "Internal Server Error"
    mock_response.text = "Internal server error in plain text"
    mock_response.json.side_effect = ValueError("No JSON")

    with pytest.raises(ApiErrorResponse) as excinfo:
        client._handle_response(mock_response)

    assert excinfo.value.code == 500
    assert excinfo.value.message == "Internal server error in plain text"
    assert excinfo.value.details == {"message": "Internal server error in plain text"}


def test_add_authorization_token(mocker):
    """Verifies add_authorization_token injects the Bearer header."""
    client = RestClient("http://api.com")

    client.add_authorization_token("my-jwt-token")

    assert client.headers["Authorization"] == "Bearer my-jwt-token"


def test_remove_authorization_token():
    """Verifies remove_authorization_token strips the Bearer header."""
    client = RestClient("http://api.com")
    client.add_authorization_token("my-jwt-token")

    client.remove_authorization_token()

    assert "Authorization" not in client.headers


def test_remove_authorization_token_when_absent_is_noop():
    """Verifies remove_authorization_token is safe when no token was set."""
    client = RestClient("http://api.com")

    client.remove_authorization_token()

    assert "Authorization" not in client.headers


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
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = b"raw_data"

    result = client.get_file("/download")

    assert result == b"raw_data"
    mock_get.assert_called_once()


def test_get_file_raises_on_error(mocker):
    """Verifies get_file raises ApiErrorResponse on error, not raw bytes."""
    client = RestClient("http://api.com")
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.status_code = 404
    mock_get.return_value.json.return_value = {"status": "fail", "message": "not found"}

    with pytest.raises(ApiErrorResponse):
        client.get_file("/missing-file")


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


def test_upload_file_keeps_auth_and_drops_content_type(mocker, tmp_path):
    """Verifies upload_file keeps the auth header but drops Content-Type so
    requests can set the multipart/form-data boundary itself."""
    client = RestClient("http://api.com")
    client.add_authorization_token("my-jwt-token")
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"data": {"name": "data.zip"}}

    zip_file = tmp_path / "data.zip"
    zip_file.write_bytes(b"PK\x03\x04")

    result = client.upload_file("/upload", str(zip_file), params={"rewrite": "true"})

    assert result == {"name": "data.zip"}
    args, kwargs = mock_post.call_args
    assert args[0] == "http://api.com/upload"
    assert kwargs["headers"]["Authorization"] == "Bearer my-jwt-token"
    assert kwargs["headers"]["Accept"] == "application/json"
    assert "Content-Type" not in kwargs["headers"]
    assert "file" in kwargs["files"]
    assert kwargs["params"] == {"rewrite": "true"}
    # the original client headers must be left intact for other (JSON) calls
    assert client.headers["Content-Type"] == "application/json"

import pytest

from crocotiger.clients.auth_client import AuthClient


@pytest.fixture
def mock_rest_client(mocker):
    """Fixture to provide a mocked RestClient."""
    return mocker.Mock()


def test_init(mock_rest_client):
    """Verifies __init__ sets the rest_client and internal endpoint."""
    client = AuthClient(mock_rest_client)
    assert client._rest_client == mock_rest_client
    assert client._endpoint == "/auth"


def test_authenticate_returns_token(mock_rest_client):
    """Verifies authenticate POSTs to sign-in and returns the token."""
    client = AuthClient(mock_rest_client)
    mock_rest_client.post.return_value = {"token": "my-jwt-token"}

    token = client.authenticate("my-passphrase")

    mock_rest_client.post.assert_called_once_with(
        "/auth/sign-in", data={"passphrase": "my-passphrase"}
    )
    assert token == "my-jwt-token"


def test_reset_passphrase(mock_rest_client):
    """Verifies reset_passphrase POSTs old and new passphrases to the endpoint."""
    client = AuthClient(mock_rest_client)

    client.reset_passphrase("old-pass", "new-pass")

    mock_rest_client.post.assert_called_once_with(
        "/auth/reset-passphrase",
        data={"old_passphrase": "old-pass", "new_passphrase": "new-pass"},
    )

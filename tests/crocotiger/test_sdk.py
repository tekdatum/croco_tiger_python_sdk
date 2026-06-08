import pytest

from crocotiger.sdk import SDK


@pytest.fixture
def mock_rest(mocker):
    return mocker.patch("crocotiger.sdk.RestClient")


@pytest.fixture
def mock_auth_client(mocker):
    return mocker.patch("crocotiger.sdk.AuthClient")


class TestSDK:
    def test_sdk_initialization_without_passphrase(self, mock_rest) -> None:
        # Act
        SDK()

        # Assert
        mock_rest.assert_called_once_with("http://localhost:8090/api/v1/")
        mock_rest.return_value.add_authorization_token.assert_not_called()

    def test_sdk_initialization_with_passphrase(
        self, mock_rest, mock_auth_client
    ) -> None:
        # Arrange
        mock_auth_client.return_value.authenticate.return_value = "jwt-token"

        # Act
        SDK(passphrase="my-pass")

        # Assert
        mock_auth_client.assert_called_once_with(mock_rest.return_value)
        mock_auth_client.return_value.authenticate.assert_called_once_with("my-pass")
        mock_rest.return_value.add_authorization_token.assert_called_once_with(
            "jwt-token"
        )

    def test_authenticate(self, mock_rest, mock_auth_client) -> None:
        # Arrange
        mock_auth_client.return_value.authenticate.return_value = "jwt-token"
        sdk = SDK()

        # Act
        sdk.authenticate("my-pass")

        # Assert
        mock_auth_client.return_value.authenticate.assert_called_once_with("my-pass")
        mock_rest.return_value.add_authorization_token.assert_called_once_with(
            "jwt-token"
        )

    def test_get_auth_client(self, mock_rest, mock_auth_client) -> None:
        # Arrange
        sdk = SDK()

        # Act
        client = sdk.get_auth_client()

        # Assert
        mock_auth_client.assert_called_once_with(sdk._rest_client)
        assert client == mock_auth_client.return_value

    def test_get_project_client(self, mock_rest, mocker) -> None:
        # Arrange
        mock_client_class = mocker.patch("crocotiger.sdk.ProjectClient")
        sdk = SDK()

        # Act
        client = sdk.get_project_client()

        # Assert
        mock_client_class.assert_called_once_with(sdk._rest_client)
        assert client == mock_client_class.return_value

    def test_get_custom_settings_client(self, mock_rest, mocker) -> None:
        # Arrange
        mock_client_class = mocker.patch("crocotiger.sdk.CustomSettingsClient")
        sdk = SDK()

        # Act
        client = sdk.get_custom_settings_client()

        # Assert
        mock_client_class.assert_called_once_with(sdk._rest_client)
        assert client == mock_client_class.return_value

    def test_get_builder_client(self, mock_rest, mocker) -> None:
        # Arrange
        mock_client_class = mocker.patch("crocotiger.sdk.BuilderClient")
        sdk = SDK()

        # Act
        client = sdk.get_builder_client()

        # Assert
        mock_client_class.assert_called_once_with(sdk._rest_client)
        assert client == mock_client_class.return_value

    def test_get_fence_client(self, mock_rest, mocker) -> None:
        # Arrange
        mock_client_class = mocker.patch("crocotiger.sdk.FenceClient")
        sdk = SDK()

        # Act
        client = sdk.get_fence_client()

        # Assert
        mock_client_class.assert_called_once_with(sdk._rest_client)
        assert client == mock_client_class.return_value

    def test_get_ip_management_client(self, mock_rest, mocker) -> None:
        # Arrange
        mock_client_class = mocker.patch("crocotiger.sdk.IPManagementClient")
        sdk = SDK()

        # Act
        client = sdk.get_ip_management_client()

        # Assert
        mock_client_class.assert_called_once_with(sdk._rest_client)
        assert client == mock_client_class.return_value

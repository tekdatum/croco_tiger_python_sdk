import pytest

from crocotiger.sdk import SDK


@pytest.fixture
def mock_rest(mocker):
    return mocker.patch("crocotiger.sdk.RestClient")


class TestSDK:
    def test_sdk_initialization(self, mock_rest) -> None:
        # Arrange
        custom_base = "https://api.example.com/v1/"
        passphrase = "test-pass"

        # Act
        sdk = SDK(base_path=custom_base, passphrase=passphrase)

        # Assert
        assert sdk.base_path == custom_base
        mock_rest.assert_called_once_with(custom_base)
        mock_rest.return_value.authenticate.assert_called_once_with(passphrase)

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

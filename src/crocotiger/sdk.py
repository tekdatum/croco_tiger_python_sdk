from typing import Optional

from crocotiger.clients.auth_client import AuthClient
from crocotiger.clients.builder_client import BuilderClient
from crocotiger.clients.custom_settings_client import CustomSettingsClient
from crocotiger.clients.fence_client import FenceClient
from crocotiger.clients.project_client import ProjectClient
from crocotiger.utils.rest import RestClient


class SDK:
    def __init__(
        self,
        base_path: str = "http://localhost:8090/api/v1/",
        passphrase: Optional[str] = None,
    ):
        self.base_path = base_path
        self._rest_client = RestClient(base_path)
        if passphrase is not None:
            self.authenticate(passphrase)

    def authenticate(self, passphrase: str) -> None:
        token = AuthClient(self._rest_client).authenticate(passphrase)
        self._rest_client.add_authorization_token(token)

    def get_auth_client(self) -> AuthClient:
        return AuthClient(self._rest_client)

    def get_project_client(self) -> ProjectClient:
        return ProjectClient(self._rest_client)

    def get_custom_settings_client(self) -> CustomSettingsClient:
        return CustomSettingsClient(self._rest_client)

    def get_builder_client(self) -> BuilderClient:
        return BuilderClient(self._rest_client)

    def get_fence_client(self) -> FenceClient:
        return FenceClient(self._rest_client)

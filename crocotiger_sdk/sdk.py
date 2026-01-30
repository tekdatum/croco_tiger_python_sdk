from clients.project_client import ProjectClient
from clients.custom_settings_client import CustomSettingsClient
from clients.builder_client import BuilderClient
from clients.fence_client import FenceClient

from utils.rest import RestClient


class SDK:
    def __init__(self, base_path: str = "http://localhost:8090/api/v1/"):
        self.base_path = base_path
        self._rest_client = RestClient(base_path)

    def get_project_client(self) -> ProjectClient:
        return ProjectClient(self._rest_client)

    def get_custom_settings_client(self) -> CustomSettingsClient:
        return CustomSettingsClient(self._rest_client)

    def get_builder_client(self) -> BuilderClient:
        return BuilderClient(self._rest_client)
    
    def get_fence_client(self) -> FenceClient:
        return FenceClient(self._rest_client)

    # getters for other clients can be added here

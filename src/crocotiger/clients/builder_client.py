from typing import Any
from crocotiger.utils.rest import RestClient


class BuilderClient:
    def __init__(self, rest_client: RestClient):
        self._rest_client = rest_client
        self.base_path = "/builder"

    def build(self, project_id: int) -> dict[bool, str]:
        data = self._rest_client.put(f"{self.base_path}/build/{project_id}", data={})
        return dict(data)

    def find_project_logs(self, project_id: int) -> list[str]:
        data = self._rest_client.get(f"{self.base_path}/logs/{project_id}")
        return list(data)

    def find_project_log_by_name(self, project_id: int, file_name: str) -> bytes:
        data = self._rest_client.get_file(
            f"{self.base_path}/log/{project_id}/{file_name}"
        )
        return data

    def find_project_accept_list(self, project_id: int) -> dict[str, Any]:
        data = self._rest_client.get(
            f"{self.base_path}/generated/{project_id}/accept_list"
        )
        return dict(data)

    def find_project_reject_list(self, project_id: int) -> dict[str, Any]:
        data = self._rest_client.get(
            f"{self.base_path}/generated/{project_id}/reject_list"
        )
        return dict(data)

    def find_project_testing_metrics(self, project_id: int) -> list[str]:
        data = self._rest_client.get(f"{self.base_path}/metrics/testing/{project_id}")
        return list(data)

    def find_project_validation_metrics(self, project_id: int) -> list[str]:
        data = self._rest_client.get(
            f"{self.base_path}/metrics/validation/{project_id}"
        )
        return list(data)

    def find_project_testing_metrics_by_name(
        self, project_id: int, file_name: str
    ) -> bytes:
        data = self._rest_client.get_file(
            f"{self.base_path}/metrics/testing/{project_id}/{file_name}"
        )
        return data

    def find_project_validation_metrics_by_name(
        self, project_id: int, file_name: str
    ) -> bytes:
        data = self._rest_client.get_file(
            f"{self.base_path}/metrics/validation/{project_id}/{file_name}"
        )
        return data

    def find_project_testing_summary(self, project_id: int) -> list[str]:
        data = self._rest_client.get(f"{self.base_path}/summary/testing/{project_id}")
        return list(data)

    def find_project_validation_summary(self, project_id: int) -> list[str]:
        data = self._rest_client.get(
            f"{self.base_path}/summary/validation/{project_id}"
        )
        return list(data)

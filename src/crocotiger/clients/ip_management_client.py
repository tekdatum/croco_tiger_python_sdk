from typing import Any

from crocotiger.enums.geo_block_type import GeoBlockType
from crocotiger.models.geo_block import GeoBlock
from crocotiger.models.ip_block import IPBlock
from crocotiger.utils.rest import RestClient


class IPManagementClient:
    def __init__(self, rest_client: RestClient):
        self._rest_client = rest_client
        self._endpoint = "/ip-management"

    def list_ips(self, project_id: int) -> list[dict[str, Any]]:
        data = self._rest_client.get(f"{self._endpoint}/{project_id}/ips")
        return list(data)

    def list_blocked_ips(self, project_id: int) -> list[IPBlock]:
        data = self._rest_client.get(f"{self._endpoint}/{project_id}/blocked")
        return [IPBlock(**item) for item in data]

    def block_ip(self, project_id: int, ip_address: str) -> IPBlock:
        data = self._rest_client.post(
            f"{self._endpoint}/{project_id}/block",
            data={"ip_address": ip_address},
        )
        return IPBlock(**data)

    def unblock_ip(self, project_id: int, ip_address: str) -> None:
        self._rest_client.delete(f"{self._endpoint}/{project_id}/block/{ip_address}")

    def list_regions(self, project_id: int) -> list[dict[str, Any]]:
        data = self._rest_client.get(f"{self._endpoint}/{project_id}/regions")
        return list(data)

    def list_geo_blocks(self, project_id: int) -> list[GeoBlock]:
        data = self._rest_client.get(f"{self._endpoint}/{project_id}/geo-blocks")
        return [GeoBlock(**item) for item in data]

    def create_geo_block(
        self,
        project_id: int,
        block_type: GeoBlockType,
        value: str,
        country_code: str | None = None,
    ) -> GeoBlock:
        payload: dict[str, Any] = {
            "block_type": block_type.value,
            "value": value,
            "country_code": country_code,
        }
        data = self._rest_client.post(
            f"{self._endpoint}/{project_id}/geo-blocks",
            data=payload,
        )
        return GeoBlock(**data)

    def delete_geo_block(self, project_id: int, entry_id: int) -> None:
        self._rest_client.delete(f"{self._endpoint}/{project_id}/geo-blocks/{entry_id}")

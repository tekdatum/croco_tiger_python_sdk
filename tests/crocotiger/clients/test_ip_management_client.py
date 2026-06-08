import pytest

from crocotiger.clients.ip_management_client import IPManagementClient
from crocotiger.enums.geo_block_type import GeoBlockType
from crocotiger.models.geo_block import GeoBlock
from crocotiger.models.ip_block import IPBlock

PROJECT_ID = 42

IP_BLOCK_DATA = {
    "id": 1,
    "project_id": PROJECT_ID,
    "ip_address": "1.2.3.4",
    "blocked_at": "2024-01-01T00:00:00",
}

GEO_BLOCK_COUNTRY_DATA = {
    "id": 10,
    "project_id": PROJECT_ID,
    "block_type": "country",
    "value": "CN",
    "country_code": None,
    "blocked_at": "2024-01-01T00:00:00",
}

GEO_BLOCK_CITY_DATA = {
    "id": 11,
    "project_id": PROJECT_ID,
    "block_type": "city",
    "value": "Miami",
    "country_code": "US",
    "blocked_at": "2024-01-01T00:00:00",
}


@pytest.fixture
def mock_rest_client(mocker):
    return mocker.Mock()


def test_init(mock_rest_client):
    client = IPManagementClient(mock_rest_client)
    assert client._rest_client == mock_rest_client
    assert client._endpoint == "/ip-management"


def test_list_ips(mock_rest_client):
    client = IPManagementClient(mock_rest_client)
    raw = [{"ip_address": "1.2.3.4", "is_blocked": True, "request_count": 5}]
    mock_rest_client.get.return_value = raw

    result = client.list_ips(PROJECT_ID)

    assert result == raw
    mock_rest_client.get.assert_called_once_with(f"/ip-management/{PROJECT_ID}/ips")


def test_list_blocked_ips(mock_rest_client):
    client = IPManagementClient(mock_rest_client)
    mock_rest_client.get.return_value = [IP_BLOCK_DATA]

    result = client.list_blocked_ips(PROJECT_ID)

    assert len(result) == 1
    assert isinstance(result[0], IPBlock)
    assert result[0].ip_address == "1.2.3.4"
    mock_rest_client.get.assert_called_once_with(f"/ip-management/{PROJECT_ID}/blocked")


def test_block_ip(mock_rest_client):
    client = IPManagementClient(mock_rest_client)
    mock_rest_client.post.return_value = IP_BLOCK_DATA

    result = client.block_ip(PROJECT_ID, "1.2.3.4")

    assert isinstance(result, IPBlock)
    assert result.ip_address == "1.2.3.4"
    assert result.project_id == PROJECT_ID
    mock_rest_client.post.assert_called_once_with(
        f"/ip-management/{PROJECT_ID}/block",
        data={"ip_address": "1.2.3.4"},
    )


def test_unblock_ip(mock_rest_client):
    client = IPManagementClient(mock_rest_client)

    client.unblock_ip(PROJECT_ID, "1.2.3.4")

    mock_rest_client.delete.assert_called_once_with(
        f"/ip-management/{PROJECT_ID}/block/1.2.3.4"
    )


def test_list_regions(mock_rest_client):
    client = IPManagementClient(mock_rest_client)
    raw = [{"country": "China", "country_code": "CN", "request_count": 100, "is_blocked": True}]
    mock_rest_client.get.return_value = raw

    result = client.list_regions(PROJECT_ID)

    assert result == raw
    mock_rest_client.get.assert_called_once_with(f"/ip-management/{PROJECT_ID}/regions")


def test_list_geo_blocks(mock_rest_client):
    client = IPManagementClient(mock_rest_client)
    mock_rest_client.get.return_value = [GEO_BLOCK_COUNTRY_DATA, GEO_BLOCK_CITY_DATA]

    result = client.list_geo_blocks(PROJECT_ID)

    assert len(result) == 2
    assert all(isinstance(item, GeoBlock) for item in result)
    assert result[0].block_type == GeoBlockType.COUNTRY
    assert result[1].block_type == GeoBlockType.CITY
    mock_rest_client.get.assert_called_once_with(
        f"/ip-management/{PROJECT_ID}/geo-blocks"
    )


def test_create_geo_block_country(mock_rest_client):
    client = IPManagementClient(mock_rest_client)
    mock_rest_client.post.return_value = GEO_BLOCK_COUNTRY_DATA

    result = client.create_geo_block(PROJECT_ID, GeoBlockType.COUNTRY, "CN")

    assert isinstance(result, GeoBlock)
    assert result.block_type == GeoBlockType.COUNTRY
    assert result.value == "CN"
    assert result.country_code is None
    mock_rest_client.post.assert_called_once_with(
        f"/ip-management/{PROJECT_ID}/geo-blocks",
        data={"block_type": "country", "value": "CN", "country_code": None},
    )


def test_create_geo_block_city(mock_rest_client):
    client = IPManagementClient(mock_rest_client)
    mock_rest_client.post.return_value = GEO_BLOCK_CITY_DATA

    result = client.create_geo_block(PROJECT_ID, GeoBlockType.CITY, "Miami", "US")

    assert isinstance(result, GeoBlock)
    assert result.block_type == GeoBlockType.CITY
    assert result.value == "Miami"
    assert result.country_code == "US"
    mock_rest_client.post.assert_called_once_with(
        f"/ip-management/{PROJECT_ID}/geo-blocks",
        data={"block_type": "city", "value": "Miami", "country_code": "US"},
    )


def test_delete_geo_block(mock_rest_client):
    client = IPManagementClient(mock_rest_client)

    client.delete_geo_block(PROJECT_ID, 10)

    mock_rest_client.delete.assert_called_once_with(
        f"/ip-management/{PROJECT_ID}/geo-blocks/10"
    )

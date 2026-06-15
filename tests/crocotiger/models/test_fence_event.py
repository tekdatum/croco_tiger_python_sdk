import pytest

from datetime import datetime

from crocotiger.models.fence_event import FenceEvent, FenceEventPage


FULL_EVENT = {
    "id": 1,
    "project_id": 42,
    "text": "texto validado",
    "valid": True,
    "reason_code": "accepted",
    "accept_score": 0.92,
    "accept_anomaly_score": 0.05,
    "accepted_nearest_neighbor": "ejemplo vecino",
    "accepted_nearest_neighbor_category": "categoria",
    "reject_score": 0.08,
    "reject_anomaly_score": 0.03,
    "rejected_nearest_neighbor": None,
    "rejected_nearest_neighbor_category": None,
    "ip_address": "192.168.1.1",
    "device_type": "desktop",
    "duration": 0.134,
    "timestamp": "2026-06-10T14:00:00",
}


class TestFenceEvent:
    def test_valid_event(self):
        event = FenceEvent(**FULL_EVENT)
        assert event.id == 1
        assert event.project_id == 42
        assert event.valid is True
        assert event.accept_score == 0.92
        assert event.rejected_nearest_neighbor is None
        assert isinstance(event.timestamp, datetime)

    def test_nullable_fields_accept_none(self):
        data = {**FULL_EVENT, "ip_address": None, "device_type": None}
        event = FenceEvent(**data)
        assert event.ip_address is None
        assert event.device_type is None

    def test_missing_required_field_raises(self):
        data = {k: v for k, v in FULL_EVENT.items() if k != "text"}
        with pytest.raises(Exception):
            FenceEvent(**data)


class TestFenceEventPage:
    def test_valid_page(self):
        page = FenceEventPage(total=1, offset=0, limit=50, data=[FULL_EVENT])
        assert page.total == 1
        assert page.offset == 0
        assert page.limit == 50
        assert len(page.data) == 1
        assert isinstance(page.data[0], FenceEvent)

    def test_empty_page(self):
        page = FenceEventPage(total=0, offset=0, limit=50, data=[])
        assert page.total == 0
        assert page.data == []

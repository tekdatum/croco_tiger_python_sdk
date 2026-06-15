from datetime import datetime

from pydantic import BaseModel


class FenceEvent(BaseModel):
    id: int
    project_id: int
    text: str
    valid: bool
    reason_code: str
    accept_score: float
    accept_anomaly_score: float
    accepted_nearest_neighbor: str | None
    accepted_nearest_neighbor_category: str | None
    reject_score: float
    reject_anomaly_score: float
    rejected_nearest_neighbor: str | None
    rejected_nearest_neighbor_category: str | None
    ip_address: str | None
    device_type: str | None
    duration: float
    timestamp: datetime


class FenceEventPage(BaseModel):
    total: int
    offset: int
    limit: int
    data: list[FenceEvent]

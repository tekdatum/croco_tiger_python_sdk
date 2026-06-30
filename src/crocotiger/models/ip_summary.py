from datetime import datetime

from pydantic import BaseModel


class IPLocation(BaseModel):
    country: str | None = None
    country_code: str | None = None
    city: str | None = None
    isp: str | None = None


class IPSummary(BaseModel):
    ip_address: str
    total_requests: int
    fence_accepted_count: int = 0
    fence_rejected_count: int = 0
    last_seen: datetime | None = None
    is_blocked: bool
    is_geo_blocked: bool
    ip_blocked_count: int
    region_blocked_count: int
    location: IPLocation | None = None

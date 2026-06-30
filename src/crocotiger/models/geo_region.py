from pydantic import BaseModel


class GeoCountrySummary(BaseModel):
    country_code: str | None = None
    country: str | None = None
    total_requests: int
    fence_accepted_count: int = 0
    fence_rejected_count: int = 0
    is_blocked: bool
    ip_blocked_count: int
    region_blocked_count: int


class GeoCitySummary(BaseModel):
    country_code: str | None = None
    city: str | None = None
    country: str | None = None
    total_requests: int
    fence_accepted_count: int = 0
    fence_rejected_count: int = 0
    is_blocked: bool
    ip_blocked_count: int
    region_blocked_count: int


class GeoRegionsSummary(BaseModel):
    countries: list[GeoCountrySummary] = []
    cities: list[GeoCitySummary] = []

from datetime import datetime

from pydantic import BaseModel

from crocotiger.enums.geo_block_type import GeoBlockType


class GeoBlock(BaseModel):
    id: int
    project_id: int
    block_type: GeoBlockType
    value: str
    country_code: str | None = None
    blocked_at: datetime

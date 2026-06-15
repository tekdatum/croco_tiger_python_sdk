from datetime import datetime

from pydantic import BaseModel


class IPBlock(BaseModel):
    id: int
    project_id: int
    ip_address: str
    blocked_at: datetime

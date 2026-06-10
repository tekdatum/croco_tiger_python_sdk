from typing import Any

from pydantic import BaseModel


class FenceValidation(BaseModel):
    text: str
    valid: bool
    reason_code: str
    category: str | None = None
    duration: float
    extra: dict[str, Any] = {}

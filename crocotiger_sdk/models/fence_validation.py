from pydantic import BaseModel


class FenceValidation(BaseModel):
    text: str
    valid: bool
    reason_code: str
    duration: float

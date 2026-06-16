from pydantic import BaseModel


class FenceCorrection(BaseModel):
    text: str
    valid: bool
    category: str | None = None

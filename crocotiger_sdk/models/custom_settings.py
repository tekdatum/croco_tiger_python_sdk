from pydantic import BaseModel
from datetime import datetime


class CustomSettings(BaseModel):
    id: int | None = None
    openai_key: str | None = None
    gemini_key: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    @property
    def trimmed_openai_key(self) -> str | None:
        return self.openai_key[-4:] if self.openai_key is not None else None

    @property
    def trimmed_gemini_key(self) -> str | None:
        return self.gemini_key[-4:] if self.gemini_key is not None else None

    def is_invalid(self) -> bool:
        return self.openai_key is None and self.gemini_key is None

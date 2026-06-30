from pydantic import BaseModel, field_validator


class LLMModel(BaseModel):
    model: str
    label: str
    message: str | None = None
    recommended: bool = False


class LLMModels(BaseModel):
    openai: list[LLMModel] = []
    gemini: list[LLMModel] = []
    deepseek: list[LLMModel] = []

    @field_validator("openai", "gemini", "deepseek", mode="before")
    @classmethod
    def _none_to_empty(cls, value: object) -> object:
        """The catalog may send a provider list as null (e.g. ``deepseek`` for
        backward compatibility); treat it as an empty list."""
        return value if value is not None else []

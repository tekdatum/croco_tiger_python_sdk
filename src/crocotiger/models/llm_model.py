from pydantic import BaseModel


class LLMModel(BaseModel):
    model: str
    label: str
    message: str | None = None
    recommended: bool = False


class LLMModels(BaseModel):
    openai: list[LLMModel] = []
    gemini: list[LLMModel] = []

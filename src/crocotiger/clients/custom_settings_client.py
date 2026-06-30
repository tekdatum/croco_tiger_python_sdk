from crocotiger.models.custom_settings import CustomSettings
from crocotiger.utils.rest import RestClient


class CustomSettingsClient:
    def __init__(self, rest_client: RestClient):
        self._rest_client = rest_client
        self.base_path = "/custom-settings"

    def find_custom_settings(self) -> CustomSettings:
        data = self._rest_client.get(f"{self.base_path}")
        return CustomSettings(**data)

    def update_custom_settings(
        self,
        openai_key: str | None = None,
        gemini_key: str | None = None,
        deepseek_key: str | None = None,
        otlp_endpoint: str | None = None,
    ) -> CustomSettings:
        """Set one or more settings. Fields left as None are omitted from the
        payload and remain unchanged server-side; at least one field must be
        provided (the server rejects an empty payload with 422)."""
        candidate = {
            "openai_key": openai_key,
            "gemini_key": gemini_key,
            "deepseek_key": deepseek_key,
            "otlp_endpoint": otlp_endpoint,
        }
        payload = {k: v for k, v in candidate.items() if v is not None}
        data = self._rest_client.put(f"{self.base_path}", data=payload)
        return CustomSettings(**data)

    def clear_llms_keys(self) -> CustomSettings | None:
        """Clear all three LLM API keys (OpenAI, Gemini, DeepSeek) at once."""
        data = self._rest_client.put(f"{self.base_path}/clear-keys", data={})
        if data is None:
            return None
        return CustomSettings(**data)

    def delete_openai_key(self) -> CustomSettings | None:
        data = self._rest_client.delete(f"{self.base_path}/openai-key")
        if data is None:
            return None
        return CustomSettings(**data)

    def delete_gemini_key(self) -> CustomSettings | None:
        data = self._rest_client.delete(f"{self.base_path}/gemini-key")
        if data is None:
            return None
        return CustomSettings(**data)

    def delete_deepseek_key(self) -> CustomSettings | None:
        data = self._rest_client.delete(f"{self.base_path}/deepseek-key")
        if data is None:
            return None
        return CustomSettings(**data)

    def delete_otlp_endpoint(self) -> CustomSettings | None:
        data = self._rest_client.delete(f"{self.base_path}/otlp-endpoint")
        if data is None:
            return None
        return CustomSettings(**data)

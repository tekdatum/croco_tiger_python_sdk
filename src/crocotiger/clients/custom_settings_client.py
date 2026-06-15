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
    ) -> CustomSettings:
        """Set one or more keys. Keys left as None are omitted from the payload
        and remain unchanged server-side; at least one key must be provided."""
        candidate = {
            "openai_key": openai_key,
            "gemini_key": gemini_key,
        }
        payload = {k: v for k, v in candidate.items() if v is not None}
        data = self._rest_client.put(f"{self.base_path}", data=payload)
        return CustomSettings(**data)

    def clear_llms_keys(self) -> CustomSettings | None:
        data = self._rest_client.put(f"{self.base_path}/clear-keys", data={})
        if data is None:
            return None
        return CustomSettings(**data)

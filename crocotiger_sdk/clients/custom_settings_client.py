from crocotiger_sdk.models.custom_settings import CustomSettings
from crocotiger_sdk.utils.rest import RestClient


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
        payload = {
            "openai_key": openai_key,
            "gemini_key": gemini_key,
        }
        data = self._rest_client.put(f"{self.base_path}", data=payload)
        return CustomSettings(**data)

    def clear_llms_keys(self) -> CustomSettings:
        data = self._rest_client.put(f"{self.base_path}/clear-keys", data={})
        return CustomSettings(**data)

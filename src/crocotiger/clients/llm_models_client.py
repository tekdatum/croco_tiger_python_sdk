from crocotiger.models.llm_model import LLMModels
from crocotiger.utils.rest import RestClient


class LLMModelsClient:
    def __init__(self, rest_client: RestClient):
        self._rest_client = rest_client
        self._endpoint = "/llm-models"

    def find_llm_models(self) -> LLMModels:
        data = self._rest_client.get(self._endpoint)
        return LLMModels(**data)

    def refresh_llm_models(self) -> LLMModels:
        data = self._rest_client.post(f"{self._endpoint}/refresh", data={})
        return LLMModels(**data)

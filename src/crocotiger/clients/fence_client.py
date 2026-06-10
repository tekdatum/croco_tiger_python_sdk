from crocotiger.models.fence_correction import FenceCorrection
from crocotiger.models.fence_validation import FenceValidation
from crocotiger.utils.rest import RestClient


class FenceClient:
    def __init__(self, rest_client: RestClient):
        self._rest_client = rest_client
        self._endpoint = "/fence"

    def validate(self, project_id: int, text: str) -> FenceValidation:
        data = self._rest_client.post(
            f"{self._endpoint}/validate/{project_id}", data={"text": text}
        )
        return FenceValidation(**data)

    def commit_corrections(
        self, project_id: int, corrections: list[FenceCorrection]
    ) -> None:
        self._rest_client.post(
            f"{self._endpoint}/commit/{project_id}",
            data={"corrections": [c.model_dump() for c in corrections]},
        )

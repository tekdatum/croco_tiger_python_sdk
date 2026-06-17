from datetime import datetime
from typing import Any, Dict, Optional

from crocotiger.models.fence_correction import FenceCorrection
from crocotiger.models.fence_event import FenceEventPage
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

    def find_events(
        self,
        project_id: int,
        limit: int = 50,
        offset: int = 0,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> FenceEventPage:
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if start_date is not None:
            params["start_date"] = start_date.isoformat()
        if end_date is not None:
            params["end_date"] = end_date.isoformat()
        data = self._rest_client.get_paged(
            f"{self._endpoint}/events/{project_id}", params=params
        )
        return FenceEventPage(**data)

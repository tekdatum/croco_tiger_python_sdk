from typing import Any
from crocotiger.models.project import Project
from crocotiger.utils.rest import RestClient


class ProjectClient:
    def __init__(self, rest_client: RestClient):
        self._rest_client = rest_client
        self._endpoint = "/project"

    def create(
        self,
        name: str,
        context: str,
        topic: str,
        restricted_topics: list[str] | None = None,
        url: str | None = None,
        total_topic_questions: int | None = None,
        zip: str | None = None,
        optimization_strategy: str | None = None,
        openai_llm: str | None = None,
        gemini_llm: str | None = None,
    ) -> Project:
        """Create a project. Optional fields left as None are omitted from the
        payload, so the server-side defaults apply."""
        payload: dict[str, Any] = {
            "name": name,
            "context": context,
            "topic": topic,
        }
        optional: dict[str, Any] = {
            "restricted_topics": restricted_topics,
            "url": url,
            "total_topic_questions": total_topic_questions,
            "zip": zip,
            "optimization_strategy": optimization_strategy,
            "openai_llm": openai_llm,
            "gemini_llm": gemini_llm,
        }
        payload.update({k: v for k, v in optional.items() if v is not None})
        data = self._rest_client.post(f"{self._endpoint}", data=payload)
        return Project(**data)

    def find_all(self, limit: int, offset: int) -> list[Project]:
        data = self._rest_client.get(f"{self._endpoint}?limit={limit}&offset={offset}")
        return [Project(**item) for item in data]

    def update(
        self,
        project_id: int,
        name: str | None = None,
        status: str | None = None,
        context: str | None = None,
        topic: str | None = None,
        restricted_topics: list[str] | None = None,
        url: str | None = None,
        zip: str | None = None,
        total_topic_questions: int | None = None,
        optimization_strategy: str | None = None,
        openai_llm: str | None = None,
        gemini_llm: str | None = None,
    ) -> Project:
        """Partially update a project. Fields left as None are omitted from the
        payload and remain unchanged server-side (clearing a nullable field by
        sending an explicit null is not supported)."""
        candidate: dict[str, Any] = {
            "name": name,
            "status": status,
            "context": context,
            "topic": topic,
            "restricted_topics": restricted_topics,
            "url": url,
            "zip": zip,
            "total_topic_questions": total_topic_questions,
            "optimization_strategy": optimization_strategy,
            "openai_llm": openai_llm,
            "gemini_llm": gemini_llm,
        }
        payload = {k: v for k, v in candidate.items() if v is not None}
        data = self._rest_client.put(f"{self._endpoint}/{project_id}", data=payload)
        return Project(**data)

    def delete(self, project_id: int) -> None:
        self._rest_client.delete(f"{self._endpoint}/{project_id}")

    def find_one(self, project_id: int) -> Project:
        data = self._rest_client.get(f"{self._endpoint}/{project_id}")
        return Project(**data)

    def find_one_by_name(self, name: str) -> Project:
        data = self._rest_client.get(f"{self._endpoint}/one-by-name/{name}")
        return Project(**data)

    def upload_chained_zip(
        self, project_id: int, file_path: str, rewrite: bool = False
    ) -> dict[str, Any]:
        data = self._rest_client.upload_file(
            f"{self._endpoint}/{project_id}/zip/chain?rewrite={str(rewrite).lower()}",
            file_path=file_path,
        )
        return dict(data)

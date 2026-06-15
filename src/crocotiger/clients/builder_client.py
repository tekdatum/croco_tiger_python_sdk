from typing import Any, Optional
from crocotiger.utils.rest import RestClient


class BuilderClient:
    def __init__(self, rest_client: RestClient):
        self._rest_client = rest_client
        self.base_path = "/builder"

    @staticmethod
    def _build_id_params(build_id: int | None) -> dict[str, Any] | None:
        return {"build_id": build_id} if build_id is not None else None

    def build(
        self,
        project_id: int,
        notes: str | None = None,
        name: str | None = None,
        context: str | None = None,
        topic: str | None = None,
        restricted_topics: list[str] | None = None,
        url: str | None = None,
        zip: str | None = None,
        total_topic_questions: int | None = None,
        optimization_strategy: str | None = None,
        openai_llm: str | None = None,
        gemini_llm: str | None = None,
    ) -> dict[bool, str]:
        """Start a full build. Fields left as None are omitted from the payload
        and keep the current draft/active config; an empty body rebuilds the
        current config as-is."""
        candidate: dict[str, Any] = {
            "notes": notes,
            "name": name,
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
        data = self._rest_client.put(
            f"{self.base_path}/build/{project_id}", data=payload
        )
        return dict(data)

    def quick_build(
        self, project_id: int, notes: Optional[str] = None
    ) -> dict[str, Any]:
        body: dict[str, Any] = {}
        if notes is not None:
            body["notes"] = notes
        data = self._rest_client.put(
            f"{self.base_path}/quick-build/{project_id}", data=body
        )
        return dict(data)

    def stop(self, project_id: int, notes: Optional[str] = None) -> dict[str, Any]:
        """Stop the in-progress build for a project and marks the build as STOPPED
        so a new build can be started. ``notes`` is an optional reason appended to
        the build's notes. Returns 404 (project_not_found) if the project does not
        exist, or 403 (not_in_progress) if there is no active IN_PROGRESS build to
        stop."""
        body: dict[str, Any] = {}
        if notes is not None:
            body["notes"] = notes
        data = self._rest_client.put(f"{self.base_path}/stop/{project_id}", data=body)
        return dict(data)

    def find_project_logs(self, project_id: int) -> list[str]:
        data = self._rest_client.get(f"{self.base_path}/logs/{project_id}")
        return list(data)

    def find_project_log_by_name(self, project_id: int, file_name: str) -> bytes:
        data = self._rest_client.get_file(
            f"{self.base_path}/log/{project_id}/{file_name}"
        )
        return data

    def find_project_accept_list(
        self, project_id: int, build_id: int | None = None
    ) -> dict[str, Any]:
        data = self._rest_client.get(
            f"{self.base_path}/generated/{project_id}/accept_list",
            params=self._build_id_params(build_id),
        )
        return dict(data)

    def find_project_reject_list(
        self, project_id: int, build_id: int | None = None
    ) -> dict[str, Any]:
        data = self._rest_client.get(
            f"{self.base_path}/generated/{project_id}/reject_list",
            params=self._build_id_params(build_id),
        )
        return dict(data)

    def find_project_testing_metrics(
        self, project_id: int, build_id: int | None = None
    ) -> list[str]:
        data = self._rest_client.get(
            f"{self.base_path}/metrics/testing/{project_id}",
            params=self._build_id_params(build_id),
        )
        return list(data)

    def find_project_validation_metrics(
        self, project_id: int, build_id: int | None = None
    ) -> list[str]:
        data = self._rest_client.get(
            f"{self.base_path}/metrics/validation/{project_id}",
            params=self._build_id_params(build_id),
        )
        return list(data)

    def find_project_testing_metrics_by_name(
        self, project_id: int, file_name: str, build_id: int | None = None
    ) -> bytes:
        data = self._rest_client.get_file(
            f"{self.base_path}/metrics/testing/{project_id}/{file_name}",
            params=self._build_id_params(build_id),
        )
        return data

    def find_project_validation_metrics_by_name(
        self, project_id: int, file_name: str, build_id: int | None = None
    ) -> bytes:
        data = self._rest_client.get_file(
            f"{self.base_path}/metrics/validation/{project_id}/{file_name}",
            params=self._build_id_params(build_id),
        )
        return data

    def find_project_testing_summary(
        self, project_id: int, build_id: int | None = None
    ) -> list[str]:
        data = self._rest_client.get(
            f"{self.base_path}/summary/testing/{project_id}",
            params=self._build_id_params(build_id),
        )
        return list(data)

    def find_project_validation_summary(
        self, project_id: int, build_id: int | None = None
    ) -> list[str]:
        data = self._rest_client.get(
            f"{self.base_path}/summary/validation/{project_id}",
            params=self._build_id_params(build_id),
        )
        return list(data)

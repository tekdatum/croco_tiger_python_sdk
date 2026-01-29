from models.project import Project
from utils.rest import RestClient


class ProjectClient:
    def __init__(self, rest_client: RestClient):
        self._rest_client = rest_client
        self._endpoint = "/project"

    def create(
        self,
        name: str,
        context: str,
        topic: str,
        restricted_topics: list[str],
        url: str,
        total_topic_questions: int,
        zip: str = "",
    ) -> Project:
        payload = {
            "name": name,
            "context": context,
            "topic": topic,
            "restricted_topics": restricted_topics,
            "url": url,
            "total_topic_questions": total_topic_questions,
            "zip": zip,
        }
        data = self._rest_client.post(f"{self._endpoint}/create", data=payload)
        return Project(**data)

    def find_all(self) -> list[Project]:
        data = self._rest_client.get(f"{self._endpoint}/all")
        return [Project(**item) for item in data]

    def update(
        self,
        project_id: int,
        name: str,
        context: str,
        topic: str,
        restricted_topics: list[str],
        url: str,
        total_topic_questions: int,
        zip: str = "",
    ) -> Project:
        payload = {
            "name": name,
            "context": context,
            "topic": topic,
            "restricted_topics": restricted_topics,
            "url": url,
            "total_topic_questions": total_topic_questions,
            "zip": zip,
        }
        data = self._rest_client.post(
            f"{self._endpoint}/update/{project_id}", data=payload
        )
        return Project(**data)

    def delete(self, project_id: int) -> None:
        self._rest_client.post(f"{self._endpoint}/delete/{project_id}", data={})

    def find_one(self, project_id: int) -> Project:
        data = self._rest_client.get(f"{self._endpoint}/{project_id}")
        return Project(**data)

    def upload_chained_zip(self, project_id: int, file_path: str) -> None:
        raise NotImplementedError("Upload of chained zip is not implemented yet.")

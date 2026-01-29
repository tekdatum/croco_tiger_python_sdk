from datetime import datetime

from crocotiger_sdk.enums.BuildStep import BuildStep
from crocotiger_sdk.enums.ProjectStatus import ProjectStatus

from pydantic import BaseModel


class Project(BaseModel):
    id: int
    name: str
    topic: str
    restricted_topics: list[str]
    url: str | None = None
    zip: str | None = None
    context: str
    total_topic_questions: int
    status: ProjectStatus
    last_build_step: BuildStep
    accept_threshold: float
    reject_threshold: float
    created_at: datetime
    updated_at: datetime | None = None
    build_started_at: datetime | None = None
    build_finished_at: datetime | None = None

    def __str__(self) -> str:
        fields = [f"{field}: {getattr(self, field)}" for field in self.__fields__]
        return "Project(\n  " + ",\n  ".join(fields) + "\n)"

    def is_done(self) -> bool:
        return self.status == ProjectStatus.DONE

from datetime import datetime


from pydantic import BaseModel

from crocotiger.enums.build_step import BuildStep
from crocotiger.enums.optimization_strategy import OptimizationStrategy
from crocotiger.enums.project_status import ProjectStatus
from crocotiger.models.project_build import ProjectBuild


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
    optimization_strategy: OptimizationStrategy = OptimizationStrategy.BALANCED
    openai_llm: str | None = None
    gemini_llm: str | None = None
    can_quick_rebuild: bool = False
    active_build: ProjectBuild | None = None
    latest_build: ProjectBuild | None = None

    def is_done(self) -> bool:
        return self.status == ProjectStatus.DONE

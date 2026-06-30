from datetime import datetime

from pydantic import BaseModel

from crocotiger.enums.build_step import BuildStep
from crocotiger.enums.optimization_strategy import OptimizationStrategy
from crocotiger.enums.project_status import ProjectStatus


class ProjectBuild(BaseModel):
    id: int | None = None
    project_id: int
    build_number: int
    status: ProjectStatus
    last_build_step: BuildStep
    accept_threshold: float
    reject_threshold: float
    is_active: bool
    build_started_at: datetime | None = None
    build_finished_at: datetime | None = None
    created_at: datetime
    notes: str | None = None
    topic: str
    context: str
    restricted_topics: list[str] = []
    url: str | None = None
    zip: str | None = None
    total_topic_questions: int
    optimization_strategy: OptimizationStrategy = OptimizationStrategy.BALANCED
    openai_llm: str | None = None
    gemini_llm: str | None = None
    deepseek_llm: str | None = None

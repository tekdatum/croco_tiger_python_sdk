from datetime import datetime

import pytest
from pydantic import ValidationError

from crocotiger.enums.build_step import BuildStep
from crocotiger.enums.optimization_strategy import OptimizationStrategy
from crocotiger.enums.project_status import ProjectStatus
from crocotiger.models.project_build import ProjectBuild


class TestProjectBuild:
    def test_valid_project_build(self) -> None:
        build = ProjectBuild(
            id=7,
            project_id=1,
            build_number=2,
            status=ProjectStatus.DONE,
            last_build_step=BuildStep.DONE,
            accept_threshold=0.5,
            reject_threshold=0.7,
            is_active=True,
            created_at=datetime.now(),
            notes="Tuned thresholds",
            topic="AI Testing",
            context="A test context",
            restricted_topics=["NSFW"],
            total_topic_questions=5000,
            optimization_strategy=OptimizationStrategy.STRICT,
            openai_llm="gpt-4o",
        )

        assert build.build_number == 2
        assert build.is_active is True
        assert build.notes == "Tuned thresholds"
        assert build.optimization_strategy == OptimizationStrategy.STRICT

    def test_defaults(self) -> None:
        build = ProjectBuild(
            project_id=1,
            build_number=1,
            status=ProjectStatus.DRAFT,
            last_build_step=BuildStep.NOT_STARTED,
            accept_threshold=0.5,
            reject_threshold=0.7,
            is_active=False,
            created_at=datetime.now(),
            topic="AI Testing",
            context="A test context",
            total_topic_questions=5000,
        )

        assert build.id is None
        assert build.notes is None
        assert build.restricted_topics == []
        assert build.url is None
        assert build.zip is None
        assert build.optimization_strategy == OptimizationStrategy.BALANCED
        assert build.openai_llm is None
        assert build.gemini_llm is None

    def test_missing_field(self) -> None:
        # "project_id" is missing
        with pytest.raises(ValidationError):
            ProjectBuild(
                build_number=1,
                status=ProjectStatus.DRAFT,
                last_build_step=BuildStep.NOT_STARTED,
                accept_threshold=0.5,
                reject_threshold=0.7,
                is_active=False,
                created_at=datetime.now(),
                topic="AI Testing",
                context="A test context",
                total_topic_questions=5000,
            )

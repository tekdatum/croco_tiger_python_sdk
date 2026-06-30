from datetime import datetime

from crocotiger.enums.build_step import BuildStep
from crocotiger.enums.optimization_strategy import OptimizationStrategy
from crocotiger.enums.project_status import ProjectStatus
from crocotiger.models.project import Project  # Adjust import path as needed
from crocotiger.models.project_build import ProjectBuild


class TestProject:
    def test_is_done_when_status_is_not_done(self) -> None:
        project = Project(
            id=1,
            name="Test Project",
            topic="AI Testing",
            restricted_topics=["NSFW", "Political"],
            context="A test context",
            total_topic_questions=10,
            status=ProjectStatus.IN_PROGRESS,
            last_build_step=BuildStep.TEST_BENCHMARKING,
            accept_threshold=0.8,
            reject_threshold=0.2,
            created_at=datetime.now(),
        )

        # Act & Assert
        assert not project.is_done()

    def test_is_done_when_status_is_done(self) -> None:
        project = Project(
            id=1,
            name="Test Project",
            topic="AI Testing",
            restricted_topics=["NSFW", "Political"],
            context="A test context",
            total_topic_questions=10,
            status=ProjectStatus.DONE,
            last_build_step=BuildStep.TEST_BENCHMARKING,
            accept_threshold=0.8,
            reject_threshold=0.2,
            created_at=datetime.now(),
        )

        # Act & Assert
        assert project.is_done()

    def test_build_fields_defaults(self) -> None:
        project = Project(
            id=1,
            name="Test Project",
            topic="AI Testing",
            restricted_topics=[],
            context="A test context",
            total_topic_questions=10,
            status=ProjectStatus.DRAFT,
            last_build_step=BuildStep.NOT_STARTED,
            accept_threshold=0.5,
            reject_threshold=0.7,
            created_at=datetime.now(),
        )

        assert project.optimization_strategy == OptimizationStrategy.BALANCED
        assert project.openai_llm is None
        assert project.gemini_llm is None
        assert project.deepseek_llm is None
        assert project.can_quick_rebuild is False
        assert project.active_build is None
        assert project.latest_build is None

    def test_with_nested_builds(self) -> None:
        build_data = {
            "id": 7,
            "project_id": 1,
            "build_number": 2,
            "status": ProjectStatus.DONE,
            "last_build_step": BuildStep.DONE,
            "accept_threshold": 0.5,
            "reject_threshold": 0.7,
            "is_active": True,
            "created_at": datetime.now(),
            "topic": "AI Testing",
            "context": "A test context",
            "total_topic_questions": 5000,
            "optimization_strategy": "broad",
        }
        project = Project(
            id=1,
            name="Test Project",
            topic="AI Testing",
            restricted_topics=[],
            context="A test context",
            total_topic_questions=5000,
            status=ProjectStatus.DONE,
            last_build_step=BuildStep.DONE,
            accept_threshold=0.5,
            reject_threshold=0.7,
            created_at=datetime.now(),
            optimization_strategy="broad",
            openai_llm="gpt-4o",
            can_quick_rebuild=True,
            active_build=build_data,
            latest_build=build_data,
        )

        assert project.optimization_strategy == OptimizationStrategy.BROAD
        assert project.openai_llm == "gpt-4o"
        assert project.can_quick_rebuild is True
        assert isinstance(project.active_build, ProjectBuild)
        assert project.active_build.build_number == 2
        assert project.active_build.is_active is True
        assert isinstance(project.latest_build, ProjectBuild)

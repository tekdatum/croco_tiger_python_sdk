from datetime import datetime

from crocotiger.enums.build_step import BuildStep
from crocotiger.enums.project_status import ProjectStatus
from crocotiger.models.project import Project  # Adjust import path as needed


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

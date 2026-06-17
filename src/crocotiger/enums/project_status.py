from enum import Enum


class ProjectStatus(Enum):
    DRAFT = "draft"
    ARCHIVED = "archived"
    IN_PROGRESS = "in_progress"
    FAILED = "failed"
    DONE = "done"
    STOPPED = "stopped"

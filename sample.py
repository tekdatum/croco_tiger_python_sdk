from crocotiger.sdk import SDK
from crocotiger.demo.projects import Project

client = SDK(base_path="http://localhost:8000/api/v1")

# Load the project
project_client = client.get_project_client()
project = project_client.find_one_by_name(Project.MEDICARE.value)
print(project)

project_client.update(
    project_id=project.id,
    name=project.name,
    topic=project.topic,
    restricted_topics=project.restricted_topics,
    total_topic_questions=project.total_topic_questions,
    url=project.url,
    zip=project.zip,
    context="Any context",
)

# Validate text for a specific project (e.g., project_id=1)
fence_client = client.get_fence_client()
validation_result = fence_client.validate(project_id=project.id, text="Text")

if validation_result.valid:
    print("✅ Text is valid.")
else:
    print(f"❌ Violation detected. Reason: {validation_result.reason_code}")

# CrocoTiger SDK

<p align="center">
  <a href="https://crocotiger.com" target="_blank">
    <img src="https://crocotiger.com/shield.png" alt="CrocoTiger Logo" width="100"/>
  </a>
</p>

<p align="center">
    <a href="https://aws.amazon.com/marketplace/pp/prodview-2xe32k5vgnekk" target="_blank">
        <img src="https://img.shields.io/badge/AWS%20Marketplace-Available-blue?logo=amazonaws" alt="AWS Marketplace"/>
    </a>
    <a href="https://pypi.org/project/crocotiger-sdk/" target="_blank">
        <img src="https://badge.fury.io/py/crocotiger-sdk.svg" alt="PyPI version"/>
    </a>
    <a href="https://pypi.org/project/crocotiger-sdk/" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/crocotiger-sdk.svg" alt="Python Versions"/>
    </a>
    <a href="https://opensource.org/licenses/Apache-2.0" target="_blank">
        <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License"/>
    </a>
</p>

This is the official Python SDK for the **CrocoTiger Engine API**.

It allows developers to easily integrate CrocoTiger's powerful **semantic fence capabilities** into their applications, enabling robust validation, project management, and data generation workflows.

---

## Download a sample docker image
CrocoTiger offers a development edition docker image with sample projects for development and testing purposes.

1. Install docker
2. Do `docker pull public.ecr.aws/k9l9y2x7/tekdatum/croco-tiger-developer-edition:1.1`
3. Do `docker run -d --name croco_tiger_container --gpus all -p 8000:8000 public.ecr.aws/k9l9y2x7/tekdatum/croco-tiger-developer-edition:1.1`
4. Replace `api_url` with `http://localhost:8000/api/v1/`

---

## Installation

To use the CrocoTiger SDK, first install it via pip:

```bash
pip install crocotiger-sdk
```

## Quick Start

### 1. Configuration

You can initialize the SDK by passing your API URL directly.

```python
from crocotiger_sdk.sdk import SDK

client = SDK(api_url="<your_api_url>")
```

### 2. Basic Usage (Fence Validation)

The most common use case is validating text against a project's fence rules.

```python
from crocotiger_sdk import SDK

client = SDK(api_url="https://api.crocotiger.com")
fence_client = client.get_fence_client()

# Validate text for a specific project (e.g., project_id=1)
validation_result = fence_client.validate(
    project_id=1, 
    text="Text to validate"
)

if validation_result.valid:
    print("✅ Text is valid.")
else:
    print(f"❌ Violation detected. Reason: {validation_result.reason_code}")

```

## Modules

The SDK provides various clients to interact with different parts of the Engine API.

### Project Client

To interact with projects, use the `ProjectClient`. It allows you to create, find, update, and delete projects.

```python
project_client = client.get_project_client()
project = project_client.find_one(1)
print(f"Project Name: {project.name}")

```

**Available methods**:
| Method | Description |
| :--- | :--- |
| `create` | Create a new project. |
| `find_all` | Retrieve all projects. This allows pagination using limit and offset parameters. |
| `find_one` | Retrieve a single project by its ID. |
| `update` | Update an existing project. |
| `delete` | Delete a project by its ID. |
| `upload_zip` | Upload a zip file for the project. |

### Custom Settings Client

The Custom Settings Client allows you to manage the LLM API Keys (e.g., OpenAI, Gemini) for your projects.

```python
settings_client = client.get_custom_settings_client()

# Update keys
settings_client.update_custom_settings(
    openai_key="<your_openai_api_key>",
    gemini_key="<your_gemini_api_key>",
)

# Clear or Retrieve keys
settings_client.clear_llms_keys()
current_settings = settings_client.find_custom_settings()
```

**Available methods**:

* `update_custom_settings`: Update the custom settings with new LLM API keys.
* `clear_llms_keys`: Clear all LLM API keys.
* `find_custom_settings`: Retrieve the current configuration.

### Builder Client

The Builder Client allows you to trigger builds and retrieve generated data (accept/reject lists, logs, and metrics).

**1. Trigger a Build**

```python
builder_client = client.get_builder_client()
builder_client.build(project_id=1)
```

**2. Retrieve Generated Data**
The client offers specific methods to find lists, logs, and metrics by project ID.

```python
# Get lists
accept_list = builder_client.find_project_accept_list(1)
reject_list = builder_client.find_project_reject_list(1)

# Get specific files
log_file = builder_client.find_project_log_by_name(1, "build_log_v1.txt")
```

**Available methods**:

* **List Retrieval:**
* `find_project_accept_list`
* `find_project_reject_list`


* **General Retrieval (Get all filenames):**
* `find_project_logs`
* `find_project_testing_metrics`
* `find_project_validation_metrics`


* **Specific Item Retrieval:**
* `find_project_log_by_name`
* `find_project_testing_metrics_by_name` (Pass a `testing_summary` filename to get metrics)
* `find_project_validation_metrics_by_name` (Pass a `validation_summary` filename to get metrics)


* **Summaries:**
* `find_project_testing_summary`
* `find_project_validation_summary`



---

## 📄 License

This project is licensed under the [Apache-2.0 License](https://opensource.org/licenses/Apache-2.0).
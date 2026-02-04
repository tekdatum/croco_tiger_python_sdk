# CrocoTiger SDK

This is the official Python SDK for CrocoTiger Engine API. It allows developers to easily integrate CrocoTiger's powerful semantic fence capabilities into their Python applications.

---
## Usage [WIP - need to define the pypi package name]
To use the CrocoTiger SDK, first install it via pip:

```bash
pip install crocotiger_sdk
```

Then, you can import the SDK and start using it in your Python code:

```python
import crocotiger_sdk as crocotiger

client = crocotiger.SDK(api_url="<YOUR_API_URL>")
project = client.get_project_client().find_one(1)
print(project)
```

## How to use

The SDK provides various clients to interact with different parts of the Engine API. Below are examples of how to use these clients.

## Project Client
To interact with projects, you can use the `ProjectClient`. Here's an example of how to retrieve a project by its ID:

**Available methods**:
  - `create`: Create a new project.
  - `find_all`: Retrieve all projects.
  - `update`: Update an existing project.
  - `delete`: Delete a project by its ID.
  - `find_one`: Retrieve a single project by its ID.
  - `upload_chained_zip`: (Not implemented) Upload a chained zip file for the project.

**Usage**:

```python
from sdk import SDK

sdk = SDK()
project_client = sdk.get_project_client()
project = project_client.find_one(1)
print(project)
```

## Custom Settings Client
Custom settings client allow you to manage the LLM API Keys for your projects. 

**Available methods**:
  - `update_custom_settings`: Update the custom settings with new LLM API keys.
  - `clear_llms_keys`: Clear all LLM API keys from the custom settings.
  - `find_custom_settings`: Retrieve the current custom settings.

**Usage**:

```python
from sdk import SDK

sdk = SDK()
custom_settings = sdk.get_custom_settings_client().update_custom_settings(
    openai_key="sk-xxxx",
    gemini_key="gemini-xxxx",
)
custom_settings = sdk.get_custom_settings_client().clear_llms_keys()
custom_settings = sdk.get_custom_settings_client().find_custom_settings()
print(custom_settings)
```

### Builder Client
The Builder Client allows you build and retrieve generated data for your projects.

**Available methods**:
 - `build`: Trigger the build process for a project.

 - ***List retrieval methods***: these methods allow you to get accept and reject lists samples generated for a project.
    - `find_project_accept_list`: Retrieve the accept list for a project.
    - `find_project_reject_list`: Retrieve the reject list for a project.

 - ***General retrieval methods***: these methods allow you to get all filenames of a certain type for a project.
    - `find_project_logs`: Retrieve all logs filename for a project.
    - `find_project_testing_metrics`: Retrieve testing metrics filename for a project.
    - `find_project_validation_metrics`: Retrieve validation metrics filename for a project.
 
  - ***Specific item retrieval methods***: these methods allow you to get the specific file you are looking for by its project id and filename.
    - `find_project_log_by_name`: Retrieve a specific log by name for a project.
    - `find_project_testing_metrics_by_name`: Retrieve a specific testing metrics file by name for a project. You can also pass a `testing_summary` file name to get the corresponding metrics.
    - `find_project_validation_metrics_by_name`: Retrieve a specific validation metrics file by name for a project. You can also pass a `validation_summary` file name to get the corresponding metrics.
  
  - ***Summary methods***:
    - `find_project_testing_summary`: Retrieve testing summary for a project.
    - `find_project_validation_summary`: Retrieve validation summary for a project.

**Usage**:
```python
from sdk import SDK
sdk = SDK()
builder_client = sdk.get_builder_client()
accept_list = builder_client.find_project_accept_list(1)
print(accept_list)
```

### Fence Client
The Fence Client allows you to validate text against a project's fence rules.

**Available methods**:
  - `validate`: Validate text to check if it complies with the project's fence rules.

**Usage**:

```python
from sdk import SDK

sdk = SDK()
fence_client = sdk.get_fence_client()

# Validate text for a project (e.g. project_id=1)
validation_result = fence_client.validate(project_id=1, text="Text to validate")

print(f"Valid: {validation_result.valid}")
print(f"Reason: {validation_result.reason_code}")
```
# How to use the SDK clients

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

## Builder Client
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

# TODO: Add examples for other clients
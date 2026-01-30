from sdk import SDK

sdk = SDK()
project = sdk.get_project_client().find_one(1)
print(project)

custom_settings = sdk.get_custom_settings_client().find_custom_settings()
print(custom_settings)
custom_settings = sdk.get_custom_settings_client().update_custom_settings(
    openai_key="sk-xxxx",
    gemini_key="gemini-xxxx",
)
print(custom_settings)
custom_settings = sdk.get_custom_settings_client().clear_llms_keys()
print(custom_settings)

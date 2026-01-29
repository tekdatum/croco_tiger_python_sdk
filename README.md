# CrocoTiger SDK

This is the official Python SDK for CrocoTiger Engine API. It allows developers to easily integrate CrocoTiger's powerful semantic fence capabilities into their Python applications.

### [🔗 Setup](docs/setup.md)
### [🔗 Clients usage](docs/how-to.md)

---
### Usage [WIP - need to define the pypi package name]
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

For more detailed usage instructions and examples, please refer to the [Usage Documentation](docs/usage.md).
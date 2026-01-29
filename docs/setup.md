# Setup & Development (VENV)

## 1. Create the Virtual Environment

1. Navigate to the sdk folder and create the venv:
    ```bash
    python3 -m venv engine_sdk --without-pip
    ```

2. Activate the virtual environment:
    ```bash
    source engine_sdk/bin/activate
    ```

3. Install pip:
    ```bash
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    rm get-pip.py
    ```

4. Activate the virtual environment (if not already activated):
    ```bash
    source engine_sdk/bin/activate
    ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
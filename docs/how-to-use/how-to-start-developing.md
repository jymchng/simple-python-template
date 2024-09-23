# How to Start Development

This page will teach you how to start developing.

## Run the script located in `${PROJECT_ROOT_DIR}/scripts/create_venv.sh`

The `create_venv.sh` script is designed to simplify the process of creating a Python virtual environment based on a specified Python version. This script allows you to specify either an exact version (e.g., `3.8.17`) or a major and minor version (e.g., `3.8`), and it will automatically find the appropriate version installed via `pyenv`.

### Functionality

1. **Argument Handling**: The script requires one argument, which is the desired Python version. If no argument is provided, it displays usage instructions and exits.

2. **Exact Version Check**: It first checks if the exact version directory exists in the `$(PYENV_ROOT)/versions` directory. If it does, the script uses that version directly.

3. **Finding the Largest Version**: If the exact version is not found, the script searches for the largest available version that matches the specified major and minor version. It iterates through the directories in `$(PYENV_ROOT)/versions` that start with the specified version and selects the highest version based on the directory names.

4. **Creating the Virtual Environment**: Once the appropriate version is determined, the script uses the corresponding Python executable to create a virtual environment named `.venv` in the current working directory.

5. **Error Handling**: The script includes error handling to notify the user if no matching Python version is found or if the Python executable is not available.

### Usage

To use the script, run the following command in your terminal:

<div style="border: 1px solid green; padding: 10px; background-color: #d4edda; color: #155724;">
  <strong>Info:</strong>

  <pre id="codeBlock"><code>bash scripts/create_venv.sh 3.12</code></pre>
  to create `./.venv` virtual environment in $PWD
</div>


## Activate the Virtual Environment and Install `poetry`

To activate the virtual environment, run the following command:

```bash
source .venv/bin/activate
```

Once the virtual environment is activated, you can install Poetry by running:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

This command will download and install the latest version of Poetry. After installation, you can verify it by checking the version:

```bash
poetry --version
```

## Configuring Poetry to Use a `.venv` Directory

To ensure that Poetry uses a specific `.venv` directory for managing your project's virtual environment, follow these steps:

**Set the Virtual Environment Path**:
You need to configure Poetry to create the virtual environment within your project directory. Run the following command in your terminal while in your project directory:

```bash
poetry config virtualenvs.in-project true
```

This command modifies Poetry's configuration to ensure that the virtual environment is created in a folder named `.venv` within your project directory.


## Install all the dependencies EXCEPT the package itself

The following command installs all the dependencies listed in your `pyproject.toml` file, excluding the package itself. This is useful for setting up the development environment without installing the package as a module, allowing you to work on the code without affecting the package installation.

```bash
poetry install --no-root -vv
```

### Explanation:
- **`poetry install`**: This command reads the `pyproject.toml` file and installs all the required dependencies specified under the `[tool.poetry.dependencies]` section.
- **`--no-root`**: This flag prevents Poetry from installing the package itself in the current environment. It is particularly useful during development when you want to test changes without reinstalling the package.

By using this command, you ensure that your environment is set up with all necessary dependencies while keeping the package in a state that reflects your current development work.

### All Commands

```bash
bash scripts/create_venv.sh <your-minimal-supported-python-version, e.g. 3.8>
source .venv/bin/activate
curl -sSL https://install.python-poetry.org | python3 -
poetry --version
poetry config virtualenvs.in-project true
poetry install --no-root -vv
```

<div align="center"><h2>
DONE! You're ready to code!
</h2></div>

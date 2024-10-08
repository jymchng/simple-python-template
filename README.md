<div align="center">
  <img src="./docs/assets/simple-python-template-logo.png" width="200">
</div><p>

<div align="center">

# Simple Python Template

## Documentation
<a href="https://spyt.asyncmove.com">
  <img src="https://img.shields.io/badge/docs-passing-brightgreen.svg" width="100" alt="docs passing">
</a>

### Compatibility and Version
<img src="https://img.shields.io/badge/%3E=python-3.8-blue.svg" alt="Python compat">
<a href="https://pypi.python.org/pypi/simple-python-template"><img src="https://img.shields.io/pypi/v/simple-python-template.svg" alt="PyPi"></a>

### CI/CD
<a href="https://github.com/jymchng/simple-python-template/actions?query=workflow%3Atests"><img src="https://github.com/jymchng/simple-python-template/actions/workflows/tests.yaml/badge.svg?branch=main" alt="GHA Status"></a>
<a href="https://codecov.io/github/jymchng/simple-python-template?branch=main"><img src="https://codecov.io/github/jymchng/simple-python-template/coverage.svg?branch=main" alt="Coverage"></a>

### License and Issues
<a href="https://github.com/jymchng/simple-python-template/blob/main/LICENSE"><img src="https://img.shields.io/github/license/jymchng/simple-python-template" alt="License"></a>
<a href="https://github.com/jymchng/simple-python-template/issues"><img src="https://img.shields.io/github/issues/jymchng/simple-python-template" alt="Issues"></a>
<a href="https://github.com/jymchng/simple-python-template/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed/jymchng/simple-python-template" alt="Closed Issues"></a>
<a href="https://github.com/jymchng/simple-python-template/issues?q=is%3Aissue+is%3Aopen"><img src="https://img.shields.io/github/issues-raw/jymchng/simple-python-template" alt="Open Issues"></a>

### Development and Quality
<a href="https://github.com/jymchng/simple-python-template/network/members"><img src="https://img.shields.io/github/forks/jymchng/simple-python-template" alt="Forks"></a>
<a href="https://github.com/jymchng/simple-python-template/stargazers"><img src="https://img.shields.io/github/stars/jymchng/simple-python-template" alt="Stars"></a>
<a href="https://pypi.python.org/pypi/simple-python-template"><img src="https://img.shields.io/pypi/dm/simple-python-template" alt="Downloads"></a>
<a href="https://github.com/jymchng/simple-python-template/graphs/contributors"><img src="https://img.shields.io/github/contributors/jymchng/simple-python-template" alt="Contributors"></a>
<a href="https://github.com/jymchng/simple-python-template/commits/main"><img src="https://img.shields.io/github/commit-activity/m/jymchng/simple-python-template" alt="Commits"></a>
<a href="https://github.com/jymchng/simple-python-template/commits/main"><img src="https://img.shields.io/github/last-commit/jymchng/simple-python-template" alt="Last Commit"></a>
<a href="https://github.com/jymchng/simple-python-template"><img src="https://img.shields.io/github/languages/code-size/jymchng/simple-python-template" alt="Code Size"></a>
<a href="https://github.com/jymchng/simple-python-template"><img src="https://img.shields.io/github/repo-size/jymchng/simple-python-template" alt="Repo Size"></a>
<a href="https://github.com/jymchng/simple-python-template/watchers"><img src="https://img.shields.io/github/watchers/jymchng/simple-python-template" alt="Watchers"></a>
<a href="https://github.com/jymchng/simple-python-template"><img src="https://img.shields.io/github/commit-activity/y/jymchng/simple-python-template" alt="Activity"></a>
<a href="https://github.com/jymchng/simple-python-template/pulls"><img src="https://img.shields.io/github/issues-pr/jymchng/simple-python-template" alt="PRs"></a>
<a href="https://github.com/jymchng/simple-python-template/pulls?q=is%3Apr+is%3Aclosed"><img src="https://img.shields.io/github/issues-pr-closed/jymchng/simple-python-template" alt="Merged PRs"></a>
<a href="https://github.com/jymchng/simple-python-template/pulls?q=is%3Apr+is%3Aopen"><img src="https://img.shields.io/github/issues-pr/open/jymchng/simple-python-template" alt="Open PRs"></a>

</div>

# Simple Python Template

This template was bootstrapped with [BrianPugn's Python Template](https://github.com/BrianPugh/python-template).

The **Simple Python Template** is a robust and flexible starting point for Python projects, specifically designed to address the challenges faced by developers writing C-Python extensions. It showcases as an example to these:

1. Building pure C extension modules to Python.
2. Building C extension modules to Python with transpilation provided by Cython.
3. (In the near future) Vendoring another C library for building C extension modules in Python.

With a comprehensive `build.py` script included, this template simplifies the building of Python extension modules, whether you're using pure C or leveraging Cython for enhanced performance and ease of use. The `build.py` script automates the compilation and linking of C code, handling dependencies and configurations seamlessly. This allows you to focus on writing your extension logic rather than wrestling with build configurations.

# Table of Contents

- [Features](#features)
- [How to Use](#how-to-use)
- [Convenient Scripts](#convenient-scripts)
- [Testing with Docker](#testing-with-docker)

# Features
Modular Design: Easily extendable with modular components.

Testing Integration: Built-in support for unit and integration tests.

Documentation: Auto-generated documentation using Read the Docs.

Continuous Integration: Configured for GitHub Actions.

Code Quality: Integrated with Code Climate, Codacy, and Snyk for code quality and security.

Coverage Tracking: Coverage tracking with Codecov.

# How To Use

Read the [documentation](https://spyt.asyncmove.com/how-to-use/download/) on how to start using this template repository.

# Convenient Scripts

The scripts are located in the [./scripts](./scripts/) folder.

## quick_tests.sh

To quickly install the package and run tests, you can use the provided `install_and_test.sh` script. This script performs the following steps:

1. **Finds the Largest Version**: It searches for the largest version of the package in the `./dist` directory.

2. **Builds the Package if Not Found**: If no package is found, it attempts to build the package using `poetry build`.

3. **Checks for Existing Installation**: Before installing the package, it checks if the package is already installed using `pip show`.

4. **Uninstalls Existing Package**: If the package is found to be installed, it uninstalls it using `pip uninstall -y`.

5. **Installs the Largest Version**: It installs the largest version found in the `./dist` directory.

6. **Runs Tests**: Finally, it runs the tests using `pytest` to ensure everything is functioning correctly.

To run, use:

```bash
bash scripts/quick_tests.sh
```

## create_venv.sh

The `create_venv.sh` script is designed to simplify the process of creating a Python virtual environment based on a specified Python version. This script allows you to specify either an exact version (e.g., `3.8.17`) or a major and minor version (e.g., `3.8`), and it will automatically find the appropriate version installed via `pyenv`.

### Functionality

1. **Argument Handling**: The script requires one argument, which is the desired Python version. If no argument is provided, it displays usage instructions and exits.

2. **Exact Version Check**: It first checks if the exact version directory exists in the `$(PYENV_ROOT)/versions` directory. If it does, the script uses that version directly.

3. **Finding the Largest Version**: If the exact version is not found, the script searches for the largest available version that matches the specified major and minor version. It iterates through the directories in `$(PYENV_ROOT)/versions` that start with the specified version and selects the highest version based on the directory names.

4. **Creating the Virtual Environment**: Once the appropriate version is determined, the script uses the corresponding Python executable to create a virtual environment named `.venv` in the current working directory.

5. **Error Handling**: The script includes error handling to notify the user if no matching Python version is found or if the Python executable is not available.

### Usage

To use the script, run the following command in your terminal:

```
bash scripts/create_venv.sh 3.8 # to create `./.venv` virtual environment in $PWD
```

# Testing with Docker

This project includes a `Dockerfile_testing` that provides a convenient and isolated environment for building and testing the application using Docker. This ensures that the application behaves consistently across different environments and eliminates issues related to local dependencies.

## Features
- **Isolated Environment**: The Dockerfile sets up a clean environment with all necessary dependencies, ensuring that tests run in a consistent context.
- **Automated Dependency Management**: The Dockerfile uses Poetry to manage dependencies, making it easy to install the required packages without manual intervention.
- **Coverage Reporting**: The testing process includes coverage reporting, allowing you to see how much of your code is covered by tests.
- **Multi-Stage Build**: The Dockerfile employs a multi-stage build process, separating the build and runtime environments. This results in a smaller final image size by excluding unnecessary build dependencies.

## Usage
To use the `Dockerfile_testing` for testing your application, follow these steps:

1. **Build the Docker Image**:
   Run the following command in the root directory of your project to build the Docker image:
   ```bash
   docker build -f Dockerfile_testing -t testing_in_docker .
   ```

2. **Run the Tests**:
   After building the image, you can run the tests by executing:
   ```bash
   docker run --rm testing_in_docker
   ```
   This command will run the tests defined in your project, and you will see the output in your terminal.

3. **Review Coverage Reports**:
   The test run will include coverage reporting. Review the output to see which parts of your code are covered by tests and identify areas for improvement.

4. **Use Make**
   You can use `make` to automate this, simply run: `make test-in-docker`

# Good Articles and Answers

https://stackoverflow.com/questions/60073711/how-to-build-c-extensions-via-poetry

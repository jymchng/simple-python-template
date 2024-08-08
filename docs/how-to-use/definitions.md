# Definitions

Here are some of the definitions that are used throughout this documentation so that you will know how the different names of the directories and files can be mapped to your own copy of the repository.

|Term|Definitions|Name in this Repository|
|:---:|:---:|:---:|
|`PROJECT_ROOT_DIR`|The directory where the `PROJECT_MANIFEST_FILE` resides|`simple-python-template` (Note that it is different from `PROJECT_SOURCE_DIR` which, in this case, is `simple_python_template`, with underscores)|
|`PROJECT_SOURCE_DIR`|The directory where the Python source files (i.e. files that contain your Python code) are located.|`simple_python_template`|
|`PROJECT_C_SOURCE_DIR`|The directory where the C source files (i.e. files that contain your C code) are located.|`sources`|
|`PROJECT_BUILD_DIR`|The directory where built distributions (e.g., source distributions and wheels) are stored after running the build command. This is typically the `dist` directory created by tools like Poetry.|`dist`|
|`PROJECT_TESTS_DIR`|The directory where your test files are located. This is where you will place your test cases to ensure your code functions as expected. Typically, this directory contains files that start with `test_` or end with `_test.py`.|`tests`|
|`PROJECT_MANIFEST_FILE`|The file that contains the metadata related to your repository that is used by the build tool, it can be `pyproject.toml`, `requirements*.txt`, `setup.py` and many more, depending on the build tool (e.g. `poetry`, `pdm` or `hatch`).|`pyproject.toml`|

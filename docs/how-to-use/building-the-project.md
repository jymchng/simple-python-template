# Building the Package with Poetry

The command `poetry build` is a crucial step in the packaging process of a Python project. When executed, this command compiles the project into distributable formats, typically generating two types of artifacts:

1. **Source Distribution (SDist):** This is a tarball (`.tar.gz`) containing the raw source code of the project. It includes all Python files and any other resources that are necessary to install and run the package. This format is highly portable and can be built on any system, making it ideal for environments that need to compile the package from source.

2. **Wheel Distribution:** A wheel (`.whl`) is a pre-built binary distribution format. It is a ZIP-format archive that is ready to be installed without needing to compile any code. This format is faster to install than an SDist, especially when the project contains extensions written in C or Cython, as these are pre-compiled in the wheel.

These artifacts are stored in the `dist` directory, ready to be distributed to a package index like PyPI or for direct installation in an environment. By building both a source and a wheel distribution, you ensure that your package can be easily installed in any environment, whether it has the necessary build tools or not.

# An Extensive Discussion on `build.py`

The `build.py` script is an advanced build automation tool for Python projects that involve compiled extensions, typically written in C or Cython. This script is essential in projects where performance is critical, or where the Python codebase needs to interface directly with lower-level system components or external libraries.

## **1. Logging Configuration**
The script starts by setting up logging to provide detailed feedback during the build process. It uses the `logging` module to output logs with different levels of importance (e.g., DEBUG, INFO, ERROR). The logs are configured to be output to `sys.stdout`, which makes them visible in the terminal or command prompt.

```python
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)s] %(message)s",
    stream=sys.stdout,
)
LOGGER = getLogger(__name__)
LOGGER.info("Running `build.py`...")
```

## **2. Handling Cython and C Extensions**
The script checks if Cython is available. Cython is a powerful tool that can convert Python code to C for performance gains. If Cython is available, the script sets up the environment to use it; otherwise, it falls back to pure C compilation.

```python
USE_CYTHON = False
try:
    from Cython.Build import build_ext  # pyright: ignore [reportMissingImports]
    from Cython.Build import cythonize
    import Cython.Compiler.Options  # pyright: ignore [reportMissingImports]

    Cython.Compiler.Options.annotate = True
    USE_CYTHON = True
except ImportError:
    LOGGER.info("Unable to import `Cython`, falling back to building only `C` extensions")
```

## **3. Directory and File Checks**
The script includes functions to verify the existence of necessary directories and files. This ensures that the build process doesn’t encounter errors due to missing components.

```python
def where_am_i() -> "Path":
    """Checks if the script is being run in the correct directory (`PROJECT_ROOT_DIR`)."""
    current_dir = Path.cwd()
    if current_dir != PROJECT_ROOT_DIR:
        raise RuntimeError(f"Please run this script in the directory: {PROJECT_ROOT_DIR}")

    required_files = [
        "pyproject.toml",
        "setup.py",
        "setup.cfg",
        "requirements.txt",
        "requirements-dev.txt",
    ]
    if not any((PROJECT_ROOT_DIR / file).exists() for file in required_files):
        raise RuntimeError("`build.py` should be located at the root directory of the project")

    LOGGER.info(f"Running in the correct directory: {current_dir}")
    return PROJECT_ROOT_DIR
```

This function checks that the script is being executed in the project's root directory and that essential configuration files are present.

## **4. Compilation of Extensions**
The script is capable of building extensions using either C or Cython, depending on the availability of Cython. It defines a set of constants related to the project's directory structure and file locations, which are used during the build process.

- **C Extensions:** If Cython is not available, the script builds pure C extensions.

- **Cython Extensions:** If Cython is available, the script converts `.pyx` files (Cython source files) into `.c` files and then compiles them.

```python
def build_cython_extensions():
    """Builds the extension modules using Cython."""
    extensions = get_extension_modules()

    include_dirs = set()
    for extension in extensions:
        include_dirs.update(extension.include_dirs)
    include_dirs = list(include_dirs)

    ext_modules = cythonize(extensions, include_path=include_dirs, language_level=3)
    LOGGER.info(f"inside function `build_cython_extensions`; `ext_modules` = {ext_modules}")
    dist = Distribution({"ext_modules": ext_modules})
    cmd = build_ext(dist)
    cmd.ensure_finalized()
    cmd.run()
    LOGGER.info(f"`cmd.build_lib` = {cmd.build_lib}")

    copy_output_to_cmd_buildlib(cmd)

    # clean up only for cython
    for file in C_SOURCE_FILES_GENERATED_FROM_CYTHON:
        remove_cython_metadata(file)
        if REMOVE_HTML_ANNOTATION_FILES:
            html_associated_file = Path(file).with_suffix(".html")
            LOGGER.info(
                f"Removing html annotation file `{html_associated_file}` associated with `{file}`; "
            )
            if os.path.exists(str(html_associated_file)):
                os.unlink(str(html_associated_file))
            LOGGER.info("Html file is removed")
```

The `build_cython_extensions` function handles the entire process of building Cython extensions, including cleaning up any generated files that are not necessary for the final build (e.g., Cython metadata).

## **5. Custom Extensions**
The script allows the definition of custom extension modules. These are compiled separately and can include custom compile-time arguments and include directories.

```python
def get_extension_modules():
    include_dirs = [str(INCLUDE_DIR)]
    LOGGER.info(f"in function `get_extension_modules`; `include_dirs` = {include_dirs}")

    custom_ext = Extension(
        f"{PACKAGE_NAME}.custom",  
        [
            str(PROJECT_C_SOURCE_DIR / "custom.c")
        ],
        include_dirs=include_dirs,
        extra_compile_args=extra_compile_args(),
        language=LANGUAGE,
    )
    extensions = [_c_extension_ext, custom_ext]
    return extensions
```

This function returns a list of extensions that are then compiled either by Cython or pure C, depending on the availability of Cython.

## **6. Error Handling and Fallbacks**
The script includes robust error handling to ensure that any issues encountered during the build process are logged and managed appropriately. If the build fails and the `ALLOWED_TO_FAIL` flag is not set, the script raises an exception.

```python
if __name__ == "__main__":
    where_am_i()
    check_dir_files_existence()
    try:
        if USE_CYTHON:
            build_cython_extensions()
        else:
            build_c_extensions()
    except Exception as err:
        LOGGER.exception(f"`build.py` has failed: error = {err}")
        if not ALLOWED_TO_FAIL:
            raise
```

This structure ensures that the build process is both flexible and resilient, providing detailed feedback to the developer while attempting to compile the project.

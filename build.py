import logging
from logging import getLogger
import os
from pathlib import Path
import shutil
import sys
import platform

from setuptools import Extension  # noqa: I001
from setuptools.command.build_ext import build_ext  # noqa: I001
from setuptools.dist import Distribution  # noqa: I001


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)s] %(message)s",
    stream=sys.stdout,
)
LOGGER = getLogger(__name__)
LOGGER.info("Running `build.py`...")

# when using setuptools, you should import setuptools before Cython,
# otherwise, both might disagree about the class to use.
USE_CYTHON = False
try:
    from Cython.Build import build_ext  # pyright: ignore [reportMissingImports]
    from Cython.Build import cythonize
    import Cython.Compiler.Options  # pyright: ignore [reportMissingImports]

    Cython.Compiler.Options.annotate = True
    USE_CYTHON = True
except ImportError:
    LOGGER.info("Unable to import `Cython`, falling back to building only `C` extensions")


def list_dir_contents(directory, depth, level=0):
    if level > depth:
        return
    try:
        with os.scandir(directory) as entries:
            for entry in entries:
                print("  " * level + f"- {entry.name}")
                if entry.is_dir(follow_symlinks=False):
                    list_dir_contents(entry.path, depth, level + 1)
    except PermissionError as e:
        print(f"PermissionError: {e}")


def get_package_name(
    default_name="simple_python_template",
) -> str:  # put a default name if there is
    """Retrieves the package name from setup.py or setup.cfg, or returns a default name."""
    if default_name is not None:
        return default_name

    # # Check for pyproject.toml
    # if os.path.exists("pyproject.toml"):
    #     with open("pyproject.toml", "rb") as f:  # Open in binary mode for tomlib
    #         pyproject = loads(f)  # Use tomlib's loads function
    #     return pyproject.get("tool", {}).get("poetry", {}).get("name", None)

    # Check for setup.py
    if os.path.exists("setup.py"):
        with open("setup.py") as f:
            for line in f:
                if "name=" in line:
                    return line.split("name=")[1].strip().strip('"').strip("'")

    # Check for setup.cfg
    if os.path.exists("setup.cfg"):
        import configparser

        config = configparser.ConfigParser()
        config.read("setup.cfg")
        return config.get("metadata", "name")

    raise Exception(
        "Unable to determine what is the `PACKAGE_NAME` for this repository, set `default_name` parameter to a default name"
    )

# Constants
# Set `PROJECT_ROOT_DIR` to the directory of the current file, if in doubt with regards to path, always use relative to `PROJECT_ROOT_DIR`
PROJECT_ROOT_DIR = Path(__file__).resolve().parent
PACKAGE_NAME = get_package_name()
# Uncomment if library can still function if extensions fail to compile
# (e.g. slower, python fallback).
# Don't allow failure if cibuildwheel is running.
# ALLOWED_TO_FAIL = os.environ.get("CIBUILDWHEEL", "0") != "1"
ALLOWED_TO_FAIL = False
REMOVE_HTML_ANNOTATION_FILES = True
PACKAGE_DIR = PROJECT_ROOT_DIR / PACKAGE_NAME
PROJECT_C_SOURCE_DIR_NAME = "sources"
PROJECT_C_SOURCE_DIR = PROJECT_ROOT_DIR / PROJECT_C_SOURCE_DIR_NAME
C_SOURCE_FILES = [str(x) for x in PROJECT_C_SOURCE_DIR.rglob("*.c")]

# Constants related to .pyx, i.e. Cython source files
PYX_SOURCE_DIR_NAME = PROJECT_C_SOURCE_DIR_NAME  # can be different
PYX_SOURCE_DIR = PROJECT_ROOT_DIR / PYX_SOURCE_DIR_NAME
PYX_SOURCE_FILES = [str(x) for x in PYX_SOURCE_DIR.rglob("*.pyx")]
C_SOURCE_FILES_GENERATED_FROM_CYTHON = [str(Path(x).with_suffix(".c")) for x in PYX_SOURCE_FILES]

INCLUDE_DIR_NAME = "include"
INCLUDE_DIR = PROJECT_ROOT_DIR / INCLUDE_DIR_NAME
INCLUDE_FILES = [str(x) for x in INCLUDE_DIR.rglob("*.h")]

LANGUAGE = "C"
C_EXTENSION_MODULE_NAME = "_c_extension"

# Log the constants
LOGGER.info(f"`PACKAGE_NAME` = {PACKAGE_NAME}")
LOGGER.info(f"`ALLOWED_TO_FAIL` = {ALLOWED_TO_FAIL}")
LOGGER.info(f"`C_SOURCE_FILES` = {C_SOURCE_FILES}")
LOGGER.info(f"`PYX_SOURCE_FILES` = {PYX_SOURCE_FILES}")


def where_am_i() -> "Path":
    """Checks if the script is being run in the correct directory (`PROJECT_ROOT_DIR`)."""
    current_dir = Path.cwd()
    if current_dir != PROJECT_ROOT_DIR:
        raise RuntimeError(f"Please run this script in the directory: {PROJECT_ROOT_DIR}")

    # Check for at least one required file in `PROJECT_ROOT_DIR`
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


def check_dir_files_existence():
    def get_corresponding_c_files(pyx_files, source_dirs):
        return {
            Path(pyx_file).with_suffix(".c")
            for pyx_file in pyx_files
            for source_dir in source_dirs
            if (source_dir / Path(pyx_file).with_suffix(".c").name).exists()
        }

    if not PROJECT_C_SOURCE_DIR.exists():
        raise RuntimeError(
            f"`PROJECT_C_SOURCE_DIR` = {PROJECT_C_SOURCE_DIR} does not exist!\nScanning files in `PROJECT_ROOT_DIR`: {list_dir_contents(PROJECT_ROOT_DIR, 0)}"
        )

    if not C_SOURCE_FILES:
        raise RuntimeError(f"""`C_SOURCE_FILES` is empty!
                            Scanning `PROJECT_ROOT_DIR` for files up to 0 level:
                            {list_dir_contents(str(PROJECT_ROOT_DIR), 0)};
                            Scanning `PROJECT_C_SOURCE_DIR` for files up to 0 level:
                            {list_dir_contents(str(PROJECT_C_SOURCE_DIR), 0)}
                            """)

    def check_missing_c_files(pyx_files, source_dirs):
        c_files = get_corresponding_c_files(pyx_files, source_dirs)
        missing_c_files = {
            Path(pyx_file).with_suffix(".c")
            for pyx_file in pyx_files
            if Path(pyx_file).with_suffix(".c") not in c_files
        }

        if missing_c_files:
            raise RuntimeError(f"Missing .c files for .pyx files: {missing_c_files}")

        if not USE_CYTHON:
            check_missing_c_files()


def remove_cython_metadata(file_path):
    """
    Removes Cython metadata from a given C file.

    Args:
        file_path (str): The path to the C file from which to remove metadata.
    """
    with open(file_path) as file:
        lines = file.readlines()

    # Find the start and end of the metadata block
    start_index = next(
        (i for i, line in enumerate(lines) if line.strip() == "/* BEGIN: Cython Metadata"), None
    )
    end_index = next(
        (i for i, line in enumerate(lines) if line.strip() == "END: Cython Metadata */"), None
    )

    # If both start and end indices are found, remove the metadata
    if start_index is not None and end_index is not None:
        del lines[start_index : end_index + 1]

    # Write the modified lines back to the file
    with open(file_path, "w") as file:
        file.writelines(lines)
    LOGGER.info(f"Finished removing Cython metadata from {file_path}")


def extra_compile_args():
    """A function to get all the extra compile arguments for the extension modules.
    Define your own arguments here.
    """
    if os.name == "nt":  # Windows
        extra_compile_args = [
            "/O2",
        ]
    else:  # UNIX-based systems
        extra_compile_args = [
            "-O3",
            "-Werror",
            "-Wno-unreachable-code-fallthrough",
            "-Wno-deprecated-declarations",
            "-Wno-parentheses-equality",
            "-Wno-unreachable-code",  # TODO: This should no longer be necessary with Cython>=3.0.3
        ]
    extra_compile_args.append("-UNDEBUG")  # Cython disables asserts by default.
    return extra_compile_args


def get_extension_modules():
    # Relative to project root directory
    include_dirs = [str(INCLUDE_DIR)]
    LOGGER.info(f"in function `get_extension_modules`; `include_dirs` = {include_dirs}")

    # define each of the extensions yourself or use some functions to collate them
    custom_ext = Extension(
        f"{PACKAGE_NAME}.custom",  # anything within it can be import with `from simple_python_template.custom import (Custom, )` within Python
        [
            str(PROJECT_C_SOURCE_DIR / "custom.c")  # this is where the source C files is
        ],
        include_dirs=include_dirs,
        extra_compile_args=extra_compile_args(),
        language=LANGUAGE,
    )
    _c_extension_ext = Extension(
        f"{PACKAGE_NAME}.{C_EXTENSION_MODULE_NAME}",  # anything within it can be import with `from simple_python_template._c_extension import (Foo, )`
        [
            str(PROJECT_C_SOURCE_DIR / "foo.c"),
            *PYX_SOURCE_FILES,
        ],
        include_dirs=include_dirs,
        extra_compile_args=extra_compile_args(),
        language=LANGUAGE,
    )
    extensions = [
        # Extension(
        #     # Your .pyx file will be available to cpython at this location.
        #     f"{PACKAGE_NAME}.{C_EXTENSION_MODULE_NAME}",
        #     [
        #         # ".c" and ".pyx" source file paths
        #         *PYX_SOURCE_FILES,
        #         *C_SOURCE_FILES,
        #     ],
        #     include_dirs=include_dirs,
        #     extra_compile_args=extra_compile_args(),
        #     language=LANGUAGE,
        # ),
        _c_extension_ext,
        custom_ext,
    ]
    return extensions


def copy_output_to_cmd_buildlib(cmd):
    build_outputs = cmd.get_outputs()
    build_outputs_str = {str(output) for output in build_outputs}
    LOGGER.info(f"Outputs produced by `build` are: {build_outputs_str}")
    for output in build_outputs:
        output = Path(output)
        relative_extension = output.relative_to(cmd.build_lib)
        relative_extension_path = PROJECT_ROOT_DIR / relative_extension
        LOGGER.info(f"Copying file from `{output}` to `{relative_extension_path}`")
        shutil.copyfile(output, relative_extension_path)
        LOGGER.info("File copied successfully")


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


def build_c_extensions():
    """Builds the extension modules using pure C without Cython."""
    extensions = get_extension_modules()
    include_dirs = set()
    for extension in extensions:
        include_dirs.update(extension.include_dirs)
    include_dirs = list(include_dirs)

    dist = Distribution({"ext_modules": extensions})
    cmd = build_ext(dist)
    cmd.ensure_finalized()
    cmd.run()
    LOGGER.info(f"`cmd.build_lib` = {cmd.build_lib}")

    copy_output_to_cmd_buildlib(cmd)


if __name__ == "__main__":
    # actual build
    # pre-build checks; making sure `build.py` is in `PROJECT_ROOT_DIR`
    where_am_i()
    check_dir_files_existence()
    try:
        if USE_CYTHON:
            build_cython_extensions()
        else:
            build_c_extensions()  # Call the new function for pure C builds
    except Exception as err:
        LOGGER.exception(f"`build.py` has failed: error = {err}")
        if not ALLOWED_TO_FAIL:
            raise

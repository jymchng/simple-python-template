import logging
from logging import getLogger
import os
from pathlib import Path
import shutil
import sys

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

# Set ROOT_DIR to the directory of the current file, if in doubt with regards to path, always use relative to `ROOT_DIR`
ROOT_DIR = Path(__file__).resolve().parent


def where_am_i() -> "Path":
    """Checks if the script is being run in the correct directory (`ROOT_DIR`)."""
    current_dir = Path.cwd()
    if current_dir != ROOT_DIR:
        raise RuntimeError(f"Please run this script in the directory: {ROOT_DIR}")
    LOGGER.info(f"Running in the correct directory: {current_dir}")
    return ROOT_DIR


# pre-build checks; making sure `build.py` is in `ROOT_DIR`
where_am_i()


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
PACKAGE_NAME = get_package_name()
# Uncomment if library can still function if extensions fail to compile
# (e.g. slower, python fallback).
# Don't allow failure if cibuildwheel is running.
# ALLOWED_TO_FAIL = os.environ.get("CIBUILDWHEEL", "0") != "1"
ALLOWED_TO_FAIL = False
REMOVE_HTML_ANNOTATION_FILES = True
PACKAGE_DIR = ROOT_DIR / PACKAGE_NAME
C_SOURCE_DIR_NAME = "_c_src"
C_SOURCE_DIR = ROOT_DIR / PACKAGE_NAME / C_SOURCE_DIR_NAME
C_SOURCE_FILES = [str(x) for x in C_SOURCE_DIR.rglob("*.c")]

PYX_SOURCE_DIR_NAME = PACKAGE_NAME  # can be different
PYX_SOURCE_DIR = ROOT_DIR / PYX_SOURCE_DIR_NAME
PYX_SOURCE_FILES = [str(x) for x in PYX_SOURCE_DIR.rglob("*.pyx")]
C_SOURCE_FILES_GENERATED_FROM_CYTHON = [str(Path(x).with_suffix(".c")) for x in PYX_SOURCE_FILES]

LANGUAGE = "C"
C_EXTENSION_MODULE_NAME = "_c_extension"

# Log the constants
LOGGER.info(f"`PACKAGE_NAME` = {PACKAGE_NAME}")
LOGGER.info(f"`ALLOWED_TO_FAIL` = {ALLOWED_TO_FAIL}")
LOGGER.info(f"`C_SOURCE_FILES` = {C_SOURCE_FILES}")
LOGGER.info(f"`PYX_SOURCE_FILES` = {PYX_SOURCE_FILES}")


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
            "/O3",
            "/Wall",  # Enable all warnings
            "/Werror",  # Treat warnings as errors
            "/Wno-unreachable-code-fallthrough",  # Ignore fallthrough warnings
            "/Wno-deprecated-declarations",  # Ignore deprecated declarations
            "/Wno-parentheses-equality",  # Ignore parentheses equality warnings
            "/Wno-unreachable-code",  # Ignore unreachable code warnings
            "/sdl",
            "/guard:cf",
            "/utf-8",
            "/diagnostics:caret",
            "/w14165",
            "/w44242",
            "/w44254",
            "/w34287",
            "/w44296",
            "/w44365",
            "/w44388",
            "/w44464",
            "/w14545",
            "/w14546",
            "/w14547",
            "/w14549",
            "/w14555",
            "/w34619",
            "/w44774",
            "/w44777",
            "/w24826",
            "/w14905",
            "/w14906",
            "/w14928",
            "/W4",
            "/permissive-",
            "/volatile:iso",
            "/Zc:inline",
            "/Zc:preprocessor",
        ]
    else:  # UNIX-based systems
        extra_compile_args = [
            "-O3",
            "-Wall",
            "-Werror",
            # "-Wno-unreachable-code-fallthrough",
            # "-Wno-deprecated-declarations",
            # "-Wno-parentheses-equality",
            "-Wno-unreachable-code",  # TODO: This should no longer be necessary with Cython>=3.0.3
            "-U_FORTIFY_SOURCE",
            "-D_FORTIFY_SOURCE=3",
            "-fstack-protector-strong",
            "-fcf-protection=full",
            "-fstack-clash-protection",
            "-Wall",
            "-Werror",
            "-Wextra",
            # "-Wpedantic", # Cython error
            # "-Wconversion", # Cython error
            "-Wsign-conversion",
            # "-Wcast-qual",
            "-Wformat=2",
            "-Wundef",
            # "-Wshadow", # Cython error
            "-Wcast-align",
            "-Wunused",
            "-Wnull-dereference",
            # "-Wdouble-promotion", # Cython error
            "-Wimplicit-fallthrough",
            "-Werror=strict-prototypes",
            "-Wwrite-strings",
            # "-Wno-warning=discarded-qualifiers", # custom.c:44:39/30/47
            "-Wno-error=discarded-qualifiers", # custom.c:44:39/30/47
        ]
    extra_compile_args.append("-UNDEBUG")  # Cython disables asserts by default.
    return extra_compile_args


def get_extension_modules():
    # Relative to project root directory
    include_dirs = [
        str(PACKAGE_DIR),
        str(C_SOURCE_DIR),
    ]
    LOGGER.info(f"in function `get_extension_modules`; `include_dirs` = {include_dirs}")

    # define each of the extensions yourself or use some functions to collate them
    custom_ext = Extension(
        f"{PACKAGE_NAME}.custom", # anything within it can be import with `from simple_python_template.custom import (Custom, )` within Python
        [
            str(C_SOURCE_DIR / "custom.c") # this is where the source C files is
        ],
        include_dirs=include_dirs,
        extra_compile_args=extra_compile_args(),
        language=LANGUAGE,
    )
    _c_extension_ext = Extension(
        f"{PACKAGE_NAME}.{C_EXTENSION_MODULE_NAME}", # anything within it can be import with `from simple_python_template._c_extension import (Foo, )`
        [
            str(C_SOURCE_DIR / "foo.c"),
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
    for output in cmd.get_outputs():
        output = Path(output)
        relative_extension = output.relative_to(cmd.build_lib)
        LOGGER.info(f"Copying file from `{output}` to `{relative_extension}`")
        shutil.copyfile(output, relative_extension)
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
    try:
        if USE_CYTHON:
            build_cython_extensions()
        else:
            build_c_extensions()  # Call the new function for pure C builds
    except Exception as err:
        LOGGER.exception(f"`build.py` has failed: error = {err}")
        if not ALLOWED_TO_FAIL:
            raise

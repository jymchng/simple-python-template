import argparse
import logging
import os
import re
import shutil
import sys
from logging import getLogger
from typing import Optional


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)s] %(message)s",
    stream=sys.stdout,
)
LOGGER = getLogger(__name__)
LOGGER.info("Running `generate_ref_docs.py`...")

TO_SKIP_MODULE_NAMES = [
    "__init__",
    "__main__",
]


def find_project_root(start_path: str) -> Optional[str]:
    """
    Searches upwards from the start_path to find the project root directory.
    The project root is identified by the presence of any of the following files:
    pyproject.toml, requirements.txt, setup.cfg, setup.py.

    Args:
        start_path (str): The starting directory path to search from.

    Returns
    -------
        Optional[str]: The project root directory if found, otherwise None.
    """
    project_files = ["pyproject.toml", "requirements.txt", "setup.cfg", "setup.py"]
    current_path = start_path

    while current_path != os.path.dirname(current_path):  # while not at the root directory
        for project_file in project_files:
            if os.path.exists(os.path.join(current_path, project_file)):
                return current_path
        current_path = os.path.dirname(current_path)

    return None


def get_package_name_from_config(project_root: str) -> Optional[str]:
    """
    Retrieves package name from setup.cfg, setup.py, or pyproject.toml in project root directory.

    Args:
        project_root (str): The root directory of the project.

    Returns
    -------
        Optional[str]: The package name if found, otherwise None.
    """
    setup_cfg_path = os.path.join(project_root, "setup.cfg")
    setup_py_path = os.path.join(project_root, "setup.py")
    pyproject_toml_path = os.path.join(project_root, "pyproject.toml")

    if os.path.exists(setup_cfg_path):
        with open(setup_cfg_path) as f:
            for line in f:
                if line.startswith("name ="):
                    return line.split("=")[1].strip().strip('"').strip("'")

    if os.path.exists(setup_py_path):
        with open(setup_py_path) as f:
            for line in f:
                match = re.search(r'name\s*=\s*[\'"]([^\'"]+)[\'"]', line)
                if match:
                    return match.group(1)

    if os.path.exists(pyproject_toml_path):
        with open(pyproject_toml_path) as f:
            for line in f:
                if line.strip().startswith("name ="):
                    return line.split("=")[1].strip().strip('"').strip("'")

    return None


def generate_docs(package_name: str, output_dir: str, project_root: str, force: bool) -> None:
    """
    Generates API reference documentation for a given Python package.
    The documentation is generated in the specified output directory.

    Args:
        package_name (str): The name of the package directory.
        output_dir (str): The directory where the documentation will be generated.
        project_root (str): The root directory of the project.
        force (bool): Whether to overwrite existing .md files.
    """
    output_dir = os.path.join(project_root, output_dir)
    LOGGER.info(f"`output_dir` = {output_dir}")

    if force and os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    package_path = os.path.join(project_root, package_name)
    for root, _, files in os.walk(package_path):
        for file in files:
            if file.endswith((".py", ".pyi")):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, package_path)
                if ".pyi" in relative_path:
                    to_replace_no = 4
                else:
                    to_replace_no = 3
                module_name = relative_path.replace(os.sep, ".")[
                    :-to_replace_no
                ]  # Strip .py or .pyi
                LOGGER.info(f"`relative_path` = {relative_path}")
                LOGGER.info(f"`module_name` = {module_name}")

                if any(to_skip in module_name for to_skip in TO_SKIP_MODULE_NAMES):
                    continue

                md_file_name = file.replace(".pyi", ".md").replace(".py", ".md")
                md_file_path = os.path.join(output_dir, md_file_name)
                LOGGER.info(f"`md_file_path` = {md_file_path}")

                if not force and os.path.exists(md_file_path):
                    print(f"Skipping existing file: {md_file_path}")
                    continue

                with open(md_file_path, "w") as md_file:
                    md_file.write(f"# {file} Reference\n\n")
                    md_file.write(f"::: {package_name}.{module_name}")

    print(f"API reference documentation has been generated in {output_dir}")


def main() -> None:
    """
    Main entry point for the script.
    Parses command-line arguments and generates API reference documentation.
    """
    parser = argparse.ArgumentParser(
        description="Generate API reference docs for a Python package."
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="docs/reference",
        help="The directory where the documentation will be generated.",
    )
    parser.add_argument(
        "--package-name", type=str, default=None, help="The name of the package directory."
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing .md files.")
    args = parser.parse_args()
    LOGGER.info(f"`args` passed: {args}")

    current_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = find_project_root(current_dir)

    if not project_root:
        print("Error: Could not find project root directory.")
        exit(1)

    package_name = (args.package_name or get_package_name_from_config(project_root)).replace(
        "-", "_"
    )
    if not package_name:
        print("Error: Could not determine package name.")
        exit(1)
    LOGGER.info(f"`package_name` = {package_name}")
    LOGGER.info(f"`project_root` = {project_root}")
    generate_docs(package_name, args.output_dir, project_root, args.force)


if __name__ == "__main__":
    main()

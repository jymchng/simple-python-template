# Download and Installation

## Downloading of the Repository

### By cloning it

To download the template repository, you can use `git`.

Clone it using HTTPS:

```bash
git clone https://github.com/jymchng/simple-python-template.git
```

Clone it using SSH:

```bash
git clone git@github.com:jymchng/simple-python-template.git
```

Then, remove the `.git` folder using:

```bash
rm -fr .git
```

### By forking it

Please refer to the [GitHub documentation on forking](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo).

## Download using the GitHub User Interface

Please refer to the GitHub documentation on [how to create a repository from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).

## Installation of the Tools

!!! Assumptions
    The current working directory must be at your `PROJECT_ROOT_DIR` (refer to [definitions](./definitions.md) for its definition) (e.g. in the template repository, it is named `simple-python-template`).

Run the following to bootstrap your installation of the tools.

```bash
bash init.sh
```

You will be instructured by the bash script on the installations of the tools. For the list of tools that are recommended, please see [here](../general-tools.md).

## Selection of the Build Tool

[`poetry`](https://python-poetry.org/) is selected as the build tool for no particular reason.

[`hatch`](https://hatch.pypa.io/latest/) and [`pdm`](https://pdm-project.org/en/latest/) are both very strong contenders but may be more difficult to use.

For example, `hatch` allows for testing across a matrix of Python versions and some meta-variables ([Reference](https://hatch.pypa.io/1.7/config/environment/advanced/#matrix)), which to the current knowledge of the author, something that `poetry` does not provide. However, it is not clear how one can build C extension modules using `hatch` or `pdm` as the build tool, as they do not seem to support arbitrary `build.py` script.

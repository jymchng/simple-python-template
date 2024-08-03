#!/bin/bash

# Check if the virtual environment directory exists
if [ ! -d "./.venv" ]; then
    echo "Error: Virtual environment not found at './.venv'."
    echo "Please create a virtual environment or change the path."
    exit 1
fi

activate () {
  . ../.venv/bin/activate
}

# Activate the virtual environment
echo "Activating virtual environment..."
ROOT_DIR=`dirname $0`
cd $ROOT_DIR
activate

# Check if the Python executable is from the virtual environment
if ! which python | grep -q "./.venv/bin/python"; then
    echo "Error: Python is not from the virtual environment."
    exit 1
else
    echo "Python located at $(which python)"
fi

# Unset PYTHON_HOME if it exists
PYTHONPATH=$(which python)

# Configure poetry
poetry config virtualenvs.in-project true
poetry env use

echo "Virtual environment activated successfully."

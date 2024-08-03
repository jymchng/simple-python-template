#!/usr/bin/env bash

# Function to install the desired Python version using pyenv
install_python_version() {
    echo "Installing Python version '$PYTHON_VERSION' using pyenv..."
    pyenv install "$PYTHON_VERSION" || { echo "Error: Failed to install Python version '$PYTHON_VERSION'."; exit 1; }
}

# Check if an argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <python_version>"
    echo "Example: $0 3.8 or $0 3.8.17"
    exit 1
fi

PYTHON_VERSION="$1"
PYENV_ROOT="$HOME/.pyenv"  # Adjust this if your PYENV_ROOT is different

# Check if the exact version exists
EXACT_VERSION_DIR="$PYENV_ROOT/versions/$PYTHON_VERSION"

if [ -d "$EXACT_VERSION_DIR" ]; then
    # Use the exact version if it exists
    LARGEST_VERSION="$PYTHON_VERSION"
else
    # Find the largest version matching the specified major.minor version
    LARGEST_VERSION=""

    for version in "$PYENV_ROOT/versions/$PYTHON_VERSION."*; do
        if [ -d "$version" ]; then
            # Extract the version number
            version_number="${version##*/}"  # Get the last part of the path
            if [[ -z "$LARGEST_VERSION" || "$version_number" > "$LARGEST_VERSION" ]]; then
                LARGEST_VERSION="$version_number"
            fi
        fi
    done

    if [ -z "$LARGEST_VERSION" ]; then
        # If no matching version is found, ask the user if they want to install it
        read -p "Python version '$PYTHON_VERSION' not found. Do you want to install it using pyenv? (y/n): " response
        if [[ "$response" == "y" || "$response" == "Y" ]]; then
            install_python_version
            # Rerun the script with the same argument
            exec "$0" "$PYTHON_VERSION" || { echo "Error: Failed to rerun the script."; exit 1; }
            exit 0  # Exit with success after rerunning
        else
            echo "Exiting without installing Python version '$PYTHON_VERSION'."
            exit 1
        fi
    fi
fi

# Check if the .venv folder exists
if [ -d ".venv" ]; then
    read -p ".venv folder already exists. Do you want to override it? (y/n): " response
    if [[ "$response" != "y" && "$response" != "Y" ]]; then
        echo "Exiting without creating a new virtual environment."
        exit 1
    fi
    # Optionally, remove the existing .venv folder
    rm -rf .venv || { echo "Error: Failed to remove existing .venv folder."; exit 1; }
fi

# Use the found version to create a virtual environment
PYTHON_EXEC="$PYENV_ROOT/versions/$LARGEST_VERSION/bin/python"

if [ -x "$PYTHON_EXEC" ]; then
    echo "Creating virtual environment using $PYTHON_EXEC..."
    "$PYTHON_EXEC" -m venv .venv || { echo "Error: Failed to create virtual environment."; exit 1; }
    echo "Virtual environment created at $(pwd)/.venv"
    echo "You can activate it by running the command: \`source ./.venv/bin/activate\`"
    exit 0  # Exit with success after creating the virtual environment
else
    echo "Error: Python executable not found in $PYENV_ROOT/versions/$LARGEST_VERSION/bin/"
    exit 1
fi

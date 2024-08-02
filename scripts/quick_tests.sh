#!/bin/bash

# Find the largest version in the ./dist directory
largest_version=$(ls ./dist/simple_python_template-*.tar.gz 2>/dev/null | sort -V | tail -n 1)

# Check if a version was found
if [[ -z "$largest_version" ]]; then
    echo "No package found in ./dist. Attempting to build the package..."
    if ! poetry build --format sdist; then  # Fail if poetry build fails
        echo "Poetry build failed. Exiting."
        exit 1
    fi
    # Re-check for the largest version after building
    largest_version=$(ls ./dist/simple_python_template-*.tar.gz 2>/dev/null | sort -V | tail -n 1)

    # Check again if a version was found after building
    if [[ -z "$largest_version" ]]; then
        echo "No package found in ./dist after building."
        exit 1
    fi
fi

# Check if the package is already installed
package_name=$(basename "$largest_version" | sed 's/-[0-9].*//')

if pip show "$package_name" > /dev/null 2>&1; then
    echo "Uninstalling existing package $package_name..."
    pip uninstall -y "$package_name"
fi

# Install the largest version
echo "Installing $largest_version..."
pip install "$largest_version"

# Run pytest with the installed package
echo "Running tests with pytest..."
python -m pytest tests

#!/usr/bin/env bash
#encoding=utf8

function install_chocolatey() {
    echo "Chocolatey is not installed. Do you want to install it? (yes/no)"
    read -r response
    if [[ "$response" == "yes" || "$response" == "y" ]]; then
        echo "Installing Chocolatey..."
        @powershell -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
        echo "Chocolatey installed successfully."
    else
        echo "Chocolatey installation skipped."
        exit 1
    fi
}

function check_installed_make() {
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        # Check for make in Windows
        which make > /dev/null
        if [ $? -ne 0 ]; then
            echo "Installing Make using Chocolatey..."
            # Ensure Chocolatey is installed
            if ! command -v choco &> /dev/null; then
                install_chocolatey
            fi
            choco install make -y
        fi
    else
        # Assuming a Debian-based system for installation
        which make > /dev/null
        if [ $? -ne 0 ]; then
            echo "Installing Make..."
            sudo apt-get update
            sudo apt-get install -y make
        fi
    fi
}

function check_installed_pip() {
   ${PYTHON} -m pip > /dev/null
   if [ $? -ne 0 ]; then
        echo_block "Installing Pip for ${PYTHON}"
        curl https://bootstrap.pypa.io/get-pip.py -s -o get-pip.py
        ${PYTHON} get-pip.py
        rm get-pip.py
   fi
}

# Check which python version is installed
function check_installed_python() {
    if [ -n "${VIRTUAL_ENV}" ]; then
        echo "Please deactivate your virtual environment before running setup.sh."
        echo "You can do this by running 'deactivate'."
        exit 2
    fi

    HAVE_PYTHON=0

    for v in 8 9 10 11 12
    do
        PYTHON="python3.${v}"
        which $PYTHON
        if [ $? -eq 0 ]; then
            echo "${PYTHON} installed"
            HAVE_PYTHON=1
            break
        fi
    done

    if [ $HAVE_PYTHON -eq 1 ]; then
        check_installed_pip
        return 0
    else
        echo "No usable python found. Please make sure to have python3.8 or newer installed."
        exit 1
    fi
}

function is_function_appended() {
    local target_file
    if [ -f ~/.bashrc ]; then
        target_file=~/.bashrc
    elif [ -f ~/.bash_profile ]; then
        target_file=~/.bash_profile
    else
        return 1
    fi

    # Check if the function is already in the target file
    if grep -q "activate_venv_in_python_projects" "$target_file"; then
        echo "$target_file"  # Return the file name
        return 0
    fi
    return 1
}

function append_activate_venv_function() {
    local appended_file
    appended_file=$(is_function_appended)
    if [ $? -eq 0 ]; then
        echo "The activate_venv_in_python_projects function is already appended in $appended_file."
        return
    fi

    read -p "Do you want to append the activate_venv_in_python_projects function to your ~/.bashrc or ~/.bash_profile? (yes/no) " response
    if [[ "$response" == "yes" || "$response" == "y" ]]; then
        # Determine the appropriate file to append to
        if [ -f ~/.bashrc ]; then
            target_file=~/.bashrc
        elif [ -f ~/.bash_profile ]; then
            target_file=~/.bash_profile
        else
            echo "No suitable file found to append the function."
            return
        fi

        # Append the function to the target file
        cat << 'EOF' >> "$target_file"

activate_venv_in_python_projects() {
    # Check if already in a virtual environment
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "Already in a virtual environment: $VIRTUAL_ENV"
        return
    fi

    # Check if we are in a subdirectory of `python_projects`
    dir="$PWD"
    while [[ "$dir" != "/" ]]; do
        if [[ "$dir" == *"/python_projects/"* ]] && [[ -d "$dir/.venv" ]]; then
            source "$dir/.venv/bin/activate"
            echo "Activated virtual environment: $dir/.venv"
            break
        fi
        dir=$(dirname "$dir")
    done
}
EOF

        echo "Function appended to $target_file. Please restart your terminal or run 'source $target_file' to use it."
    else
        echo "Function not appended."
    fi
}

function check_installed_pre_commit() {
    if ! command -v pre-commit &> /dev/null; then
        echo "pre-commit is not installed. Do you want to install it? (yes/no)"
        read -r response
        if [[ "$response" == "yes" || "$response" == "y" ]]; then
            echo "Installing pre-commit..."
            # Assuming pip is available for installation
            pip install pre-commit
            echo "pre-commit installed successfully."
        else
            echo "pre-commit installation skipped."
            exit 1
        fi
    else
        echo "pre-commit is already installed."
    fi
}

function check_installed_cppcheck() {
    if ! command -v cppcheck &> /dev/null; then
        echo "cppcheck is not installed. Do you want to install it? (yes/no)"
        read -r response
        if [[ "$response" == "yes" || "$response" == "y" ]]; then
            if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
                echo "Installing cppcheck using Chocolatey..."
                choco install cppcheck -y
            else
                echo "Installing cppcheck..."
                sudo apt-get update
                sudo apt-get install -y cppcheck
            fi
            echo "cppcheck installed successfully."
        else
            echo "cppcheck installation skipped."
            exit 1
        fi
    else
        echo "cppcheck is already installed."
    fi
}

function check_installed_clang_format() {
    if ! command -v clang-format &> /dev/null; then
        echo "clang-format is not installed. Do you want to install it? (yes/no)"
        read -r response
        if [[ "$response" == "yes" || "$response" == "y" ]]; then
            if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
                echo "Installing clang-format using Chocolatey..."
                choco install llvm -y  # clang-format is included in LLVM
            else
                echo "Installing clang-format..."
                sudo apt-get update
                sudo apt-get install -y clang-format
            fi
            echo "clang-format installed successfully."
        else
            echo "clang-format installation skipped."
            exit 1
        fi
    else
        echo "clang-format is already installed."
    fi
}

function install_pyenv() {
    if ! command -v pyenv &> /dev/null; then
        echo "Pyenv is not installed. Installing Pyenv..."

        # Check if the user is on Windows
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
            echo "Note: Pyenv does not officially support Windows and does not work outside the Windows Subsystem for Linux."
            echo "For Windows users, we recommend using @kirankotari's pyenv-win fork, which installs native Windows Python versions."
            echo "You can find it here: https://github.com/pyenv-win/pyenv-win"
        else
            # Attempt to install pyenv and exit if it fails
            if ! curl https://pyenv.run | bash; then
                echo "Failed to install Pyenv. Exiting."
                exit 1
            fi
            echo "Pyenv installed successfully."
        fi
    else
        echo "Pyenv is already installed."
    fi
}

# Ask the user for permission to make scripts executable
read -p "Do you want to make all scripts in the 'scripts' directory executable? (yes/no): " response
if [[ "$response" == "yes" || "$response" == "y" ]]; then
    chmod +x scripts/*.sh 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "All scripts in the 'scripts' directory have been made executable."
    else
        echo "Error: Failed to make scripts executable. Please check permissions."
    fi
else
    echo "Skipping making scripts executable."
fi

if [ -d $HOME/.pyenv ]; then
    echo "\`pyenv\` is already installed"
else
    install_pyenv
fi

# Check if pyenv commands are already in ~/.bashrc
if
   grep -q 'eval "\$(pyenv init -)"' ~/.bashrc; then
    echo "Pyenv access is already configured in ~/.bashrc."
else
    # Ask the user if they want quicker access to pyenv on terminal activation
    read -p "Do you want quicker access to 'pyenv' on terminal activation? (yes/no): " pyenv_response

    if [[ "$pyenv_response" == "yes" || "$pyenv_response" == "y" ]]; then
        echo '' >> ~/.bashrc
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
        echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
        echo 'eval "$(pyenv init -)"' >> ~/.bashrc
        echo "Pyenv access added to ~/.bashrc. Please restart your terminal."
    else
        echo "For more information on setting up Pyenv, visit: https://github.com/pyenv/pyenv?tab=readme-ov-file#set-up-your-shell-environment-for-pyenv"
    fi
fi

# Call the function to prompt the user
append_activate_venv_function

# Check for Make
check_installed_make
check_installed_python
check_installed_pip
check_installed_pre_commit

# Check for cppcheck and clang-format; for C extensions
check_installed_cppcheck
check_installed_clang_format

# Ask if the user wants to rename the package now
read -p "Do you want to rename your package now? (yes/no): " rename_response

if [[ "$rename_response" == "yes" || "$rename_response" == "y" ]]; then
    # Prompt the user for the package name and GIT_USERNAME
    read -p "Enter the name for your package: " PACKAGE_NAME
    read -p "Enter your GIT_USERNAME: " GIT_USERNAME
    read -p "Enter your GIT_REPONAME: " GIT_REPONAME

    # Define the directories and files to search
    SEARCH_DIRS=("/assets" "/tests" "README.md" "LICENSE" "simple_python_template")

    # Loop through each directory and file
    for item in "${SEARCH_DIRS[@]}"; do
        if [[ -e "$item" ]]; then
            echo "Processing $item..."
            # Use sed to replace instances of simple_python_template, simple-python-template, GIT_USERNAME, and GIT_REPONAME
            sed -i.bak -e "s/simple_python_template/$PACKAGE_NAME/g" \
                    #    -e "s/simple-python-template/$PACKAGE_NAME/g" \
                       -e "s/jymchng/$GIT_USERNAME/g" \
                       -e "s/simple-python-template/$GIT_REPONAME/g" "$item"
        else
            echo "$item does not exist, skipping."
        fi
    done

    echo "Replacement complete."
else
    echo "Package renaming skipped."
fi

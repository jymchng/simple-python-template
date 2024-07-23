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

    for v in 12 11 10 9
    do
        PYTHON="python3.${v}"
        which $PYTHON
        if [ $? -eq 0 ]; then
            echo "using ${PYTHON}"
            check_installed_pip
            return
        fi
    done

    echo "No usable python found. Please make sure to have python3.9 or newer installed."
    exit 1
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

# Call the function to prompt the user
append_activate_venv_function

# Call the function to prompt the user
append_activate_venv_function

# Check for Make
check_installed_make
check_installed_python
check_installed_pip
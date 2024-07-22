#!/usr/bin/env bash
#encoding=utf8

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
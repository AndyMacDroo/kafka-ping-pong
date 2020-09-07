#!/usr/bin/env bash

function check_and_install_virtualenv_if_required() {
    IS_VIRTUALENV_INSTALLED=$(which virtualenv)
    if [ -z ${IS_VIRTUALENV_INSTALLED} ] && [ -z ${SHOULD_INSTALL_VIRTUALENV} ]; then
        echo -e "virtualenv command not found. Closing. Please install virtualenv:\n pip install virtualenv"
        exit 1
    elif [ -z ${IS_VIRTUALENV_INSTALLED} ] && [ ${SHOULD_INSTALL_VIRTUALENV} ] && [ ${SHOULD_INSTALL_VIRTUALENV} == true ]; then
        echo "Installing virtualenv"
        pip install virtualenv
    fi
}
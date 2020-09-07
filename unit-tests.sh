#!/usr/bin/env bash

IS_ERROR=false

if [ -z "${PROJECT_DIRECTORY}" ]; then
    PROJECT_DIRECTORY=${PWD}
fi

create_virtualenv() {
    echo -e "[$1]: Creating virtualenv..."
    virtualenv $2/venv
    # shellcheck source=./unit-tests.sh
    source $2/venv/bin/activate
}

remove_virtualenv() {
    deactivate
    echo -e "[$1]: Clearing up venv directory: $1/venv/"
    rm -rf $2/services/$1/venv/
}

install_requirements() {
    echo -e "[$1]: Installing requirements.txt"
    pip install -r $2/requirements.txt
}

unit_tests() {
    echo -e "[$1]: Running unit tests..."
    python -m unittest discover $2/services/$1 "*_test.py"
}
# shellcheck source=./unit-tests.sh
source "${PROJECT_DIRECTORY}"/bin/scripts/pre-requisites.sh
check_and_install_virtualenv_if_required

for dir in "${PROJECT_DIRECTORY}"/services/*/
do
    SERVICE_NAME=$(basename ${dir})

    create_virtualenv "${SERVICE_NAME}" "${dir}"
    install_requirements "${SERVICE_NAME}" "${dir}"
    unit_tests "${SERVICE_NAME}" "${PROJECT_DIRECTORY}"
    EXIT_CODE=$?
    remove_virtualenv "${SERVICE_NAME}" "${PROJECT_DIRECTORY}"
    if [ $EXIT_CODE != 0 ]; then
        IS_ERROR=true
    fi
    if [ $IS_ERROR == true ]; then
        echo -e "[${SERVICE_NAME}]: ERROR - Some of the unit tests failed."
        exit 1
    fi
done
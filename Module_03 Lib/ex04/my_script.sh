#!/bin/bash

# This script will create a virtual environment and install the requirements for the project.
# Run this script witn 'source my_script.sh' to get the virtual environment activated.

bash clean_repo.sh

python3 -m venv ~/sgoinfre/django_venv
source ~/sgoinfre/django_venv/bin/activate

if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo '✅ Virtual environment activated.'
    echo '⭐ Installing requirements...'
    echo "💻 Python version: $(which python)"
else
    echo '❌ Failed to activate virtual environment.'
fi

pip install -r requirement.txt

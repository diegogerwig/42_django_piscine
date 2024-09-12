#!/bin/sh

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

django-admin startproject Django_project

cd Django_project

python manage.py startapp helloworld_app

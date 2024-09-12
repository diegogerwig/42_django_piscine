#!/bin/sh

bash clean_repo.sh

~/sgoinfre/django_venv
source ~/sgoinfre/django_venv/bin/activate


if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo '✅ Virtual environment activated.'
    echo '⭐ Installing requirements...'
    echo "💻 Python version: $(which python)"
else
    echo '❌ Failed to activate virtual environment.'
fi

pip install -r requirement.txt

django-admin startproject helloworld_project

cd helloworld_project

python manage.py startapp helloworld

# python manage.py migrate

# python manage.py runserver
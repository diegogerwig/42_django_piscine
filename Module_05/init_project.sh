#!/bin/sh

bash ./src/clean_repo.sh

python3 -m venv ~/sgoinfre/django_venv
source ~/sgoinfre/django_venv/bin/activate

if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo '✅ Virtual environment activated.'
    echo '⭐ Installing requirements...'
    echo "💻 Python version: $(which python)"
else
    echo '❌ Failed to activate virtual environment.'
fi

pip install -r requirements.txt

echo "🐳 Starting Docker..."
docker stop $(docker ps -q)
docker rm $(docker ps -aq)
docker-compose up --build -d

if docker ps | grep -q "postgres" && docker ps | grep -q "adminer" && docker ps | grep -q "pgadmin"; then
    echo "✅ Docker is running."
else
    echo "❌ Docker failed to start."
fi

bash ./src/create_django_project.sh

bash ./src/create_app_ex00.sh
bash ./src/create_app_ex01.sh

bash ./src/run_project.sh

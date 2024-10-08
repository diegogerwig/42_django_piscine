#!/bin/sh

bash ./src/clean_repo.sh

python3 -m venv ~/sgoinfre/django_venv
source ~/sgoinfre/django_venv/bin/activate

if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo '✅ Virtual environment activated.'
    echo "💻 Python version: $(which python)"
    echo -e '⭐ Installing requirements...\n'
else
    echo '❌ Failed to activate virtual environment.'
fi

pip install -r requirements.txt

echo -e "\n🐳 Starting Docker..."
docker stop $(docker ps -q)
docker rm $(docker ps -aq)
docker-compose up --build -d

if docker ps | grep -q "postgres" && docker ps | grep -q "adminer" && docker ps; then
    echo -e "✅ Docker is running.\n"
else
    echo -e "❌ Docker failed to start.\n"
fi

bash ./src/create_django_project.sh

bash ./src/create_app_ex00.sh
bash ./src/create_app_ex01.sh
bash ./src/create_app_ex02.sh
bash ./src/create_app_ex03.sh
bash ./src/create_app_ex04.sh
bash ./src/create_app_ex05.sh
bash ./src/create_app_ex06.sh
bash ./src/create_app_ex07.sh
bash ./src/create_app_ex08.sh
bash ./src/create_app_ex09.sh
bash ./src/create_app_ex10.sh

bash ./src/run_project.sh

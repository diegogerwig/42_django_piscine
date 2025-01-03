#!/bin/sh

activate_venv() {
    source ~/sgoinfre/django_venv/bin/activate
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        echo '✅ Virtual environment activated.'
        echo "💻 Python location: $(which python) | Version: $(python --version 2>&1)"
        echo -e '⭐ Virtual environment ready\n'
    else
        echo '❌ Failed to activate virtual environment.'
        exit 1
    fi
}

run_project() {
    bash ./src/run_project.sh
}

full_init() {
    bash ./src/clean_repo.sh

    python3 -m venv ~/sgoinfre/django_venv
    activate_venv
    
    pip install -r requirements.txt

    echo -e "\n🐳 Starting Docker..."
    docker stop $(docker ps -q) 2>/dev/null || true
    docker rm $(docker ps -aq) 2>/dev/null || true
    docker-compose up --build -d

    if docker ps | grep -q "postgres" && docker ps | grep -q "adminer" && docker ps; then
        echo -e "✅ Docker is running.\n"
    else
        echo -e "❌ Docker failed to start.\n"
        exit 1
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

    run_project
}

case "$1" in
    -up)
        activate_venv
        run_project
        ;;
    "")
        full_init
        ;;
    *)
        echo "❌ Invalid argument: $1"
        echo "Usage: source $0 [-up]"
        echo "  no args  : Full initialization"
        echo "  -up     : Just activate venv and run project"
        return 1  
        ;;
esac
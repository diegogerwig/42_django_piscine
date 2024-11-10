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

    bash ./src/create_django_project.sh
    bash ./src/create_app_account.sh
    bash ./src/create_app_chat.sh

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
<<<<<<< HEAD
        echo "  no args : Full initialization"
        echo "  -up     : Just activate venv and run project"
=======
        echo "  no args  : Full initialization"
        echo "  -up      : Just activate venv and run project"
>>>>>>> refs/remotes/origin/main
        return 1  
        ;;
esac
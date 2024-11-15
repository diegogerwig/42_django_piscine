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
    # Instalar daphne si no está instalado
    pip install daphne >/dev/null 2>&1

    # Obtener el PID de cualquier proceso existente
    DAPHNE_PID=$(pgrep -f "daphne.*d09.asgi:application" || echo "")
    DJANGO_PID=$(pgrep -f "python.*manage.py.*runserver" || echo "")

    # Matar procesos existentes si existen
    if [ ! -z "$DAPHNE_PID" ]; then
        echo "🔄 Stopping existing daphne server (PID: $DAPHNE_PID)..."
        kill -9 $DAPHNE_PID
    fi
    if [ ! -z "$DJANGO_PID" ]; then
        echo "🔄 Stopping existing Django server (PID: $DJANGO_PID)..."
        kill -9 $DJANGO_PID
    fi

    # Ir al directorio del proyecto
    cd d09

    # Aplicar migraciones
    echo "🔄 Applying migrations..."
    python manage.py makemigrations >/dev/null 2>&1
    python manage.py migrate >/dev/null 2>&1

    # Configurar la variable de entorno DJANGO_SETTINGS_MODULE
    export DJANGO_SETTINGS_MODULE=d09.settings
    export PYTHONPATH=$(pwd):$PYTHONPATH

    # Intentar iniciar daphne con la configuración correcta
    echo "🚀 Starting daphne server..."
    if python -m daphne -b 0.0.0.0 -p 8000 d09.asgi:application; then
        echo "✅ Daphne server running"
    else
        echo " Daphne failed to start, falling back to Django development server..."
        python manage.py runserver
    fi
}

full_init() {
    bash ./src/clean_repo.sh

    python3 -m venv ~/sgoinfre/django_venv
    activate_venv
    
    # Asegurarse de que daphne está en requirements.txt si no está
    if ! grep -q "daphne==4.0.0" requirements.txt; then
        echo "daphne==4.0.0" >> requirements.txt
    fi
    if ! grep -q "channels==4.0.0" requirements.txt; then
        echo "channels==4.0.0" >> requirements.txt
    fi
    
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
        echo "  no args : Full initialization"
        echo "  -up     : Just activate venv and run project"
        return 1  
        ;;
esac
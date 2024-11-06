
# Variables
VENV_PATH = ~/sgoinfre/django_venv
PYTHON = python3
PIP = pip

all: clean venv install docker apps run

clean:
	bash ./src/clean_repo.sh

venv:
	$(PYTHON) -m venv $(VENV_PATH)
	@echo '🔄 Activating virtual environment...'
	@. $(VENV_PATH)/bin/activate && \
	if [ "$$VIRTUAL_ENV" != "" ]; then \
		echo '✅ Virtual environment activated.'; \
		echo "💻 Python version: $$(which python)"; \
		echo '⭐ Installing requirements...'; \
	else \
		echo '❌ Failed to activate virtual environment.'; \
		exit 1; \
	fi

install: venv
	@. $(VENV_PATH)/bin/activate && $(PIP) install -r requirements.txt

docker:
	@echo '🐳 Starting Docker...'
	-docker stop $$(docker ps -q)
	-docker rm $$(docker ps -aq)
	docker-compose up --build -d
	@if docker ps | grep -q "postgres" && docker ps | grep -q "adminer" && docker ps; then \
		echo "✅ Docker is running.\n"; \
	else \
		echo "❌ Docker failed to start.\n"; \
		exit 1; \
	fi

apps: 
	bash ./src/create_django_project.sh
	@for i in {0..10}; do \
		bash ./src/create_app_ex$$i.sh; \
	done

run:
	bash ./src/run_project.sh


.PHONY: all clean venv install docker apps run

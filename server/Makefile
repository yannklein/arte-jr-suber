clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build

compile:
	pip-compile requirements.in

install:
	pip install -r requirements.txt

install-dev:
	pip install -r dev.txt

test:
	pytest tests/ -v --cov=delivery

run:
	FLASK_APP=app.py flask run

run-dev:
	FLASK_APP=app.py FLASK_ENV=development flask run

start-dev:
	docker-compose up --build flask_app

venv:
	@echo "Creating virtual environment..."
	python3 -m venv venv
	@echo "Virtual environment created."
	@echo "To activate the virtual environment, run 'source venv/bin/activate' on Unix/Linux/MacOS or 'venv\\Scripts\\activate' on Windows."

compile-requirements:
	@echo "Compiling requirements..."
	. venv/bin/activate; pip install pip-tools; pip-compile requirements.in
	@echo "Requirements compiled into requirements.txt."

install-requirements:
	@echo "Installing dependencies..."
	. venv/bin/activate; pip install -r requirements.txt
	@echo "Dependencies installed."
	@echo "To activate the virtual environment, run '. venv/bin/activate' on Unix/Linux/MacOS or 'venv\\Scripts\\activate' on Windows."


.PHONY: cases clean compile install install-dev init_db upgrade db_dev drop_db test run run-dev venv
cases:
	@echo "Select an option:"
	@echo "1) start docker container"
	@echo "2) start flask server locally"
	@echo "3) create virtual environment and install dependencies"
	@read -p "Enter your choice (1/2): " CASE; \
	case "$$CASE" in \
		1) make start-dev ;; \
		2) make run-dev ;; \
		3) make venv compile-requirements install-requirements ;; \
		*) echo "Invalid option";; \
	esac

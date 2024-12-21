# Variables

PYTHON_INTERPRETER=python
PIP=pip
SHELL=/bin/bash
PYTHONPATH=$(shell pwd)

# 1: Create virtual environment
create-environment:
	$(PYTHON_INTERPRETER) -m venv venv

# 2: Install dependencies
install-dependencies: create-environment
	source venv/bin/activate && $(PIP) install pip-tools
	source venv/bin/activate && pip-compile requirements.in
	source venv/bin/activate && $(PIP) install -r ./requirements.txt

# 3. install code quality tools
install-dev-tools:
	source venv/bin/activate && $(PIP) install bandit safety flake8

# run code quality checks
security-checks: 
	source venv/bin/activate && safety check -r ./requirements/txt
	source venv/bin/activate && bandit -lll */*.py *c/*/*.py

# 4. run unit tests
unit-test:
	source venv/bin/activate && PYTHONPATH=$(PYTHONPATH) pytest -vvv

# run the test coverage check
check-coverage:
	source venv/bin/activate && PYTHONPATH=$(PYTHONPATH) pytest --cov=src test/

# run all dependencies
run-all: install-dependencies install-dev-tools security-checks unit-test check-coverage

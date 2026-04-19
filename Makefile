PYTHON_SYS = python3
PIP = $(VENV)/bin/pip
VENV = .venv
PYTHON_VENV = $(VENV)/bin/python3
MAIN = a_maze_ing.py
CONFIG = config.txt

.PHONY: all venv install run clean lint lint-strict build test-install

all: install build

$(VENV)/bin/activate: requirements.txt
	$(PYTHON_SYS) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install build wheel
	@touch $(VENV)/bin/activate

venv: $(VENV)/bin/activate

install: venv

run: venv
	$(PYTHON_VENV) $(MAIN) $(CONFIG)

clean:
	rm -rf $(VENV) dist build *.egg-info .mypy_cache .pytest_cache
	rm -rf maze.txt
	find . -name "__pycache__" -exec rm -rf {} + 
	find . -name "*.pyc" -exec rm -rf {} + 

lint: venv
	$(PYTHON_VENV) -m flake8 . --exclude=$(VENV),build,dist
	$(PYTHON_VENV) -m mypy . --exclude $(VENV) --ignore-missing-imports --disallow-untyped-defs

lint-strict: venv
	$(PYTHON_VENV) -m flake8 . --exclude=$(VENV),build,dist
	$(PYTHON_VENV) -m mypy . --exclude $(VENV) --strict

build: venv
	@rm -rf dist build *.egg-info
	@$(PYTHON_VENV) -m build
	@cp dist/*.whl .
	@rm -rf dist build *.egg-info

# installs the package in the current venv. to use it, you need to source the venv first
# source .venv/bin/activate

test-install: build
	@$(PIP) install --force-reinstall *.whl
PYTHON_SYS = python3
PIP = $(VENV)/bin/pip
VENV = venv
PYTHON_VENV = $(VENV)/bin/python
MAIN = a_maze_ing.py
CONFIG = config.txt

$(VENV)/bin/activate: requirements.txt
	$(PYTHON_SYS) -m venv $(VENV)
	$(PIP) install -r requirements.txt
	@touch $(VENV)/bin/activate

venv: $(VENV)/bin/activate

install: venv

run: venv
	$(PYTHON_VENV) $(MAIN) $(CONFIG)

clean:
	rm -rf $(VENV) maze.txt
	find . -name "__pycache__" -exec rm -rf {} + 
	find . -name "*.pyc" -exec rm -rf {} + 

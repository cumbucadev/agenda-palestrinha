.PHONY: install test lint fix-lint clean

PYTHON ?= python3
PATHSEP := /
ifeq ($(OS),Windows_NT)
PYTHON := py
VENV_BIN := .venv\Scripts
PATHSEP := \\
else
VENV_BIN := .venv/bin
endif

PIP := $(VENV_BIN)$(PATHSEP)pip
PYTEST := $(VENV_BIN)$(PATHSEP)pytest
RUFF := $(VENV_BIN)$(PATHSEP)ruff

install:
	$(PYTHON) -m venv .venv
	$(PIP) install -e ".[dev]"

test:
	$(PYTEST) tests/ -v

lint:
	$(RUFF) check .
	$(RUFF) format --check .

fix-lint:
	$(RUFF) check --fix .
	$(RUFF) format .

clean:
	$(PYTHON) -c "import os, shutil; [shutil.rmtree(os.path.join(root, d)) for root, dirs, files in os.walk('.') for d in dirs if d == '__pycache__']; [os.remove(os.path.join(root, f)) for root, dirs, files in os.walk('.') for f in files if f.endswith('.pyc')]"

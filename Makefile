.PHONY: install test lint fix-lint clean

install:
	python3 -m venv .venv
	.venv/bin/pip install -e ".[dev]"

test:
	.venv/bin/pytest tests/ -v

lint:
	.venv/bin/ruff check .
	.venv/bin/ruff format --check .

fix-lint:
	.venv/bin/ruff check --fix .
	.venv/bin/ruff format .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

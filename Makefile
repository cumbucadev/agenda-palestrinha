.PHONY: install test lint fix-lint clean install-npm run-server

install:
	uv sync --extra dev

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .

fix-lint:
	uv run ruff check --fix .
	uv run ruff format .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

install-npm:
	npm i

run-server:
	cd ./frontend/asserts/agenda-palestrinha && npm run liquido

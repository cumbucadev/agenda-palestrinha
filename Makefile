.PHONY: install test lint fix-lint clean install-npm run-server

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

install-npm:
	npm i

run-server:
	cd ./frontend/asserts/agenda-palestrinha && npm run liquido

update-liquido:
	npm up liquido
	cd ./frontend/asserts/ && npx liquido novo agenda-palestrinha --sim --tipo "mvc"  --linguagem "delegua"  --gerenciador "npm"

rename-folder:
	mv ./frontend/asserts/agenda-palestrinha ./frontend/asserts/agenda-palestrinha.old

copy-files:
	cp ./frontend/asserts/agenda-palestrinha.old/visoes/inicial.lmht ./frontend/asserts/agenda-palestrinha/visoes/inicial.lmht 
	cp ./frontend/asserts/agenda-palestrinha.old/rotas/inicial.delegua ./frontend/asserts/agenda-palestrinha/rotas/inicial.delegua
	cp ./frontend/asserts/agenda-palestrinha.old/estilos/principal.foles ./frontend/asserts/agenda-palestrinha/estilos/principal.foles
	
delete-old-folder:
	rm -rf ./frontend/asserts/agenda-palestrinha.old

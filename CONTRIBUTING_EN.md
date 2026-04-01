# Contributing

[Versão em Português](/CONTRIBUTING.md)

Thanks for taking the time to contribute! Every little bit of help counts!

## Prerequisites

- [Python 3.12+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [Make](https://www.gnu.org/software/make/)

## Local setup

1. Fork the repository and clone it:

```bash
git clone https://github.com/YOUR_USERNAME/agenda-palestrinha.git
cd agenda-palestrinha
```

2. Install dependencies:

```bash
make install
```

This creates a virtual environment (`.venv/`) and installs all development dependencies.

## Useful commands

| Command | What it does |
|---------|-------------|
| `make install` | Creates the virtual environment and installs dependencies |
| `make test` | Runs tests with pytest |
| `make lint` | Checks lint and formatting (ruff) |
| `make fix-lint` | Automatically fixes lint and formatting |
| `make clean` | Removes Python cache files |

## Contribution workflow

1. Create a branch from `main`:

```bash
git checkout -b my-feature
```

2. Make your changes and ensure lint and tests pass:

```bash
make fix-lint
make test
```

3. Commit and push:

```bash
git add .
git commit -m "Description of changes"
git push origin my-feature
```

4. Open a Pull Request targeting the `main` branch.

## Project conventions

- **Code in Portuguese**: variable names, functions, classes, and comments should be in Brazilian Portuguese.
- **Formatting**: we use [ruff](https://docs.astral.sh/ruff/) for linting and formatting. Run `make fix-lint` before committing.
- **Tests**: every new feature should have tests. Run `make test` to verify.

## Project structure

```
agenda-palestrinha/
├── .github/
│   ├── workflows/          # GitHub Actions (CI, event workflow)
│   └── ISSUE_TEMPLATE/     # Issue templates
├── backend/
│   ├── banco_de_dados/     # eventos.json (event data)
│   └── adicionar_evento.py # Script to add events
├── tests/                  # Tests with pytest
├── pyproject.toml          # Dependencies and project configuration
└── Makefile                # Shortcuts for common commands
```

## Questions?

Open a [Discussion](https://github.com/cumbucadev/agenda-palestrinha/discussions) and we'll help you out!

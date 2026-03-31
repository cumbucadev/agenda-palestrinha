# Contribuindo

[English Version](/CONTRIBUTING_EN.md)

Obrigado por dedicar o seu tempo para contribuir! Toda ajuda é bem-vinda!

## Pré-requisitos

- [Python 3.12+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [Make](https://www.gnu.org/software/make/)

## Setup local

1. Faça um fork do repositório e clone:

```bash
git clone https://github.com/SEU_USUARIO/agenda-palestrinha.git
cd agenda-palestrinha
```

2. Instale as dependências:

```bash
make install
```

Isso cria um ambiente virtual (`.venv/`) e instala todas as dependências de desenvolvimento.

## Comandos úteis

| Comando | O que faz |
|---------|-----------|
| `make install` | Cria o ambiente virtual e instala as dependências |
| `make test` | Roda os testes com pytest |
| `make lint` | Verifica lint e formatação (ruff) |
| `make fix-lint` | Corrige lint e formatação automaticamente |
| `make clean` | Remove arquivos de cache do Python |

## Fluxo de contribuição

1. Crie uma branch a partir de `main`:

```bash
git checkout -b minha-feature
```

2. Faça suas alterações e garanta que lint e testes passam:

```bash
make fix-lint
make test
```

3. Faça commit e push:

```bash
git add .
git commit -m "Descrição das alterações"
git push origin minha-feature
```

4. Abra um Pull Request para a branch `main`.

## Convenções do projeto

- **Código em português**: nomes de variáveis, funções, classes e comentários devem ser em português do Brasil.
- **Formatação**: usamos [ruff](https://docs.astral.sh/ruff/) para lint e formatação. Rode `make fix-lint` antes de commitar.
- **Testes**: toda funcionalidade nova deve ter testes. Rode `make test` para verificar.

## Estrutura do projeto

```
agenda-palestrinha/
├── .github/
│   ├── workflows/          # GitHub Actions (CI, workflow de eventos)
│   └── ISSUE_TEMPLATE/     # Templates de issues
├── backend/
│   ├── banco_de_dados/     # eventos.json (dados dos eventos)
│   ├── adicionar_evento.py # Script para adicionar eventos
│   ├── requirements.txt    # Dependências de produção
│   └── requirements-dev.txt # Dependências de desenvolvimento
├── tests/                  # Testes com pytest
├── Makefile                # Atalhos para comandos comuns
└── pytest.ini              # Configuração do pytest
```

## Dúvidas?

Abra uma [Discussion](https://github.com/cumbucadev/agenda-palestrinha/discussions) que iremos te ajudar!

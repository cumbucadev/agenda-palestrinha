import json
from pathlib import Path

CAMINHO_EVENTOS = (
    Path(__file__).resolve().parent.parent
    / "backend"
    / "banco_de_dados"
    / "eventos.json"
)


def test_eventos_json_existe():
    assert CAMINHO_EVENTOS.exists()


def test_eventos_json_e_lista_valida():
    dados = json.loads(CAMINHO_EVENTOS.read_text())
    assert isinstance(dados, list)

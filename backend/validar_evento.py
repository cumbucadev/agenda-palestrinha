import json
import os
import sys
from datetime import date

from jsonschema import validate

# Descobre a pasta onde este script está
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho absoluto do arquivo de esquema
caminho_esquema = os.path.join(BASE_DIR, "esquema_issue_evento.json")

with open(caminho_esquema, encoding="utf-8") as f:
    esquema_issue_evento = json.load(f)

MESES = {
    "Janeiro": 1,
    "Fevereiro": 2,
    "Março": 3,
    "Abril": 4,
    "Maio": 5,
    "Junho": 6,
    "Julho": 7,
    "Agosto": 8,
    "Setembro": 9,
    "Outubro": 10,
    "Novembro": 11,
    "Dezembro": 12,
}


def validar_esquema(evento):
    try:
        validate(instance=evento, schema=esquema_issue_evento)
        return True
    except Exception as e:
        print(f"Erro ao validar esquema: {e}")
        return False


def extrair_data(evento, prefixo):
    ano = int(evento[f"ano-do-{prefixo}"]["text"])
    mes = MESES[evento[f"mes-do-{prefixo}"]["text"]]
    dia = int(evento[f"dia-do-{prefixo}"]["text"])
    return date(ano, mes, dia)


def validar_datas(evento):
    try:
        primeiro_dia_evento = extrair_data(evento, "primeiro-dia-de-evento")
        ultimo_dia_evento = extrair_data(evento, "ultimo-dia-de-evento")
        primeiro_dia_submissao = extrair_data(evento, "primeiro-dia-de-submissao")
        ultimo_dia_submissao = extrair_data(evento, "ultimo-dia-de-submissao")
    except ValueError as e:
        print(f"Data inválida no calendário: {e}")
        return False

    if ultimo_dia_evento < primeiro_dia_evento:
        print("Último dia do evento é anterior ao primeiro dia.")
        return False

    if ultimo_dia_submissao < primeiro_dia_submissao:
        print("Último dia de submissão é anterior ao primeiro dia.")
        return False

    if ultimo_dia_submissao > primeiro_dia_evento:
        print("Submissão termina depois do evento começar.")
        return False

    return True


def validar_duplicidade(evento, caminho_eventos=None):
    if caminho_eventos is None:
        caminho_eventos = os.path.join(BASE_DIR, "banco_de_dados", "eventos.json")

    with open(caminho_eventos, encoding="utf-8") as f:
        eventos_existentes = json.load(f)

    nome = evento["nome-do-evento"]["text"]
    for e in eventos_existentes:
        if e["nome"] == nome:
            print(f"Evento '{nome}' já existe no banco de dados.")
            return False

    return True


def validar_evento(evento, caminho_eventos=None):
    if not validar_esquema(evento):
        return False
    if not validar_datas(evento):
        return False
    if not validar_duplicidade(evento, caminho_eventos):
        return False
    return True


def carregar_evento_de_arquivo(caminho_arquivo):
    with open(caminho_arquivo, encoding="utf-8") as arquivo:
        return json.load(arquivo)


if __name__ == "__main__":
    caminho_issue = sys.argv[1]

    if validar_evento(carregar_evento_de_arquivo(caminho_issue)):
        print("issue_data.json é válido.")
        sys.exit(0)
    else:
        print("issue_data.json é inválido.")
        sys.exit(1)

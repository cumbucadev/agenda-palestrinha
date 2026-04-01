import json
import os
import sys

from jsonschema import validate

# Descobre a pasta onde este script está
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho absoluto do arquivo de esquema
caminho_esquema = os.path.join(BASE_DIR, "esquema.json")

with open(caminho_esquema, encoding="utf-8") as f:
    esquema_evento = json.load(f)


def validar_evento(evento):
    try:
        validate(instance=evento, schema=esquema_evento)
        return True
    except Exception:
        return False


def carregar_evento_de_arquivo(caminho_arquivo):
    with open(caminho_arquivo, encoding="utf-8") as arquivo:
        return json.load(arquivo)


if __name__ == "__main__":
    caminho_issue = sys.argv[1]

    if validar_evento(carregar_evento_de_arquivo(caminho_issue)):
        print("issue_data.json é válido.")
        os._exit(0)
    else:
        print("issue_data.json é inválido.")
        os._exit(1)

    # Teste
    # caminho_pasta_issues = os.path.join(os.path.dirname(BASE_DIR), "issues_eventos")
    # for nome_arquivo in os.listdir(caminho_pasta_issues):
    #     if nome_arquivo.endswith(".json"):
    #         caminho_arquivo = os.path.join(caminho_pasta_issues, nome_arquivo)
    #         evento = carregar_evento_de_arquivo(caminho_arquivo)
    #         if validar_evento(evento):
    #             print(f"{nome_arquivo} é válido.")
    #         else:
    #             print(f"{nome_arquivo} é inválido.")

import json
import os
import sys
import uuid
from datetime import UTC, datetime

from backend.validar_evento import MESES

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_EVENTOS = os.path.join(BASE_DIR, "banco_de_dados", "eventos.json")

FORMATOS = {
    "Presencial": "presencial",
    "Híbrido": "hibrido",
    "Online": "online",
}

FORMATOS_SUBMISSAO = {
    "Palestra": "palestra",
    "Workshop": "workshop",
    "Lightning talk": "lightning",
    "Painel": "painel",
    "Tutorial": "tutorial",
    "Minicurso": "minicurso",
}


def converter_formato(texto):
    return FORMATOS[texto]


def converter_data(evento, prefixo):
    ano = evento[f"ano-do-{prefixo}"]["text"]
    mes = MESES[evento[f"mes-do-{prefixo}"]["text"]]
    dia = evento[f"dia-do-{prefixo}"]["text"]
    return f"{ano}-{mes:02d}-{dia}"


def converter_formatos_submissao(evento):
    itens = evento["tipos-de-submissao-aceitos"]["list"]
    return [
        FORMATOS_SUBMISSAO[item["text"]]
        for item in itens
        if item["checked"] and item["text"] in FORMATOS_SUBMISSAO
    ]


def converter_local(evento):
    def _valor(chave):
        campo = evento.get(chave)
        if campo is None:
            return None
        texto = campo["text"]
        return texto if texto else None

    return {
        "cidade": _valor("cidade-deixe-em-branco-se-online"),
        "estado": _valor("estado-provincia-deixe-em-branco-se-online"),
        "pais": _valor("pais-deixe-em-branco-se-online"),
    }


def transformar_evento(evento_issue):
    submissao = {
        "primeiro_dia": converter_data(evento_issue, "primeiro-dia-de-submissao"),
        "ultimo_dia": converter_data(evento_issue, "ultimo-dia-de-submissao"),
        "formatos": converter_formatos_submissao(evento_issue),
    }

    outros_marcado = any(
        item["checked"] and item["text"] == "Outros (especificar abaixo)"
        for item in evento_issue["tipos-de-submissao-aceitos"]["list"]
    )
    outros_texto = evento_issue["se-marcou-outros-especifique"]["text"]
    if outros_marcado and outros_texto:
        submissao["outros_formatos"] = outros_texto

    return {
        "id": str(uuid.uuid4()),
        "nome": evento_issue["nome-do-evento"]["text"],
        "url_site": evento_issue["site-do-evento"]["text"],
        "formato": converter_formato(evento_issue["formato-do-evento"]["text"]),
        "local": converter_local(evento_issue),
        "datas_evento": {
            "primeiro_dia": converter_data(evento_issue, "primeiro-dia-de-evento"),
            "ultimo_dia": converter_data(evento_issue, "ultimo-dia-de-evento"),
        },
        "submissao": submissao,
        "atualizado_em": datetime.now(UTC).isoformat(),
    }


def adicionar_ao_banco(evento, caminho_eventos):
    with open(caminho_eventos, encoding="utf-8") as f:
        eventos = json.load(f)

    eventos.append(evento)

    with open(caminho_eventos, "w", encoding="utf-8") as f:
        json.dump(eventos, f, ensure_ascii=False, indent=2)
        f.write("\n")


def carregar_issue(caminho):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    caminho_issue = sys.argv[1]
    evento_issue = carregar_issue(caminho_issue)
    evento = transformar_evento(evento_issue)
    adicionar_ao_banco(evento, CAMINHO_EVENTOS)
    print(f"Evento '{evento['nome']}' adicionado com sucesso (id={evento['id']}).")

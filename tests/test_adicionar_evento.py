import copy
import json
import os
import tempfile

import pytest

from backend.adicionar_evento import (
    adicionar_ao_banco,
    converter_data,
    converter_formato,
    converter_formatos_submissao,
    converter_local,
    transformar_evento,
)


def _campo(texto, titulo="Titulo"):
    return {"title": titulo, "content": [texto], "text": texto}


@pytest.fixture
def evento_issue():
    return {
        "nome-do-evento": _campo("Python Brasil 2026"),
        "site-do-evento": _campo("https://pythonbrasil.org.br"),
        "formato-do-evento": _campo("Presencial"),
        "cidade-deixe-em-branco-se-online": _campo("Brasília"),
        "estado-provincia-deixe-em-branco-se-online": _campo("DF"),
        "pais-deixe-em-branco-se-online": _campo("BR"),
        "ano-do-primeiro-dia-de-evento": _campo("2026"),
        "mes-do-primeiro-dia-de-evento": _campo("Outubro"),
        "dia-do-primeiro-dia-de-evento": _campo("20"),
        "ano-do-ultimo-dia-de-evento": _campo("2026"),
        "mes-do-ultimo-dia-de-evento": _campo("Outubro"),
        "dia-do-ultimo-dia-de-evento": _campo("25"),
        "ano-do-primeiro-dia-de-submissao": _campo("2026"),
        "mes-do-primeiro-dia-de-submissao": _campo("Janeiro"),
        "dia-do-primeiro-dia-de-submissao": _campo("01"),
        "ano-do-ultimo-dia-de-submissao": _campo("2026"),
        "mes-do-ultimo-dia-de-submissao": _campo("Junho"),
        "dia-do-ultimo-dia-de-submissao": _campo("30"),
        "tipos-de-submissao-aceitos": {
            "title": "Tipos de Submissão aceitos",
            "content": [],
            "text": "",
            "list": [
                {"checked": True, "text": "Palestra"},
                {"checked": True, "text": "Workshop"},
                {"checked": False, "text": "Lightning talk"},
                {"checked": False, "text": "Painel"},
                {"checked": False, "text": "Tutorial"},
                {"checked": False, "text": "Minicurso"},
                {"checked": False, "text": "Outros (especificar abaixo)"},
            ],
        },
        "se-marcou-outros-especifique": _campo(""),
    }


class TestConverterFormato:
    @pytest.mark.parametrize(
        "entrada,esperado",
        [
            ("Presencial", "presencial"),
            ("Híbrido", "hibrido"),
            ("Online", "online"),
        ],
    )
    def test_formatos_validos(self, entrada, esperado):
        assert converter_formato(entrada) == esperado


class TestConverterData:
    def test_data_basica(self, evento_issue):
        assert converter_data(evento_issue, "primeiro-dia-de-evento") == "2026-10-20"

    def test_data_com_mes_de_um_digito(self, evento_issue):
        evento = copy.deepcopy(evento_issue)
        evento["mes-do-primeiro-dia-de-evento"] = _campo("Janeiro")
        assert converter_data(evento, "primeiro-dia-de-evento") == "2026-01-20"

    def test_data_com_dia_de_um_digito(self, evento_issue):
        assert converter_data(evento_issue, "primeiro-dia-de-submissao") == "2026-01-01"

    def test_ultimo_dia_de_evento(self, evento_issue):
        assert converter_data(evento_issue, "ultimo-dia-de-evento") == "2026-10-25"


class TestConverterLocal:
    def test_evento_presencial_completo(self, evento_issue):
        assert converter_local(evento_issue) == {
            "cidade": "Brasília",
            "estado": "DF",
            "pais": "BR",
        }

    def test_evento_online_campos_vazios(self, evento_issue):
        evento = copy.deepcopy(evento_issue)
        evento["cidade-deixe-em-branco-se-online"] = _campo("")
        evento["estado-provincia-deixe-em-branco-se-online"] = _campo("")
        evento["pais-deixe-em-branco-se-online"] = _campo("")
        assert converter_local(evento) == {
            "cidade": None,
            "estado": None,
            "pais": None,
        }

    def test_evento_online_campos_ausentes(self, evento_issue):
        evento = copy.deepcopy(evento_issue)
        del evento["cidade-deixe-em-branco-se-online"]
        del evento["estado-provincia-deixe-em-branco-se-online"]
        del evento["pais-deixe-em-branco-se-online"]
        assert converter_local(evento) == {
            "cidade": None,
            "estado": None,
            "pais": None,
        }

    def test_evento_hibrido_parcial(self, evento_issue):
        evento = copy.deepcopy(evento_issue)
        evento["estado-provincia-deixe-em-branco-se-online"] = _campo("")
        assert converter_local(evento) == {
            "cidade": "Brasília",
            "estado": None,
            "pais": "BR",
        }


def _marcar(evento, textos_marcados):
    """Ajusta a lista de tipos de submissão deixando apenas os textos marcados."""
    evento = copy.deepcopy(evento)
    for item in evento["tipos-de-submissao-aceitos"]["list"]:
        item["checked"] = item["text"] in textos_marcados
    return evento


class TestConverterFormatosSubmissao:
    def test_apenas_palestra_marcada(self, evento_issue):
        evento = _marcar(evento_issue, ["Palestra"])
        assert converter_formatos_submissao(evento) == ["palestra"]

    def test_multiplos_marcados(self, evento_issue):
        evento = _marcar(evento_issue, ["Palestra", "Workshop", "Lightning talk"])
        assert converter_formatos_submissao(evento) == [
            "palestra",
            "workshop",
            "lightning",
        ]

    def test_todos_os_formatos(self, evento_issue):
        evento = _marcar(
            evento_issue,
            [
                "Palestra",
                "Workshop",
                "Lightning talk",
                "Painel",
                "Tutorial",
                "Minicurso",
            ],
        )
        assert converter_formatos_submissao(evento) == [
            "palestra",
            "workshop",
            "lightning",
            "painel",
            "tutorial",
            "minicurso",
        ]

    def test_outros_marcado_nao_entra_na_lista(self, evento_issue):
        evento = _marcar(evento_issue, ["Palestra", "Outros (especificar abaixo)"])
        assert converter_formatos_submissao(evento) == ["palestra"]

    def test_nenhum_marcado(self, evento_issue):
        evento = _marcar(evento_issue, [])
        assert converter_formatos_submissao(evento) == []


class TestTransformarEvento:
    def test_campos_basicos(self, evento_issue):
        evento = _marcar(evento_issue, ["Palestra"])
        resultado = transformar_evento(evento)

        assert resultado["nome"] == "Python Brasil 2026"
        assert resultado["url_site"] == "https://pythonbrasil.org.br"
        assert resultado["formato"] == "presencial"
        assert resultado["local"] == {
            "cidade": "Brasília",
            "estado": "DF",
            "pais": "BR",
        }
        assert resultado["datas_evento"] == {
            "primeiro_dia": "2026-10-20",
            "ultimo_dia": "2026-10-25",
        }
        assert resultado["submissao"]["primeiro_dia"] == "2026-01-01"
        assert resultado["submissao"]["ultimo_dia"] == "2026-06-30"
        assert resultado["submissao"]["formatos"] == ["palestra"]

    def test_gera_id_uuid(self, evento_issue):
        import uuid

        evento = _marcar(evento_issue, ["Palestra"])
        resultado = transformar_evento(evento)

        uuid.UUID(resultado["id"])

    def test_ids_diferentes_em_chamadas_diferentes(self, evento_issue):
        evento = _marcar(evento_issue, ["Palestra"])
        r1 = transformar_evento(evento)
        r2 = transformar_evento(evento)
        assert r1["id"] != r2["id"]

    def test_atualizado_em_formato_iso_utc(self, evento_issue):
        from datetime import datetime

        evento = _marcar(evento_issue, ["Palestra"])
        resultado = transformar_evento(evento)

        timestamp = datetime.fromisoformat(resultado["atualizado_em"])
        assert timestamp.tzinfo is not None

    def test_outros_marcado_e_especificado(self, evento_issue):
        evento = _marcar(evento_issue, ["Palestra", "Outros (especificar abaixo)"])
        evento["se-marcou-outros-especifique"] = _campo("pôster, mesa redonda")
        resultado = transformar_evento(evento)

        assert resultado["submissao"]["outros_formatos"] == "pôster, mesa redonda"

    def test_outros_nao_marcado_omite_campo(self, evento_issue):
        evento = _marcar(evento_issue, ["Palestra"])
        resultado = transformar_evento(evento)

        assert "outros_formatos" not in resultado["submissao"]

    def test_outros_marcado_sem_texto_omite_campo(self, evento_issue):
        evento = _marcar(evento_issue, ["Palestra", "Outros (especificar abaixo)"])
        evento["se-marcou-outros-especifique"] = _campo("")
        resultado = transformar_evento(evento)

        assert "outros_formatos" not in resultado["submissao"]


class TestAdicionarAoBanco:
    def _criar_arquivo(self, eventos):
        arquivo = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        json.dump(eventos, arquivo)
        arquivo.close()
        return arquivo.name

    def test_adiciona_em_banco_vazio(self):
        caminho = self._criar_arquivo([])
        try:
            evento = {"id": "abc", "nome": "Python Brasil"}
            adicionar_ao_banco(evento, caminho)
            with open(caminho, encoding="utf-8") as f:
                dados = json.load(f)
            assert dados == [evento]
        finally:
            os.unlink(caminho)

    def test_adiciona_preservando_eventos_existentes(self):
        existentes = [{"id": "1", "nome": "Evento A"}, {"id": "2", "nome": "Evento B"}]
        caminho = self._criar_arquivo(existentes)
        try:
            novo = {"id": "3", "nome": "Evento C"}
            adicionar_ao_banco(novo, caminho)
            with open(caminho, encoding="utf-8") as f:
                dados = json.load(f)
            assert dados == existentes + [novo]
        finally:
            os.unlink(caminho)

    def test_escreve_json_formatado(self):
        caminho = self._criar_arquivo([])
        try:
            adicionar_ao_banco({"id": "x", "nome": "Teste"}, caminho)
            with open(caminho, encoding="utf-8") as f:
                conteudo = f.read()
            assert "\n" in conteudo
        finally:
            os.unlink(caminho)

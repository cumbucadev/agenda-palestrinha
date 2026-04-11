import copy
import json
import os
import tempfile

import pytest

from backend.validar_evento import (
    validar_datas,
    validar_duplicidade,
    validar_esquema,
    validar_evento,
)


def _campo(texto, titulo="Titulo"):
    """Cria um campo no formato do issue-forms-body-parser."""
    return {"title": titulo, "content": [texto], "text": texto}


@pytest.fixture
def evento_valido():
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
            "content": ["Palestra", "Workshop"],
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


# =====================================================================
# Validação de esquema (JSON Schema)
# =====================================================================


class TestValidarEsquema:
    def test_evento_valido(self, evento_valido):
        assert validar_esquema(evento_valido) is True

    def test_evento_online_sem_local(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["formato-do-evento"] = _campo("Online")
        del evento["cidade-deixe-em-branco-se-online"]
        del evento["estado-provincia-deixe-em-branco-se-online"]
        del evento["pais-deixe-em-branco-se-online"]
        assert validar_esquema(evento) is True

    def test_evento_hibrido(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["formato-do-evento"] = _campo("Híbrido")
        assert validar_esquema(evento) is True

    @pytest.mark.parametrize(
        "campo",
        [
            "nome-do-evento",
            "site-do-evento",
            "formato-do-evento",
            "ano-do-primeiro-dia-de-evento",
            "mes-do-primeiro-dia-de-evento",
            "dia-do-primeiro-dia-de-evento",
            "ano-do-ultimo-dia-de-evento",
            "mes-do-ultimo-dia-de-evento",
            "dia-do-ultimo-dia-de-evento",
            "ano-do-primeiro-dia-de-submissao",
            "mes-do-primeiro-dia-de-submissao",
            "dia-do-primeiro-dia-de-submissao",
            "ano-do-ultimo-dia-de-submissao",
            "mes-do-ultimo-dia-de-submissao",
            "dia-do-ultimo-dia-de-submissao",
            "tipos-de-submissao-aceitos",
            "se-marcou-outros-especifique",
        ],
    )
    def test_campo_obrigatorio_ausente(self, evento_valido, campo):
        evento = copy.deepcopy(evento_valido)
        del evento[campo]
        assert validar_esquema(evento) is False

    def test_formato_evento_invalido(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["formato-do-evento"] = _campo("Virtual")
        assert validar_esquema(evento) is False

    def test_dia_invalido_maior_que_31(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["dia-do-primeiro-dia-de-evento"] = _campo("32")
        assert validar_esquema(evento) is False

    def test_dia_invalido_zero(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["dia-do-primeiro-dia-de-evento"] = _campo("00")
        assert validar_esquema(evento) is False

    def test_dia_invalido_texto(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["dia-do-primeiro-dia-de-evento"] = _campo("abc")
        assert validar_esquema(evento) is False

    def test_mes_invalido(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["mes-do-primeiro-dia-de-evento"] = _campo("Janero")
        assert validar_esquema(evento) is False

    def test_ano_invalido_curto(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["ano-do-primeiro-dia-de-evento"] = _campo("26")
        assert validar_esquema(evento) is False

    def test_campo_sem_text(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["nome-do-evento"] = {"title": "Nome", "content": ["teste"]}
        assert validar_esquema(evento) is False

    def test_campo_sem_title(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["nome-do-evento"] = {"content": ["teste"], "text": "teste"}
        assert validar_esquema(evento) is False

    def test_evento_vazio(self):
        assert validar_esquema({}) is False


# =====================================================================
# Validação de datas (regras de negócio)
# =====================================================================


class TestValidarDatas:
    def test_datas_validas(self, evento_valido):
        assert validar_datas(evento_valido) is True

    def test_evento_um_dia(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["ano-do-ultimo-dia-de-evento"] = _campo("2026")
        evento["mes-do-ultimo-dia-de-evento"] = _campo("Outubro")
        evento["dia-do-ultimo-dia-de-evento"] = _campo("20")
        assert validar_datas(evento) is True

    def test_31_de_fevereiro(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["mes-do-primeiro-dia-de-evento"] = _campo("Fevereiro")
        evento["dia-do-primeiro-dia-de-evento"] = _campo("31")
        assert validar_datas(evento) is False

    def test_30_de_fevereiro(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["mes-do-primeiro-dia-de-evento"] = _campo("Fevereiro")
        evento["dia-do-primeiro-dia-de-evento"] = _campo("30")
        assert validar_datas(evento) is False

    def test_29_fevereiro_ano_nao_bissexto(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["ano-do-primeiro-dia-de-evento"] = _campo("2027")
        evento["mes-do-primeiro-dia-de-evento"] = _campo("Fevereiro")
        evento["dia-do-primeiro-dia-de-evento"] = _campo("29")
        evento["ano-do-ultimo-dia-de-evento"] = _campo("2027")
        evento["mes-do-ultimo-dia-de-evento"] = _campo("Março")
        evento["dia-do-ultimo-dia-de-evento"] = _campo("01")
        assert validar_datas(evento) is False

    def test_29_fevereiro_ano_bissexto(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["ano-do-primeiro-dia-de-evento"] = _campo("2028")
        evento["mes-do-primeiro-dia-de-evento"] = _campo("Fevereiro")
        evento["dia-do-primeiro-dia-de-evento"] = _campo("29")
        evento["ano-do-ultimo-dia-de-evento"] = _campo("2028")
        evento["mes-do-ultimo-dia-de-evento"] = _campo("Março")
        evento["dia-do-ultimo-dia-de-evento"] = _campo("01")
        assert validar_datas(evento) is True

    def test_31_de_abril(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["mes-do-primeiro-dia-de-evento"] = _campo("Abril")
        evento["dia-do-primeiro-dia-de-evento"] = _campo("31")
        assert validar_datas(evento) is False

    def test_ultimo_dia_evento_antes_do_primeiro(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["dia-do-primeiro-dia-de-evento"] = _campo("25")
        evento["dia-do-ultimo-dia-de-evento"] = _campo("20")
        assert validar_datas(evento) is False

    def test_ultimo_dia_submissao_antes_do_primeiro(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["mes-do-primeiro-dia-de-submissao"] = _campo("Junho")
        evento["dia-do-primeiro-dia-de-submissao"] = _campo("30")
        evento["mes-do-ultimo-dia-de-submissao"] = _campo("Janeiro")
        evento["dia-do-ultimo-dia-de-submissao"] = _campo("01")
        assert validar_datas(evento) is False

    def test_submissao_termina_depois_do_evento_comecar(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["mes-do-ultimo-dia-de-submissao"] = _campo("Novembro")
        evento["dia-do-ultimo-dia-de-submissao"] = _campo("01")
        assert validar_datas(evento) is False

    def test_submissao_termina_no_dia_do_evento(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["mes-do-ultimo-dia-de-submissao"] = _campo("Outubro")
        evento["dia-do-ultimo-dia-de-submissao"] = _campo("20")
        assert validar_datas(evento) is True


# =====================================================================
# Validação de duplicidade
# =====================================================================


class TestValidarDuplicidade:
    def _criar_arquivo_eventos(self, eventos):
        arquivo = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        json.dump(eventos, arquivo)
        arquivo.close()
        return arquivo.name

    def test_evento_novo_sem_duplicidade(self, evento_valido):
        caminho = self._criar_arquivo_eventos([])
        try:
            assert validar_duplicidade(evento_valido, caminho) is True
        finally:
            os.unlink(caminho)

    def test_evento_duplicado(self, evento_valido):
        eventos_existentes = [{"nome": "Python Brasil 2026"}]
        caminho = self._criar_arquivo_eventos(eventos_existentes)
        try:
            assert validar_duplicidade(evento_valido, caminho) is False
        finally:
            os.unlink(caminho)

    def test_evento_nome_diferente(self, evento_valido):
        eventos_existentes = [{"nome": "Python Nordeste 2026"}]
        caminho = self._criar_arquivo_eventos(eventos_existentes)
        try:
            assert validar_duplicidade(evento_valido, caminho) is True
        finally:
            os.unlink(caminho)


# =====================================================================
# Validação completa (integração)
# =====================================================================


class TestValidarEvento:
    def test_evento_valido_completo(self, evento_valido):
        assert validar_evento(evento_valido) is True

    def test_esquema_invalido_rejeita(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        del evento["nome-do-evento"]
        assert validar_evento(evento) is False

    def test_data_invalida_rejeita(self, evento_valido):
        evento = copy.deepcopy(evento_valido)
        evento["mes-do-primeiro-dia-de-evento"] = _campo("Fevereiro")
        evento["dia-do-primeiro-dia-de-evento"] = _campo("31")
        assert validar_evento(evento) is False

import json
import os

def extrair_dados_issue():
    """
    Extrai dados de issues do repositório e salva em um arquivo JSON.
    """
    print("Carregando dados das issues...")
    with open("issues.json", "r") as file:
        issues = json.load(file)
        print(f"Carregadas {len(issues)} issues")
        return issues

def adicionar_evento_ao_arquivo(issues, arquivo):
    """
    Adiciona eventos de issues ao arquivo README.md como nova linha na tabela.
    """
    print(f"Adicionando eventos ao arquivo: {arquivo}")
    with open(arquivo, "a", encoding="utf-8") as file:
        for issue in issues:
            titulo = issue.get("title", "")
            corpo = issue.get("body", "")
            labels = [label["name"] for label in issue.get("labels", [])]
            
            print(f"Processando evento: {titulo}")
    
            linhas = corpo.split('\n')
            data_hora = ""
            local_link = ""
            modelo = ""
            descricao = ""
            for linha in linhas:
                if linha.lower().startswith("data/hora:"):
                    data_hora = linha.split(":", 1)[1].strip()
                elif linha.lower().startswith("local/link:"):
                    local_link = linha.split(":", 1)[1].strip()
                elif linha.lower().startswith("modelo:"):
                    modelo = linha.split(":", 1)[1].strip()
                elif linha.lower().startswith("descrição:"):
                    descricao = linha.split(":", 1)[1].strip()
            
            linha_tabela = f"| {titulo} | {data_hora} | {local_link} | {modelo} | {descricao} |\n"
            file.write(linha_tabela)
            print(f"Adicionada linha: {linha_tabela.strip()}")
    
    print(f"Finalizada adição de eventos em {arquivo}")

if __name__ == "__main__":
    print("Iniciando processo de adição de eventos")
    issues = extrair_dados_issue()
    arquivo = "README.md"
    arquivo_EN = "README_EN.md"
    adicionar_evento_ao_arquivo(issues, arquivo)
    adicionar_evento_ao_arquivo(issues, arquivo_EN)
    print("Processo de adição finalizado")

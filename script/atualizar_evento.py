import json

def extrair_dados_issue():
    print("Carregando dados das issues para atualização...")
    with open("issues.json", "r") as file:
        issues = json.load(file)
        print(f"Carregadas {len(issues)} issues")
        return issues

def atualizar_evento_no_arquivo(issues, arquivo):
    print(f"Atualizando eventos no arquivo: {arquivo}")
    with open(arquivo, "r", encoding="utf-8") as file:
        linhas = file.readlines()

    # Encontra início da tabela
    inicio_tabela = None
    for i, linha in enumerate(linhas):
        if linha.strip().startswith("| ---"):
            inicio_tabela = i + 1
            break

    if inicio_tabela is None:
        print("Tabela não encontrada.")
        return

    print(f"Tabela encontrada na linha {inicio_tabela}")
    
    # Atualiza linhas da tabela
    eventos = []
    for issue in issues:
        titulo = issue.get("title", "")
        corpo = issue.get("body", "")
        print(f"Atualizando evento: {titulo}")
        
        linhas_corpo = corpo.split('\n')
        data_hora = local_link = modelo = descricao = ""
        for linha in linhas_corpo:
            if linha.lower().startswith("data/hora:"):
                data_hora = linha.split(":", 1)[1].strip()
            elif linha.lower().startswith("local/link:"):
                local_link = linha.split(":", 1)[1].strip()
            elif linha.lower().startswith("modelo:"):
                modelo = linha.split(":", 1)[1].strip()
            elif linha.lower().startswith("descrição:"):
                descricao = linha.split(":", 1)[1].strip()
        
        linha_evento = f"| {titulo} | {data_hora} | {local_link} | {modelo} | {descricao} |\n"
        eventos.append(linha_evento)
        print(f"Evento atualizado: {linha_evento.strip()}")

    # Remove linhas antigas e adiciona atualizadas
    linhas = linhas[:inicio_tabela] + eventos

    with open(arquivo, "w", encoding="utf-8") as file:
        file.writelines(linhas)
    
    print(f"Finalizada atualização de eventos em {arquivo}")

if __name__ == "__main__":
    print("Iniciando processo de atualização de eventos")
    issues = extrair_dados_issue()
    atualizar_evento_no_arquivo(issues, "README.md")
    atualizar_evento_no_arquivo(issues, "README_EN.md")
    print("Processo de atualização finalizado")

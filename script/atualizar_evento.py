import json

def extrair_dados_issue():
    with open("issues.json", "r") as file:
        issues = json.load(file)
        return issues

def atualizar_evento_no_arquivo(issues, arquivo):
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

    # Atualiza linhas da tabela
    eventos = []
    for issue in issues:
        titulo = issue.get("name", "")
        corpo = issue.get("body", "")
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
        eventos.append(f"| {titulo} | {data_hora} | {local_link} | {modelo} | {descricao} |\n")

    # Remove linhas antigas e adiciona atualizadas
    linhas = linhas[:inicio_tabela] + eventos

    with open(arquivo, "w", encoding="utf-8") as file:
        file.writelines(linhas)

if __name__ == "__main__":
    issues = extrair_dados_issue()
    atualizar_evento_no_arquivo(issues, "README.md")
    atualizar_evento_no_arquivo(issues, "README_EN.md")
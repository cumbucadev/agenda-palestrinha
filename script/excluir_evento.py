import json

def extrair_dados_issue():
    with open("issues.json", "r") as file:
        issues = json.load(file)
        return issues

def remover_evento_do_arquivo(issues, arquivo):
    titulos_para_remover = [issue.get("name", "") for issue in issues]
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

    # Remove linhas que têm o título das issues marcadas para remoção
    novas_linhas = linhas[:inicio_tabela]
    for linha in linhas[inicio_tabela:]:
        if not any(f"| {titulo} |" in linha for titulo in titulos_para_remover):
            novas_linhas.append(linha)

    with open(arquivo, "w", encoding="utf-8") as file:
        file.writelines(novas_linhas)

if __name__ == "__main__":
    issues = extrair_dados_issue()
    remover_evento_do_arquivo(issues, "README.md")
    remover_evento_do_arquivo(issues, "README_EN.md")
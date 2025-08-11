import json

def extrair_dados_issue():
    print("Carregando dados das issues para remoção...")
    with open("issues.json", "r") as file:
        issues = json.load(file)
        print(f"Carregadas {len(issues)} issues")
        return issues

def remover_evento_do_arquivo(issues, arquivo):
    print(f"Removendo eventos do arquivo: {arquivo}")
    titulos_para_remover = [issue.get("title", "") for issue in issues]
    print(f"Títulos para remover: {titulos_para_remover}")
    
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
    
    # Remove linhas que têm o título das issues marcadas para remoção
    novas_linhas = linhas[:inicio_tabela]
    linhas_removidas = 0
    
    for linha in linhas[inicio_tabela:]:
        remover_linha = False
        for titulo in titulos_para_remover:
            if f"| {titulo} |" in linha:
                print(f"Removendo linha com evento: {titulo}")
                remover_linha = True
                linhas_removidas += 1
                break
        
        if not remover_linha:
            novas_linhas.append(linha)
    
    print(f"Total de linhas removidas: {linhas_removidas}")

    with open(arquivo, "w", encoding="utf-8") as file:
        file.writelines(novas_linhas)
    
    print(f"Finalizada remoção de eventos em {arquivo}")

if __name__ == "__main__":
    print("Iniciando processo de remoção de eventos")
    issues = extrair_dados_issue()
    remover_evento_do_arquivo(issues, "README.md")
    remover_evento_do_arquivo(issues, "README_EN.md")
    print("Processo de remoção finalizado")

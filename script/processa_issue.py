import re
import json
import sys

def parse_issue(nome_arquivo : str) -> dict:
    """
    Recebe um JSON de issue do GitHub (dict) e retorna outro JSON (dict)
    com os campos do body estruturados + label principal.
    """
    with open(nome_arquivo, "r", encoding="utf-8") as f:
        issue = json.load(f)
    # pega só o nome do primeiro label (se existir)
    labels = [label["name"] for label in issue.get("labels", [])]
    label = labels[0] if labels else ""

    resultado = {
        
        "title": issue.get("title", ""),
        "label": label,
        "labels": labels,
    }

    body = issue.get("body", "")

    # Extrair blocos do tipo ### Campo \n valor
    padrao_markdown = re.compile(r"###\s*(.*?)\n+([^#]+)", re.DOTALL)
    for campo, valor in padrao_markdown.findall(body):
        chave = campo.strip().lower().replace(" ", "_")
        resultado[chave] = valor.strip()

    # Extrair blocos do tipo **Campo**: valor
    padrao_negrito = re.compile(r"\*\*(.*?)\*\*:\s*(.*)")
    for campo, valor in padrao_negrito.findall(body):
        chave = campo.strip().lower().replace(" ", "_")
        resultado[chave] = valor.strip()
    
    print(resultado)
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)
    
    labels_permitidos = ['adicionar', 'remover', 'atualizar']
    # exibir dados extraídos
    with  open('dados_extraidos.txt', 'w', encoding='utf-8') as f:
        for chave, valor in resultado.items():
            if chave == 'label' and valor in labels_permitidos:
                f.write(f"{chave}: {valor}\n")
            if chave == 'nome do evento':
                f.write(f"{chave}: {valor}\n")

# Exemplo de uso
if __name__ == "__main__":
    arquivo = sys.argv[1] 
    print("ok")
    parse_issue(arquivo)

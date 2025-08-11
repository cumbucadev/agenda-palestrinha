import os
import json
import subprocess

def normaliza_label(label):
    return label.strip().lower()

def processa_issue(arquivo):
    print(f"Processando issue do arquivo: {arquivo}")
    with open(arquivo, 'r', encoding='utf-8') as f:
        issue = json.load(f)[0]  # pega a única issue do arquivo
    
    print(f"Processando issue: {issue['id']}")
    labels = [normaliza_label(label['name'] if isinstance(label, dict) else label) for label in issue.get('labels', [])]

    base_dir = os.path.dirname(os.path.abspath(__file__))
    scripts = {
        'adicionar': os.path.join(base_dir, 'adicionar_evento.py'),
        'atualizar': os.path.join(base_dir, 'atualizar_evento.py'),
        'remover': os.path.join(base_dir, 'excluir_evento.py')
    }

    for label in labels:
        if label in scripts:
            print(f"Executando script para '{label}'...")
            subprocess.run(
                ["py", scripts[label], str(issue['id'])],
                check=True
            )
            break  # executa só o primeiro script que encontrar correspondente
    else:
        print("Nenhum script correspondente às labels encontrado.")

if __name__ == "__main__":
    processa_issue('issues.json')

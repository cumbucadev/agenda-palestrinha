import os
import json

def processa_issue(arquivo):
    with open(arquivo, 'r') as f:
        issues = json.load(f)
    for issue in issues:
        if 'Vamos adicionar um novo evento?😁' in [label['name'] for label in issue.get('labels', [])]:
            os.system('python script/adicionar_evento.py')
        elif 'Vamos atualizar um evento existente?' in [label['name'] for label in issue.get('labels', [])]:
            os.system('python script/atualizar_evento.py')
        elif 'Remover evento ❌' in [label['name'] for label in issue.get('labels', [])]:
            os.system('python script/remover_evento.py')
        elif 'Atualizar evento' in [label['name'] for label in issue.get('labels', [])]:
            os.system('python script/atualizar_evento.py')

if __name__ == "__main__":
    processa_issue('issues.json')
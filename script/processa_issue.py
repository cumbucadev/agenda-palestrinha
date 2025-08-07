import os
import json

def processa_issue(arquivo):
    print(f"Processando issues do arquivo: {arquivo}")
    with open(arquivo, 'r') as f:
        issues = json.load(f)
    
    print(f"Encontradas {len(issues)} issues para processar")
    
    for issue in issues:
        labels = [label['name'] for label in issue.get('labels', [])]
        print(f"Processando issue: {issue.get('title', 'Sem título')}")
        print(f"Labels encontradas: {labels}")
        
        if 'Vamos adicionar um novo evento?🏃' in labels:
            print("Executando script para adicionar evento")
            os.system('python script/adicionar_evento.py')
        elif 'Vamos atualizar um evento existente?' in labels:
            print("Executando script para atualizar evento")
            os.system('python script/atualizar_evento.py')
        elif 'Remover evento 🗑️' in labels:
            print("Executando script para remover evento")
            os.system('python script/excluir_evento.py')
        elif 'Atualizar evento' in labels:
            print("Executando script para atualizar evento (alternativo)")
            os.system('python script/atualizar_evento.py')
        else:
            print("Nenhuma ação encontrada para esta issue")

if __name__ == "__main__":
    processa_issue('issues.json')

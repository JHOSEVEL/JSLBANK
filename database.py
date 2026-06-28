import json 
import os

# Load the database from a JSON file
USUARIOS_FILE = 'database/usuarios.json'
CARTOES_FILE = 'database/cartoes.json'
TRANSACOES_FILE = 'database/transacoes.json'

# all past and files have to created before running the code, otherwise it will throw an error
os.makedirs('database', exist_ok=True)
for file in [USUARIOS_FILE, CARTOES_FILE, TRANSACOES_FILE]:
    if not os.path.exists(file):
        with open(file, 'w', encoding='utf-8') as f:
            json.dump([], f)
            
def ler_dados(arquivo):
    if not os.path.exists(arquivo) or os.path.getsize(arquivo) == 0:
        return []

    with open(arquivo, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def salvar_dado(arquivo, novo_dado):
    dados = ler_dados(arquivo)
    dados.append(novo_dado)
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def gravar_dados(arquivo, dados):
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def atualizar_usuario(usuario_id, campos):
    usuarios = ler_dados(USUARIOS_FILE)
    for i, usuario in enumerate(usuarios):
        if usuario.get('id') == usuario_id:
            usuarios[i].update(campos)
            gravar_dados(USUARIOS_FILE, usuarios)
            return usuarios[i]
    return None
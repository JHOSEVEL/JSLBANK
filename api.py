from flask import Flask, request, jsonify
from datetime import datetime
import database
import utils

api = Flask(__name__)

# toute api to create a new user
@api.route('/cadastrar', methods=['POST'])

# fuction to handle the request and create a new user
def cadastrar():
    dados = request.get_json()

    # validate the password on the backend
    if dados.get('senha') != dados.get('confirmar_senha'):
        return jsonify({"erro": "as senhas não coincidem."}), 400
    
    # remove the confirmar_senha field from the data before saving it to the database
    usuario = { 
        "id": len(database.ler_dados(database.USUARIOS_FILE)) + 1,
        "nome": dados.get('nome'),
        "sobrenome": dados.get('sobrenome'),
        "email": dados.get('email'),
        "senha": dados.get('senha'),
        "telefone": dados.get('telefone'),
        "cidade": dados.get('cidade'),
        "estado": dados.get('estado'),
        "senha": dados.get('senha'), #hash the password before saving it to the database
        "saldo": 1000.00,
        "pontos": 10
    }
    

    # create a fictitious card for the user
    cartao = utils.gerar_cartao_ficticio(usuario['nome'], usuario['sobrenome'])
    cartao['usuario_id'] = usuario['id'] 
    
     #save the user and card data to the database
    database.salvar_dado(database.USUARIOS_FILE, usuario)
    database.salvar_dado(database.CARTOES_FILE, cartao) 

    # return a success response with the user and card data
    return jsonify({
        "usuario": usuario,
        "cartao": cartao
          
    }), 201


def _buscar_cartao(usuario_id):
    cartoes = database.ler_dados(database.CARTOES_FILE)
    return next((c for c in cartoes if c.get('usuario_id') == usuario_id), None)


def _buscar_transacoes(usuario_id):
    transacoes = database.ler_dados(database.TRANSACOES_FILE)
    return [t for t in transacoes if t.get('usuario_id') == usuario_id]


def _normalizar_usuario(usuario):
    if 'saldo' not in usuario:
        usuario['saldo'] = 1000.00
    if 'pontos' not in usuario:
        usuario['pontos'] = 10
    return usuario


@api.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    usuarios = database.ler_dados(database.USUARIOS_FILE)
    usuario = next(
        (u for u in usuarios if u.get('email') == email and u.get('senha') == senha),
        None
    )

    if not usuario:
        return jsonify({"erro": "E-mail ou senha inválidos."}), 401

    usuario = _normalizar_usuario(usuario)
    cartao = _buscar_cartao(usuario['id'])
    transacoes = _buscar_transacoes(usuario['id'])

    return jsonify({
        "usuario": usuario,
        "cartao": cartao,
        "transacoes": transacoes
    }), 200


@api.route('/usuario/<int:usuario_id>', methods=['GET'])
def obter_usuario(usuario_id):
    usuarios = database.ler_dados(database.USUARIOS_FILE)
    usuario = next((u for u in usuarios if u.get('id') == usuario_id), None)

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    usuario = _normalizar_usuario(usuario)
    cartao = _buscar_cartao(usuario_id)
    transacoes = _buscar_transacoes(usuario_id)

    return jsonify({
        "usuario": usuario,
        "cartao": cartao,
        "transacoes": transacoes
    }), 200


@api.route('/transferir', methods=['POST'])
def transferir():
    dados = request.get_json()
    usuario_id = dados.get('usuario_id')
    tipo = dados.get('tipo')
    destinatario_nome = dados.get('destinatario_nome', '').strip()
    valor_raw = dados.get('valor')

    try:
        valor = round(float(str(valor_raw).replace(',', '.')), 2)
    except (TypeError, ValueError):
        return jsonify({"erro": "Valor inválido."}), 400

    if not usuario_id or not tipo or not destinatario_nome or valor <= 0:
        return jsonify({"erro": "Preencha todos os campos corretamente."}), 400

    if tipo not in ('Pix', 'TED'):
        return jsonify({"erro": "Tipo de transferência inválido."}), 400

    usuarios = database.ler_dados(database.USUARIOS_FILE)
    usuario = next((u for u in usuarios if u.get('id') == usuario_id), None)

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado."}), 404

    usuario = _normalizar_usuario(usuario)

    if usuario['saldo'] < valor:
        return jsonify({"erro": "Saldo insuficiente para esta transferência."}), 400

    novo_saldo = round(usuario['saldo'] - valor, 2)
    database.atualizar_usuario(usuario_id, {'saldo': novo_saldo})

    transacoes = database.ler_dados(database.TRANSACOES_FILE)
    transacao = {
        "id": len(transacoes) + 1,
        "usuario_id": usuario_id,
        "tipo": tipo,
        "destinatario_nome": destinatario_nome,
        "valor": valor,
        "data": datetime.now().strftime("%d/%m/%Y")
    }
    database.salvar_dado(database.TRANSACOES_FILE, transacao)

    usuario['saldo'] = novo_saldo

    return jsonify({
        "usuario": usuario,
        "transacao": transacao
    }), 201


if __name__ == '__main__':
    # run the api on port 5001
    api.run(port=5001, debug=True)
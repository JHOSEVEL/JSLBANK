from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"

API_URL = "http://localhost:5001"


def _render_dashboard(dados):
    usuario = dados.get("usuario") or {}
    return render_template(
        "dashboard.html",
        usuario=usuario,
        user=usuario,
        cartao=dados.get("cartao") or {},
        transacoes=dados.get("transacoes") or [],
    )


def _carregar_dados_usuario(usuario_id):
    response = requests.get(f"{API_URL}/usuario/{usuario_id}")
    if response.status_code == 200:
        return response.json()
    return None


@app.route('/')
def landing():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        dados_formulario = {
            "email": request.form.get('email'),
            "senha": request.form.get('senha'),
        }

        try:
            response = requests.post(f"{API_URL}/login", json=dados_formulario)

            if response.status_code == 200:
                dados_response = response.json()
                session['user_id'] = dados_response["usuario"]["id"]
                return _render_dashboard(dados_response)

            erro = response.json().get("erro", "Login inválido.")
            flash(erro, "error")

        except requests.exceptions.ConnectionError:
            flash("Não foi possível conectar à API. Verifique se a API está em execução.", "error")

    return render_template("login.html")


@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash("Faça login para acessar o painel.", "error")
        return redirect(url_for('login'))

    try:
        dados = _carregar_dados_usuario(user_id)
        if dados:
            return _render_dashboard(dados)
        flash("Usuário não encontrado.", "error")
    except requests.exceptions.ConnectionError:
        flash("Não foi possível conectar à API. Verifique se a API está em execução.", "error")

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/transferir', methods=['GET', 'POST'])
def transferir():
    user_id = session.get('user_id')
    if not user_id:
        flash("Faça login para fazer transferências.", "error")
        return redirect(url_for('login'))

    try:
        dados = _carregar_dados_usuario(user_id)
    except requests.exceptions.ConnectionError:
        flash("Não foi possível conectar à API. Verifique se a API está em execução.", "error")
        return redirect(url_for('dashboard'))

    if not dados:
        flash("Usuário não encontrado.", "error")
        return redirect(url_for('login'))

    usuario = dados['usuario']
    tipo_padrao = request.args.get('tipo', 'Pix')

    if request.method == 'POST':
        payload = {
            "usuario_id": user_id,
            "tipo": request.form.get('tipo'),
            "destinatario_nome": request.form.get('destinatario_nome'),
            "valor": request.form.get('valor'),
        }

        try:
            response = requests.post(f"{API_URL}/transferir", json=payload)

            if response.status_code == 201:
                flash("Transferência realizada com sucesso!", "success")
                return redirect(url_for('dashboard'))

            erro = response.json().get("erro", "Não foi possível realizar a transferência.")
            flash(erro, "error")
            tipo_padrao = payload['tipo']

        except requests.exceptions.ConnectionError:
            flash("Não foi possível conectar à API. Verifique se a API está em execução.", "error")

    return render_template(
        "transferir.html",
        usuario=usuario,
        user=usuario,
        tipo=tipo_padrao,
    )


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        dados_formulario = {
            "nome": request.form.get('nome'),
            "sobrenome": request.form.get('sobrenome'),
            "email": request.form.get('email'),
            "senha": request.form.get('senha'),
            "confirmar_senha": request.form.get('confirmar_senha'),
            "telefone": request.form.get('telefone'),
            "cidade": request.form.get('cidade'),
            "estado": request.form.get('estado')
        }

        try:
            response = requests.post(f"{API_URL}/cadastrar", json=dados_formulario)

            if response.status_code == 201:
                dados_response = response.json()
                return render_template(
                    "sucesso.html",
                    nome=dados_response["usuario"]["nome"],
                    cartao=dados_response["cartao"],
                )

            erro = response.json().get("erro", "Não foi possível criar a conta.")
            flash(erro, "error")

        except requests.exceptions.ConnectionError:
            flash("Não foi possível conectar à API. Verifique se a API está em execução.", "error")

    return render_template("cadastro.html")


if __name__ == "__main__":
    app.run(port=5000, debug=True)

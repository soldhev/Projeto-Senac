

from flask import Flask, render_template, request, redirect, url_for
from controllers.usuario_controller import UsuarioController
from database.conexao import Conexao

app = Flask(__name__)
Conexao.criar_tabela()

# Rota principal
@app.route("/")
def login():
    return render_template("login.html")

# Rota para cadastrar usuário
@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")

    controller = UsuarioController()
    controller.cadastrar(nome, email, senha)

    return """
    <script>
    alert("Usuário cadastrado com sucesso!");
    window.location.href="/";
    </script>
    """
# Rota para o login
@app.route("/logar", methods=["POST"])
def logar():
    email = request.form.get("email")
    senha = request.form.get("senha")

    controller = UsuarioController()

    # Verifica login
    if controller.login(email, senha):
        return """
        <script>
        alert("Login realizado com sucesso!");
        window.location.href="/";
        </script>
        """
    else:
        return """
        <script>
        alert("E-mail ou senha inválidos!");
        window.location.href="/";
        </script>
        """
if __name__ == "__main__":
    app.run(debug=True)    


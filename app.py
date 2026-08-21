from flask import Flask, render_template, redirect, url_for
import config
from database.connection import criar_tabelas

from routes.home import home_bp
from routes.cursos import cursos_bp
from routes.localizacao import localizacao_bp
from routes.cadastro import cadastro_bp
from routes.login import login_bp
from routes.admin import admin_bp
from routes.perfil import perfil_bp

app = Flask(__name__)
app.secret_key = config.CHAVE_SECRETA

# Cria o banco de dados e a tabela de usuários, caso ainda não existam
criar_tabelas()

# Registra os grupos de rotas (blueprints) no app
app.register_blueprint(home_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(localizacao_bp)
app.register_blueprint(cadastro_bp)
app.register_blueprint(login_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(perfil_bp)


@app.route("/")
def raiz():
    # Quando alguém acessa só o endereço principal, manda para a home
    return redirect(url_for("home.tela_home"))


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def erro_interno(erro):
    return render_template("errors/500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)

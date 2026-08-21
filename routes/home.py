from flask import Blueprint, render_template

# Um Blueprint agrupa rotas relacionadas (aqui, só a home).
# Isso deixa o app.py mais organizado, sem todas as rotas no mesmo arquivo.
home_bp = Blueprint("home", __name__)


@home_bp.route("/home/index.html")
def tela_home():
    return render_template("home/index.html")

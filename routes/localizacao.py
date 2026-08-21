from flask import Blueprint, render_template

localizacao_bp = Blueprint("localizacao", __name__)


@localizacao_bp.route("/localizacao/localizacao.html")
def tela_localizacao():
    return render_template("localizacao/localizacao.html")

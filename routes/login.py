from flask import Blueprint, render_template, request, redirect, url_for, session
from database.models import buscar_usuario_por_email_ou_usuario
from utils.helpers import senha_esta_correta

login_bp = Blueprint("login", __name__)


@login_bp.route("/login/login.html", methods=["GET", "POST"])
def tela_login():
    if request.method == "GET":
        veio_do_cadastro = request.args.get("sucesso") == "1"
        return render_template("login/login.html", erro=None, sucesso=veio_do_cadastro)

    login_digitado = request.form.get("login", "").strip()
    senha_digitada = request.form.get("senha", "")

    usuario = buscar_usuario_por_email_ou_usuario(login_digitado)

    if usuario is None or not senha_esta_correta(senha_digitada, usuario["senha"]):
        return render_template(
            "login/login.html",
            erro="Usuário/e-mail ou senha inválidos.",
            sucesso=False
        )

    session["usuario_id"] = usuario["id"]
    session["usuario_nome"] = usuario["nome"]
    session["admin"] = bool(usuario["admin"])

    if session["admin"]:
        return redirect(url_for("admin.tela_painel"))

    return redirect(url_for("home.tela_home"))


@login_bp.route("/login/logout")
def logout():
    session.clear()
    return redirect(url_for("home.tela_home"))

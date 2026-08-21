from flask import Blueprint, render_template

cursos_bp = Blueprint("cursos", __name__)


@cursos_bp.route("/cursos/cursos.html")
def tela_cursos():
    return render_template("cursos/cursos.html")


@cursos_bp.route("/cursos/curso_info.html")
def curso_informatica():
    return render_template("cursos/curso_info.html")


@cursos_bp.route("/cursos/curso_redes.html")
def curso_redes():
    return render_template("cursos/curso_redes.html")


@cursos_bp.route("/cursos/curso_sistemas.html")
def curso_sistemas():
    return render_template("cursos/curso_sistemas.html")


@cursos_bp.route("/cursos/curso_admin.html")
def curso_administracao():
    return render_template("cursos/curso_admin.html")


@cursos_bp.route("/cursos/curso_jogos.html")
def curso_jogos():
    return render_template("cursos/curso_jogos.html")

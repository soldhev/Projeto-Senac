from flask import Blueprint, render_template, request, redirect, url_for, session
import config
from database.models import (
    buscar_usuario_por_id, atualizar_perfil, definir_senha,
    atualizar_foto_perfil, email_ou_dados_ja_existem_em_outro_usuario
)
from utils.helpers import login_obrigatorio, gerar_hash_senha, senha_esta_correta, salvar_foto_perfil

perfil_bp = Blueprint("perfil", __name__)


@perfil_bp.route("/perfil/perfil.html")
@login_obrigatorio
def tela_perfil():
    usuario = buscar_usuario_por_id(session["usuario_id"])
    # request.args.get("sucesso") deixa mostrar uma mensagem depois de
    # um redirect (ex: "dados", "senha", "foto"), sem precisar reenviar o form
    return render_template(
        "perfil/perfil.html", usuario=usuario, erro=None,
        sucesso=request.args.get("sucesso")
    )


@perfil_bp.route("/perfil/editar", methods=["POST"])
@login_obrigatorio
def editar_dados():
    """Atualiza os dados cadastrais do próprio usuário logado."""
    usuario_id = session["usuario_id"]
    usuario_atual = buscar_usuario_por_id(usuario_id)

    dados = {
        "nome": request.form.get("nome", "").strip(),
        "sobrenome": request.form.get("sobrenome", "").strip(),
        "endereco": request.form.get("endereco", "").strip(),
        "numero": request.form.get("numero", "").strip(),
        "bairro": request.form.get("bairro", "").strip(),
        "cidade": request.form.get("cidade", "").strip(),
        "estado": request.form.get("estado", "").strip(),
        "cpf": request.form.get("cpf", "").strip(),
        "rg": request.form.get("rg", "").strip(),
        "data_nascimento": request.form.get("data_nascimento", "").strip(),
        "celular": request.form.get("celular", "").strip(),
        "email": request.form.get("email", "").strip().lower(),
        "usuario": request.form.get("usuario", "").strip(),
        "observacao": request.form.get("observacao", "").strip(),
    }

    if not all([dados["nome"], dados["sobrenome"], dados["email"], dados["usuario"]]):
        return render_template(
            "perfil/perfil.html", usuario=usuario_atual, sucesso=None,
            erro="Preencha ao menos nome, sobrenome, e-mail e usuário."
        )

    if email_ou_dados_ja_existem_em_outro_usuario(
        dados["email"], dados["cpf"], dados["usuario"], usuario_id
    ):
        return render_template(
            "perfil/perfil.html", usuario=usuario_atual, sucesso=None,
            erro="Esse e-mail, CPF ou usuário já pertence a outra pessoa."
        )

    atualizar_perfil(usuario_id, dados)
    # Se o usuário mudou o nome, a sessão precisa refletir isso
    session["usuario_nome"] = dados["nome"]

    return redirect(url_for("perfil.tela_perfil", sucesso="dados"))


@perfil_bp.route("/perfil/senha", methods=["POST"])
@login_obrigatorio
def alterar_minha_senha():
    """Permite o próprio usuário trocar a senha dele."""
    usuario_id = session["usuario_id"]
    usuario = buscar_usuario_por_id(usuario_id)

    senha_atual = request.form.get("senha_atual", "")
    nova_senha = request.form.get("nova_senha", "")
    confirmar_nova_senha = request.form.get("confirmar_nova_senha", "")

    if not senha_esta_correta(senha_atual, usuario["senha"]):
        return render_template(
            "perfil/perfil.html", usuario=usuario, sucesso=None,
            erro="A senha atual digitada está incorreta."
        )

    if not nova_senha or nova_senha != confirmar_nova_senha:
        return render_template(
            "perfil/perfil.html", usuario=usuario, sucesso=None,
            erro="A nova senha e a confirmação precisam ser iguais."
        )

    definir_senha(usuario_id, gerar_hash_senha(nova_senha))
    return redirect(url_for("perfil.tela_perfil", sucesso="senha"))


@perfil_bp.route("/perfil/foto", methods=["POST"])
@login_obrigatorio
def atualizar_minha_foto():
    """Permite o próprio usuário trocar a foto de perfil."""
    usuario_id = session["usuario_id"]
    usuario = buscar_usuario_por_id(usuario_id)

    arquivo_foto = request.files.get("foto")
    nome_arquivo_salvo = salvar_foto_perfil(
        arquivo_foto, usuario_id, config.PASTA_UPLOADS_PERFIL
    )

    if not nome_arquivo_salvo:
        return render_template(
            "perfil/perfil.html", usuario=usuario, sucesso=None,
            erro="Escolha uma imagem válida (.png, .jpg ou .jpeg)."
        )

    atualizar_foto_perfil(usuario_id, nome_arquivo_salvo)
    return redirect(url_for("perfil.tela_perfil", sucesso="foto"))

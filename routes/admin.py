from flask import Blueprint, render_template, request, redirect, url_for
import config
from database.models import (
    listar_usuarios, buscar_usuario_por_id, atualizar_usuario, excluir_usuario,
    definir_senha, criar_usuario, email_ou_dados_ja_existem,
    email_ou_dados_ja_existem_em_outro_usuario, atualizar_foto_perfil
)
from utils.helpers import admin_obrigatorio, gerar_hash_senha, salvar_foto_perfil

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/painel.html")
@admin_obrigatorio
def tela_painel():
    usuarios = listar_usuarios()
    return render_template("admin/painel.html", usuarios=usuarios)


@admin_bp.route("/admin/editar_usuario/<int:usuario_id>.html", methods=["GET", "POST"])
@admin_obrigatorio
def editar_usuario(usuario_id):
    usuario = buscar_usuario_por_id(usuario_id)

    if usuario is None:
        return redirect(url_for("admin.tela_painel"))

    if request.method == "GET":
        return render_template("admin/editar_usuario.html", usuario=usuario, erro=None)

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
        "admin": 1 if request.form.get("admin") == "on" else 0,
    }

    if not all([dados["nome"], dados["sobrenome"], dados["email"], dados["usuario"]]):
        return render_template(
            "admin/editar_usuario.html", usuario=usuario,
            erro="Preencha ao menos nome, sobrenome, e-mail e usuário."
        )

    if email_ou_dados_ja_existem_em_outro_usuario(
        dados["email"], dados["cpf"], dados["usuario"], usuario_id
    ):
        return render_template(
            "admin/editar_usuario.html", usuario=usuario,
            erro="Esse e-mail, CPF ou usuário já pertence a outra pessoa."
        )

    atualizar_usuario(usuario_id, dados)

    nova_senha = request.form.get("nova_senha", "")
    confirmar_nova_senha = request.form.get("confirmar_nova_senha", "")
    if nova_senha or confirmar_nova_senha:
        if nova_senha != confirmar_nova_senha:
            usuario_atualizado = buscar_usuario_por_id(usuario_id)
            return render_template(
                "admin/editar_usuario.html", usuario=usuario_atualizado,
                erro="A nova senha e a confirmação não são iguais. Os outros dados já foram salvos."
            )
        definir_senha(usuario_id, gerar_hash_senha(nova_senha))

    return redirect(url_for("admin.tela_painel"))


@admin_bp.route("/admin/novo_usuario.html", methods=["GET", "POST"])
@admin_obrigatorio
def novo_usuario():
    if request.method == "GET":
        return render_template("admin/novo_usuario.html", erro=None)

    nome = request.form.get("nome", "").strip()
    sobrenome = request.form.get("sobrenome", "").strip()
    endereco = request.form.get("endereco", "").strip()
    numero = request.form.get("numero", "").strip()
    bairro = request.form.get("bairro", "").strip()
    cidade = request.form.get("cidade", "").strip()
    estado = request.form.get("estado", "").strip()
    cpf = request.form.get("cpf", "").strip()
    rg = request.form.get("rg", "").strip()
    data_nascimento = request.form.get("data_nascimento", "").strip()
    celular = request.form.get("celular", "").strip()
    email = request.form.get("email", "").strip().lower()
    usuario = request.form.get("usuario", "").strip()
    senha = request.form.get("senha", "")
    confirmar_senha = request.form.get("confirmar_senha", "")
    observacao = request.form.get("observacao", "").strip()
    eh_admin = 1 if request.form.get("admin") == "on" else 0

    campos_obrigatorios = [
        nome, sobrenome, endereco, numero, bairro, cidade, estado,
        cpf, rg, data_nascimento, celular, email, usuario, senha,
        confirmar_senha
    ]

    if not all(campos_obrigatorios):
        return render_template(
            "admin/novo_usuario.html",
            erro="Preencha todos os campos obrigatórios."
        )

    if senha != confirmar_senha:
        return render_template(
            "admin/novo_usuario.html",
            erro="A senha e a confirmação de senha não são iguais."
        )

    if email_ou_dados_ja_existem(email, cpf, usuario):
        return render_template(
            "admin/novo_usuario.html",
            erro="Já existe um cadastro com esse e-mail, CPF ou usuário."
        )

    dados = {
        "nome": nome, "sobrenome": sobrenome, "endereco": endereco,
        "numero": numero, "bairro": bairro, "cidade": cidade, "estado": estado,
        "cpf": cpf, "rg": rg, "data_nascimento": data_nascimento,
        "celular": celular, "email": email, "usuario": usuario,
        "senha": gerar_hash_senha(senha), "observacao": observacao
    }

    novo_id = criar_usuario(dados)

    if eh_admin:
        usuario_criado = buscar_usuario_por_id(novo_id)
        dados_completos = dict(usuario_criado)
        dados_completos["admin"] = 1
        atualizar_usuario(novo_id, dados_completos)

    arquivo_foto = request.files.get("foto")
    nome_arquivo_salvo = salvar_foto_perfil(
        arquivo_foto, novo_id, config.PASTA_UPLOADS_PERFIL
    )
    if nome_arquivo_salvo:
        atualizar_foto_perfil(novo_id, nome_arquivo_salvo)

    return redirect(url_for("admin.tela_painel"))


@admin_bp.route("/admin/excluir_usuario/<int:usuario_id>", methods=["POST"])
@admin_obrigatorio
def excluir(usuario_id):
    excluir_usuario(usuario_id)
    return redirect(url_for("admin.tela_painel"))

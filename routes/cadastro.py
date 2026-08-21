from flask import Blueprint, render_template, request, redirect, url_for
import config
from database.models import criar_usuario, email_ou_dados_ja_existem
from utils.helpers import gerar_hash_senha, salvar_foto_perfil

cadastro_bp = Blueprint("cadastro", __name__)


@cadastro_bp.route("/cadastro/cadastro.html", methods=["GET", "POST"])
def tela_cadastro():
    if request.method == "GET":
        return render_template("cadastro/cadastro.html", erro=None)

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

    campos_obrigatorios = [
        nome, sobrenome, endereco, numero, bairro, cidade, estado,
        cpf, rg, data_nascimento, celular, email, usuario, senha,
        confirmar_senha
    ]

    if not all(campos_obrigatorios):
        return render_template(
            "cadastro/cadastro.html",
            erro="Preencha todos os campos obrigatórios."
        )

    if senha != confirmar_senha:
        return render_template(
            "cadastro/cadastro.html",
            erro="A senha e a confirmação de senha não são iguais."
        )

    if email_ou_dados_ja_existem(email, cpf, usuario):
        return render_template(
            "cadastro/cadastro.html",
            erro="Já existe um cadastro com esse e-mail, CPF ou usuário."
        )

    dados = {
        "nome": nome, "sobrenome": sobrenome, "endereco": endereco,
        "numero": numero, "bairro": bairro, "cidade": cidade, "estado": estado,
        "cpf": cpf, "rg": rg, "data_nascimento": data_nascimento,
        "celular": celular, "email": email, "usuario": usuario,
        "senha": gerar_hash_senha(senha), "observacao": observacao
    }

    novo_usuario_id = criar_usuario(dados)

    arquivo_foto = request.files.get("foto")
    nome_arquivo_salvo = salvar_foto_perfil(
        arquivo_foto, novo_usuario_id, config.PASTA_UPLOADS_PERFIL
    )
    if nome_arquivo_salvo:
        from database.models import atualizar_foto_perfil
        atualizar_foto_perfil(novo_usuario_id, nome_arquivo_salvo)

    return redirect(url_for("login.tela_login", sucesso="1"))

from functools import wraps
import os
from flask import session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

EXTENSOES_PERMITIDAS = {"png", "jpg", "jpeg"}


def gerar_hash_senha(senha):
    return generate_password_hash(senha)


def senha_esta_correta(senha_digitada, hash_guardado_no_banco):
    return check_password_hash(hash_guardado_no_banco, senha_digitada)


def login_obrigatorio(funcao_da_rota):
    @wraps(funcao_da_rota)
    def rota_protegida(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login.tela_login"))
        return funcao_da_rota(*args, **kwargs)
    return rota_protegida


def admin_obrigatorio(funcao_da_rota):
    @wraps(funcao_da_rota)
    def rota_protegida(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login.tela_login"))
        if not session.get("admin"):
            return redirect(url_for("home.tela_home"))
        return funcao_da_rota(*args, **kwargs)
    return rota_protegida


def extensao_permitida(nome_arquivo):
    if "." not in nome_arquivo:
        return False
    extensao = nome_arquivo.rsplit(".", 1)[1].lower()
    return extensao in EXTENSOES_PERMITIDAS


def salvar_foto_perfil(arquivo_enviado, usuario_id, pasta_uploads):
    if arquivo_enviado is None or arquivo_enviado.filename == "":
        return None

    if not extensao_permitida(arquivo_enviado.filename):
        return None

    extensao = arquivo_enviado.filename.rsplit(".", 1)[1].lower()
    nome_arquivo = secure_filename(f"usuario_{usuario_id}.{extensao}")

    os.makedirs(pasta_uploads, exist_ok=True)
    caminho_completo = os.path.join(pasta_uploads, nome_arquivo)
    arquivo_enviado.save(caminho_completo)

    return nome_arquivo

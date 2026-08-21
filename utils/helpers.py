from functools import wraps
import os
from flask import session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# Extensões de imagem aceitas para a foto de perfil
EXTENSOES_PERMITIDAS = {"png", "jpg", "jpeg"}


def gerar_hash_senha(senha):
    """
    Transforma a senha digitada em um "hash" (uma versão embaralhada
    e irreversível). Assim, mesmo que alguém acesse o banco de dados,
    não vê a senha real de ninguém.
    """
    return generate_password_hash(senha)


def senha_esta_correta(senha_digitada, hash_guardado_no_banco):
    """Compara a senha digitada no login com o hash guardado no banco."""
    return check_password_hash(hash_guardado_no_banco, senha_digitada)


def login_obrigatorio(funcao_da_rota):
    """
    Decorator (uma "etiqueta" que colocamos em cima de uma rota).

    Use @login_obrigatorio em qualquer rota que só pode ser acessada
    por quem já fez login. Se não estiver logado, manda para a tela
    de login.
    """
    @wraps(funcao_da_rota)
    def rota_protegida(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login.tela_login"))
        return funcao_da_rota(*args, **kwargs)
    return rota_protegida


def admin_obrigatorio(funcao_da_rota):
    """
    Igual ao login_obrigatorio, mas além de estar logado, a pessoa
    também precisa ser administradora. Usado nas rotas do painel admin.
    """
    @wraps(funcao_da_rota)
    def rota_protegida(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login.tela_login"))
        if not session.get("admin"):
            return redirect(url_for("home.tela_home"))
        return funcao_da_rota(*args, **kwargs)
    return rota_protegida


def extensao_permitida(nome_arquivo):
    """Confere se o arquivo enviado tem uma extensão de imagem aceita."""
    if "." not in nome_arquivo:
        return False
    extensao = nome_arquivo.rsplit(".", 1)[1].lower()
    return extensao in EXTENSOES_PERMITIDAS


def salvar_foto_perfil(arquivo_enviado, usuario_id, pasta_uploads):
    """
    Salva a foto de perfil enviada no formulário (campo <input type="file">).

    'arquivo_enviado' é o objeto que vem de request.files.get("foto").
    Retorna o nome do arquivo salvo, ou None se não veio nenhum arquivo
    válido (o campo é opcional, então isso é normal acontecer).
    """
    if arquivo_enviado is None or arquivo_enviado.filename == "":
        return None

    if not extensao_permitida(arquivo_enviado.filename):
        return None

    extensao = arquivo_enviado.filename.rsplit(".", 1)[1].lower()
    # Nome fixo por usuário (ex: usuario_7.jpg), assim toda vez que a
    # pessoa troca a foto, o arquivo antigo é simplesmente sobrescrito.
    nome_arquivo = secure_filename(f"usuario_{usuario_id}.{extensao}")

    os.makedirs(pasta_uploads, exist_ok=True)
    caminho_completo = os.path.join(pasta_uploads, nome_arquivo)
    arquivo_enviado.save(caminho_completo)

    return nome_arquivo

import os

# Pasta onde este arquivo (config.py) está, usada como referência
# para montar outros caminhos do projeto sem precisar escrever
# o caminho completo na mão.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho do arquivo do banco de dados SQLite.
# O SQLite guarda tudo em um único arquivo, o que é ótimo para
# projetos de estudo (não precisa instalar nada).
CAMINHO_BANCO = os.path.join(BASE_DIR, "database", "banco.db")

# Pasta onde as fotos de perfil enviadas pelos usuários são salvas.
# Fica dentro de static/ para que o Flask consiga servir essas
# imagens automaticamente pelo navegador.
PASTA_UPLOADS_PERFIL = os.path.join(BASE_DIR, "static", "uploads", "perfil")

# Chave secreta usada pelo Flask para proteger a sessão do usuário
# logado (cookie de login). Em um projeto real essa chave ficaria
# escondida fora do código, mas aqui deixamos simples de propósito.
CHAVE_SECRETA = "senac-tech-chave-de-desenvolvimento-troque-em-producao"

# Dados do usuário administrador criado automaticamente na primeira
# vez que o site roda (assim sempre existe um admin para entrar
# no painel, mesmo em um banco novo/vazio).
ADMIN_EMAIL = "admin@senac.com"
ADMIN_USUARIO = "admin"
ADMIN_SENHA = "admin123"

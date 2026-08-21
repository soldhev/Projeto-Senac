import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CAMINHO_BANCO = os.path.join(BASE_DIR, "database", "banco.db")

PASTA_UPLOADS_PERFIL = os.path.join(BASE_DIR, "static", "uploads", "perfil")

CHAVE_SECRETA = "senac-tech-chave-de-desenvolvimento-troque-em-producao"

ADMIN_EMAIL = "admin@senac.com"
ADMIN_USUARIO = "admin"
ADMIN_SENHA = "admin123"

import sqlite3
import config


def obter_conexao():
    conexao = sqlite3.connect(config.CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabelas():
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            endereco TEXT NOT NULL,
            numero TEXT NOT NULL,
            bairro TEXT NOT NULL,
            cidade TEXT NOT NULL,
            estado TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            rg TEXT NOT NULL,
            data_nascimento TEXT NOT NULL,
            celular TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            observacao TEXT,
            admin INTEGER NOT NULL DEFAULT 0,
            foto_perfil TEXT,
            data_cadastro TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    conexao.commit()

    cursor.execute("PRAGMA table_info(usuarios)")
    colunas_existentes = [linha["name"] for linha in cursor.fetchall()]
    if "foto_perfil" not in colunas_existentes:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN foto_perfil TEXT")
        conexao.commit()

    cursor.execute("SELECT id FROM usuarios WHERE admin = 1")
    ja_existe_admin = cursor.fetchone()

    if not ja_existe_admin:
        from utils.helpers import gerar_hash_senha

        cursor.execute("""
            INSERT INTO usuarios
                (nome, sobrenome, endereco, numero, bairro, cidade, estado,
                 cpf, rg, data_nascimento, celular, email, usuario, senha,
                 observacao, admin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            "Administrador", "Senac", "Rua Exemplo", "0", "Centro",
            "Sapucaia do Sul", "RS", "00000000000", "0000000000",
            "2000-01-01", "(51) 00000-0000", config.ADMIN_EMAIL,
            config.ADMIN_USUARIO, gerar_hash_senha(config.ADMIN_SENHA),
            "Usuário administrador criado automaticamente pelo sistema"
        ))
        conexao.commit()

    conexao.close()

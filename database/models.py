from database.connection import obter_conexao


def criar_usuario(dados):
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO usuarios
            (nome, sobrenome, endereco, numero, bairro, cidade, estado,
             cpf, rg, data_nascimento, celular, email, usuario, senha, observacao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dados["nome"], dados["sobrenome"], dados["endereco"], dados["numero"],
        dados["bairro"], dados["cidade"], dados["estado"], dados["cpf"],
        dados["rg"], dados["data_nascimento"], dados["celular"], dados["email"],
        dados["usuario"], dados["senha"], dados["observacao"]
    ))

    conexao.commit()
    novo_id = cursor.lastrowid
    conexao.close()
    return novo_id


def buscar_usuario_por_email_ou_usuario(login):
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE email = ? OR usuario = ?",
        (login, login)
    )

    usuario = cursor.fetchone()
    conexao.close()
    return usuario


def buscar_usuario_por_id(usuario_id):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
    usuario = cursor.fetchone()
    conexao.close()
    return usuario


def email_ou_dados_ja_existem(email, cpf, usuario):
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id FROM usuarios WHERE email = ? OR cpf = ? OR usuario = ?",
        (email, cpf, usuario)
    )

    existe = cursor.fetchone()
    conexao.close()
    return existe is not None


def email_ou_dados_ja_existem_em_outro_usuario(email, cpf, usuario, usuario_id):
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute(
        """SELECT id FROM usuarios
           WHERE (email = ? OR cpf = ? OR usuario = ?) AND id != ?""",
        (email, cpf, usuario, usuario_id)
    )

    existe = cursor.fetchone()
    conexao.close()
    return existe is not None


def listar_usuarios():
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios ORDER BY nome, sobrenome")
    usuarios = cursor.fetchall()
    conexao.close()
    return usuarios


def atualizar_usuario(usuario_id, dados):
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET nome = ?, sobrenome = ?, endereco = ?, numero = ?, bairro = ?,
            cidade = ?, estado = ?, cpf = ?, rg = ?, data_nascimento = ?,
            celular = ?, email = ?, usuario = ?, observacao = ?, admin = ?
        WHERE id = ?
    """, (
        dados["nome"], dados["sobrenome"], dados["endereco"], dados["numero"],
        dados["bairro"], dados["cidade"], dados["estado"], dados["cpf"],
        dados["rg"], dados["data_nascimento"], dados["celular"], dados["email"],
        dados["usuario"], dados["observacao"], dados["admin"], usuario_id
    ))

    conexao.commit()
    conexao.close()


def excluir_usuario(usuario_id):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    conexao.commit()
    conexao.close()


def atualizar_perfil(usuario_id, dados):
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET nome = ?, sobrenome = ?, endereco = ?, numero = ?, bairro = ?,
            cidade = ?, estado = ?, cpf = ?, rg = ?, data_nascimento = ?,
            celular = ?, email = ?, usuario = ?, observacao = ?
        WHERE id = ?
    """, (
        dados["nome"], dados["sobrenome"], dados["endereco"], dados["numero"],
        dados["bairro"], dados["cidade"], dados["estado"], dados["cpf"],
        dados["rg"], dados["data_nascimento"], dados["celular"], dados["email"],
        dados["usuario"], dados["observacao"], usuario_id
    ))

    conexao.commit()
    conexao.close()


def definir_senha(usuario_id, novo_hash_senha):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE usuarios SET senha = ? WHERE id = ?",
        (novo_hash_senha, usuario_id)
    )
    conexao.commit()
    conexao.close()


def atualizar_foto_perfil(usuario_id, nome_arquivo):
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE usuarios SET foto_perfil = ? WHERE id = ?",
        (nome_arquivo, usuario_id)
    )
    conexao.commit()
    conexao.close()

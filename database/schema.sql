-- ============================================================
-- Script SQL - Sistema Senac Tech
-- Banco: SQLite (arquivo database/banco.db)
--
-- Este arquivo é só para DOCUMENTAR o modelo do banco de dados,
-- como pede o edital ("criar o script SQL"). Na prática, o
-- próprio sistema (database/connection.py) já cria essa mesma
-- tabela sozinho na primeira vez que o app.py roda, então você
-- não precisa rodar este arquivo manualmente para o site funcionar.
-- ============================================================

CREATE TABLE IF NOT EXISTS usuarios (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Dados pessoais
    nome              TEXT NOT NULL,
    sobrenome         TEXT NOT NULL,
    endereco          TEXT NOT NULL,
    numero            TEXT NOT NULL,
    bairro            TEXT NOT NULL,
    cidade            TEXT NOT NULL,
    estado            TEXT NOT NULL,          -- sigla, ex: "RS"
    cpf               TEXT NOT NULL UNIQUE,
    rg                TEXT NOT NULL,
    data_nascimento   TEXT NOT NULL,           -- formato AAAA-MM-DD
    celular           TEXT NOT NULL,

    -- Dados de acesso ao sistema
    email             TEXT NOT NULL UNIQUE,
    usuario           TEXT NOT NULL UNIQUE,
    senha             TEXT NOT NULL,           -- hash da senha (nunca texto puro)

    -- Outros
    observacao        TEXT,
    admin             INTEGER NOT NULL DEFAULT 0,  -- 0 = usuário comum, 1 = administrador
    foto_perfil       TEXT,                        -- nome do arquivo salvo em static/uploads/perfil/
    data_cadastro     TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Usuário administrador criado automaticamente pelo sistema
-- (login: admin / senha: admin123 - trocar depois de subir o projeto)
-- Esse INSERT também é feito sozinho pelo connection.py, aqui é
-- só para documentação de como fica o registro:
--
-- INSERT INTO usuarios (nome, sobrenome, ..., usuario, senha, admin)
-- VALUES ('Administrador', 'Senac', ..., 'admin', '<hash-da-senha>', 1);

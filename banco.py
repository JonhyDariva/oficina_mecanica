# banco.py
# conexao com o banco e criacao das tabelas
# IBM4023 - AC1 - oficina mecanica

import os
import sqlite3


def conectar_banco():
    """conecta ao banco sqlite e garante que as tabelas existem."""
    os.makedirs('dados', exist_ok=True)
    conn = sqlite3.connect('dados/oficina.db')
    conn.row_factory = sqlite3.Row

    conn.execute('''
        CREATE TABLE IF NOT EXISTS veiculos (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            placa             TEXT    NOT NULL UNIQUE,
            marca             TEXT    NOT NULL,
            modelo            TEXT    NOT NULL,
            ano               INTEGER NOT NULL,
            nome_proprietario TEXT    NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS servicos (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            veiculo_id   INTEGER NOT NULL,
            descricao    TEXT    NOT NULL,
            data_entrada TEXT    NOT NULL,
            valor        REAL    NOT NULL,
            concluido    TEXT    NOT NULL DEFAULT 'nao',
            FOREIGN KEY (veiculo_id) REFERENCES veiculos(id)
        )
    ''')

    conn.commit()
    return conn

import sqlite3

conexao = sqlite3.connect("usuarios.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    saldo REAL DEFAULT 0
)
""")

conexao.commit()
conexao.close()
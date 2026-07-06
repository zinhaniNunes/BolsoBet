from flask import Flask, render_template, request, redirect, url_for, flash, session
from pathlib import Path
import sqlite3
import hashlib
import secrets

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "usuarios.db"
app.secret_key = secrets.token_hex(32)

# Conectar ao banco
def conectar():
    return sqlite3.connect(DB_PATH)


# Página inicial
@app.route("/")
def home():

    if "usuario_id" not in session:
        return render_template("home.html")

    con = conectar()
    cursor = con.cursor()

    cursor.execute(
        "SELECT saldo FROM usuarios WHERE id=?",
        (session["usuario_id"],)
    )

    saldo = cursor.fetchone()[0]

    con.close()

    return render_template(
        "home.html",
        saldo=saldo
    )


# Página de login
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/games/tigrinho")
def tigrinho():
    return render_template("games/Tigrinho.html")

# Página de cadastro
@app.route("/register")
def register():
    return render_template("register.html")


# Receber cadastro
@app.route("/cadastrar", methods=["POST"])
def cadastrar():

    nome = request.form["usuario"]
    email = request.form["email"]

    con = conectar()
    cursor = con.cursor()

    cursor.execute(
        "SELECT 1 FROM usuarios WHERE email = ?",
        (email,)
    )

    if cursor.fetchone():
        con.close()
        flash("email já cadastrado.")
        return redirect(url_for("register"))
    
    senha = request.form["senha"]
    confirmar = request.form["confirmar_senha"]

    if senha != confirmar:
        flash("senhas não coincidem.")
        return redirect(url_for("register"))

    senha = hashlib.sha256(senha.encode()).hexdigest()

    try:
        cursor.execute("""
            INSERT INTO usuarios
            (nome, email, senha, saldo)
            VALUES (?, ?, ?, ?)
        """, (nome, email, senha, 0))

        con.commit()

    except sqlite3.IntegrityError:
        flash("algo deu errado, tente novamente.")
        return redirect(url_for("register"))

    finally:
        con.close()

    flash("Conta criada com sucesso!")
    return redirect(url_for("login"))


# Receber login
@app.route("/entrar", methods=["POST"])
def entrar():

    email = request.form["email"]
    senha = hashlib.sha256(
        request.form["senha"].encode()
    ).hexdigest()

    con = conectar()
    cursor = con.cursor()

    cursor.execute("""
        SELECT * FROM usuarios
        WHERE email=? AND senha=?
    """, (email, senha))

    usuario = cursor.fetchone()

    con.close()

    if usuario:
        session["usuario_id"] = usuario[0]
        session["nome"] = usuario[1]
        session["saldo"] = usuario[4]

        return redirect(url_for("home"))
    else:
        flash("Email ou senha incorretos.")
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
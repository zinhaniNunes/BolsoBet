from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import hashlib

app = Flask(__name__)


# Conectar ao banco
def conectar():
    return sqlite3.connect("usuarios.db")


# Página inicial
@app.route("/")
def home():
    return render_template("home.html")


# Página de login
@app.route("/login")
def login():
    return render_template("login.html")


# Página de cadastro
@app.route("/register")
def register():
    return render_template("register.html")


# Receber cadastro
@app.route("/cadastrar", methods=["POST"])
def cadastrar():

    nome = request.form["usuario"]
    email = request.form["email"]
    senha = hashlib.sha256(
        request.form["senha"].encode()
    ).hexdigest()

    con = conectar()
    cursor = con.cursor()

    cursor.execute("""
        INSERT INTO usuarios
        (nome,email,senha,saldo)
        VALUES(?,?,?,?)
    """, (nome, email, senha, 0))

    con.commit()
    con.close()

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
        return "Login realizado!"
    else:
        return "Email ou senha incorretos."


if __name__ == "__main__":
    app.run(debug=True)
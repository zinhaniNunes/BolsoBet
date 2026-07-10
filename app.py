from flask import Flask, render_template, request, redirect, url_for, flash, session
from pathlib import Path
from flask import jsonify
import sqlite3
import hashlib
import secrets
import tigrinho

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
        "SELECT nome, saldo FROM usuarios WHERE id=?",
        (session["usuario_id"],)
    )

    usuario = cursor.fetchone()
    con.close()

    session["nome"] = usuario[0]
    session["saldo"] = usuario[1]

    return render_template("home.html")


# Página de login
@app.route("/login")
def login():
    return render_template("login.html")

#jogos
@app.route("/games/tigrinho")
def pagina_tigrinho():
    return render_template("games/Tigrinho.html")
@app.route("/spin", methods=["POST"])
def spin():

    # Verifica se está logado
    if "usuario_id" not in session:
        return jsonify({"erro": "Faça login"}), 401

    aposta = float(request.json["aposta"])

    # Conecta ao banco
    con = conectar()
    cursor = con.cursor()

    # Busca o saldo do usuário
    cursor.execute("""
        SELECT saldo
        FROM usuarios
        WHERE id = ?
    """, (session["usuario_id"],))

    saldo = cursor.fetchone()[0]

    # Verifica se a aposta é válida
    if aposta <= 0:
        con.close()
        return jsonify({"erro": "Aposta inválida"}), 400

    if aposta > saldo:
        con.close()
        return jsonify({"erro": "Saldo insuficiente"}), 400

    # Executa o jogo
    resultado = tigrinho.jogar(aposta)

    # Atualiza o saldo
    saldo = saldo - aposta
    saldo += resultado["ganho"]

    # Salva no banco
    cursor.execute("""
        UPDATE usuarios
        SET saldo = ?
        WHERE id = ?
    """, (saldo, session["usuario_id"]))

    con.commit()
    con.close()

    # Atualiza a sessão
    session["saldo"] = saldo

    # Envia o resultado para a página
    return jsonify({
        "matriz": resultado["matriz"],
        "ganho": resultado["ganho"],
        "spin_bonus": resultado["spin_bonus"],
        "saldo": saldo
    })

#Página de depósito
@app.route("/deposito")
def deposito():

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    return render_template("deposito.html")

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

        print("\033[32mUsuário logado:\033[0m", session["nome"])

        return redirect(url_for("home"))

    else:
        flash("Email ou senha incorretos.")
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

#add credit to the user
@app.route("/depositar", methods=["POST"])
def depositar():

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    valor = float(request.form["valor"])

    con = conectar()
    cursor = con.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET saldo = saldo + ?
        WHERE id = ?
    """, (valor, session["usuario_id"]))

    con.commit()

    cursor.execute("""
        SELECT saldo
        FROM usuarios
        WHERE id = ?
    """, (session["usuario_id"],))

    session["saldo"] = cursor.fetchone()[0]

    con.close()

    flash("Crédito adicionado com sucesso!")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
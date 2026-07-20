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

@app.route("/saldo")
def saldo():
    return {
        "saldo": session["saldo"]
    }

@app.route("/spin", methods=["POST"])
def spin():

    # Verifica se está logado
    if "usuario_id" not in session:
        return jsonify({"erro": "Faça login"}), 401

    aposta = float(request.json["aposta"])
    spins = int(request.json["comprar_spins"])

    # Conecta ao banco
    con = conectar()
    cursor = con.cursor()

    # Busca o saldo
    cursor.execute("""
        SELECT saldo
        FROM usuarios
        WHERE id = ?
    """, (session["usuario_id"],))

    saldo = cursor.fetchone()[0]

    # Validações
    if aposta <= 0:
        con.close()
        return jsonify({"erro": "Aposta inválida"}), 400

    if spins <= 0:
        con.close()
        return jsonify({"erro": "Quantidade de spins inválida"}), 400

    custo = aposta * spins

    if saldo < custo:
        con.close()
        return jsonify({"erro": "Saldo insuficiente"}), 400

    # Cobra todas as spins antecipadamente
    saldo -= custo

    resultados = []
    ganho_total = 0
    lista_ganho = []

    while spins > 0:

        spins -= 1

        resultado = tigrinho.jogar(aposta)

        ganho_total += resultado["ganho"]

        # adiciona spins bônus
        spins += resultado["spin_bonus"]

        resultados.append(resultado)

    # Soma os ganhos ao saldo
    saldo += ganho_total

    # Salva no banco
    cursor.execute("""
        UPDATE usuarios
        SET saldo = ?
        WHERE id = ?
    """, (saldo, session["usuario_id"]))

    con.commit()
    con.close()

    session["saldo"] = saldo

    return jsonify({
        "resultados": resultados,
        "ganho_total": ganho_total,
        "saldo": saldo,
        "lista_ganho": lista_ganho
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
    print("\033[33mUsuário deslogado:\033[0m", session["nome"])
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
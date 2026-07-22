from flask import Flask, render_template, request, redirect, url_for, flash, session
from pathlib import Path
from flask import jsonify
import sqlite3
import hashlib
import secrets
import tigrinho
import slot_cassino
import slot_pirata
import slot_king
import slot_brasil
import slot_classic
import slot_zeus
import slot_egito

# import slot_zeus, slot_egito, slot_pirata, slot_king, slot_brasil, slot_classic  # crie seguindo o mesmo padrão

app = Flask(__name__)

# Registro central: cada jogo é um módulo com uma função jogar(aposta)
JOGOS = {
    "tigrinho": tigrinho,
    "fortune-cassino": slot_cassino,
    "pirate-fortune": slot_pirata,
    "zeus-fortune": slot_zeus,
    "cleopatra-fortune": slot_egito,
    "brasil-mega-wins": slot_brasil,
    "classic-slot": slot_classic,
    "fortune-king": slot_king,
}
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
    session["jogo_atual"] = "tigrinho"
    return render_template("games/Tigrinho.html")

@app.route("/games/fortune-cassino")
def fortune_cassino():
    session["jogo_atual"] = "fortune-cassino"
    return render_template("games/slot-cassino.html")

@app.route("/games/pirate-fortune")
def pirate_fortune():
    session["jogo_atual"] = "pirate-fortune"  # crie slot_pirata.py e registre em JOGOS
    return render_template("games/slot-pirata.html")

@app.route("/games/zeus-fortune")
def zeus_fortune():
    session["jogo_atual"] = "zeus-fortune"  # crie slot_zeus.py e registre em JOGOS
    return render_template("games/slot-zeus.html")

@app.route("/games/cleopatra-fortune")
def cleopatra_fortune():
    session["jogo_atual"] = "cleopatra-fortune"  # crie slot_egito.py e registre em JOGOS
    return render_template("games/slot-egito.html")

@app.route("/games/brasil-mega-wins")
def brasil_mega_wins():
    session["jogo_atual"] = "brasil-mega-wins"  # crie slot_brasil.py e registre em JOGOS
    return render_template("games/slot-Brasil.html")

@app.route("/games/classic-slot")
def classic_slot():
    session["jogo_atual"] = "classic-slot"  # crie slot_classic.py e registre em JOGOS
    return render_template("games/slot-classic.html")

@app.route("/games/fortune-king")
def fortune_king():
    session["jogo_atual"] = "fortune-king"  # crie slot_king.py e registre em JOGOS
    return render_template("games/slot-fortune-King.html")

@app.route("/games/21")
def vinte_um():
    return render_template("games/21.html")

@app.route("/games/roleta")
def roleta():
    return render_template("games/roleta.html")

@app.route("/games/fortune-mines")
def fortune_mines():
    return render_template("games/fortune-mines.html")

@app.route("/games/aviator")
def aviator():
    return render_template("games/aviator.html")

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

    jogo = JOGOS.get(session.get("jogo_atual"))
    if jogo is None:
        return jsonify({"erro": "Jogo inválido ou sessão expirada"}), 400

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
    saldo_rodando = saldo  # já descontada a aposta

    while spins > 0:
        spins -= 1

        resultado = jogo.jogar(aposta)

        ganho_total += resultado["ganho"]
        saldo_rodando += resultado["ganho"]     
        resultado["saldo"] = saldo_rodando

        spins += resultado["spin_bonus"]
        resultados.append(resultado)

    # saldo final = saldo_rodando (já tem aposta descontada + todos os ganhos somados)
    saldo = saldo_rodando

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
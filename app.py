from flask import Flask, render_template, request, redirect, url_for, flash, session
from pathlib import Path
from flask import jsonify
import sqlite3
import hashlib
import secrets
import random
from math import comb
import tigrinho
import slot_cassino
import slot_pirata
import slot_king
import slot_brasil
import slot_classic
import slot_zeus
import slot_egito
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

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

MINES_ATIVOS = {}

TABULEIRO_TOTAL = 36  # grid 6x6
MINES_APOSTA_MINIMA = 0.40
MINES_BOMBAS_MIN = 25
MINES_BOMBAS_MAX = 35


def mines_multiplicador(bomba_in_game, jogadas):
    if jogadas <= 0:
        return 0
    elif jogadas < 3:
        retorno = jogadas*(1/2)*(bomba_in_game/25)
        return retorno
    else:
        retorno = jogadas*(2/5.5)*(bomba_in_game/25)
        return retorno


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
@login_required
def pagina_tigrinho():
    session["jogo_atual"] = "tigrinho"
    return render_template("games/Tigrinho.html")

@app.route("/games/fortune-cassino")
@login_required
def fortune_cassino():
    session["jogo_atual"] = "fortune-cassino"
    return render_template("games/slot-cassino.html")

@app.route("/games/slot-pirata")
@login_required
def pirate_fortune():
    session["jogo_atual"] = "pirate-fortune"
    return render_template("games/slot-pirata.html")

@app.route("/games/slot-zeus")
@login_required
def zeus_fortune():
    session["jogo_atual"] = "zeus-fortune"
    return render_template("games/slot-zeus.html")

@app.route("/games/slot-egito")
@login_required
def cleopatra_fortune():
    session["jogo_atual"] = "cleopatra-fortune"
    return render_template("games/slot-egito.html")

@app.route("/games/slot-brasil")
@login_required
def brasil_mega_wins():
    session["jogo_atual"] = "brasil-mega-wins"
    return render_template("games/slot-brasil.html")

@app.route("/games/slot-classic")
@login_required
def classic_slot():
    session["jogo_atual"] = "classic-slot"
    return render_template("games/slot-classic.html")

@app.route("/games/slot-king")
@login_required
def fortune_king():
    session["jogo_atual"] = "fortune-king"
    return render_template("games/slot-king.html")

@app.route("/games/21")
@login_required
def vinte_um():
    return render_template("games/21.html")

@app.route("/games/roleta")
@login_required
def roleta():
    return render_template("games/roleta.html")

@app.route("/games/fortune-mines")
@login_required
def fortune_mines():
    return render_template("games/fortune-mines.html")


@app.route("/mines/iniciar", methods=["POST"])
@login_required
def mines_iniciar():

    dados = request.get_json(silent=True) or {}

    try:
        aposta = float(dados.get("aposta"))
        num_bombas = int(dados.get("bombas"))
    except (TypeError, ValueError):
        return jsonify({"erro": "Dados inválidos"}), 400

    if aposta < MINES_APOSTA_MINIMA:
        return jsonify({"erro": f"Aposta mínima de R$ {MINES_APOSTA_MINIMA:.2f}"}), 400

    if num_bombas < MINES_BOMBAS_MIN or num_bombas > MINES_BOMBAS_MAX:
        return jsonify({"erro": f"Escolha entre {MINES_BOMBAS_MIN} e {MINES_BOMBAS_MAX} bombas"}), 400

    usuario_id = session["usuario_id"]

    if usuario_id in MINES_ATIVOS and MINES_ATIVOS[usuario_id]["ativo"]:
        return jsonify({"erro": "Você já tem uma rodada em andamento"}), 400

    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT saldo FROM usuarios WHERE id = ?", (usuario_id,))
    saldo = cursor.fetchone()[0]

    if aposta > saldo:
        con.close()
        return jsonify({"erro": "Saldo insuficiente"}), 400

    saldo -= aposta

    cursor.execute("UPDATE usuarios SET saldo = ? WHERE id = ?", (saldo, usuario_id))
    con.commit()
    con.close()

    session["saldo"] = saldo

    # Sorteia as posições das bombas no grid 6x6
    bombas = set()
    while len(bombas) < num_bombas:
        linha = random.randint(0, 5)
        coluna = random.randint(0, 5)
        bombas.add((linha, coluna))

    MINES_ATIVOS[usuario_id] = {
        "aposta": aposta,
        "num_bombas": num_bombas,
        "bombas": bombas,
        "abertas": set(),
        "jogadas": 0,
        "ativo": True,
    }

    return jsonify({"saldo": saldo, "multiplicador": 0.0})


@app.route("/mines/abrir", methods=["POST"])
@login_required
def mines_abrir():

    usuario_id = session["usuario_id"]
    jogo = MINES_ATIVOS.get(usuario_id)

    if not jogo or not jogo["ativo"]:
        return jsonify({"erro": "Nenhuma rodada em andamento"}), 400

    dados = request.get_json(silent=True) or {}

    try:
        linha = int(dados.get("linha"))
        coluna = int(dados.get("coluna"))
    except (TypeError, ValueError):
        return jsonify({"erro": "Coordenadas inválidas"}), 400

    if not (0 <= linha <= 5 and 0 <= coluna <= 5):
        return jsonify({"erro": "Coordenadas fora do tabuleiro"}), 400

    if (linha, coluna) in jogo["abertas"]:
        return jsonify({"erro": "Essa casa já foi aberta"}), 400

    jogo["abertas"].add((linha, coluna))

    if (linha, coluna) in jogo["bombas"]:
        jogo["ativo"] = False
        del MINES_ATIVOS[usuario_id]

        con = conectar()
        cursor = con.cursor()
        cursor.execute("SELECT saldo FROM usuarios WHERE id = ?", (usuario_id,))
        saldo = cursor.fetchone()[0]
        con.close()

        session["saldo"] = saldo

        return jsonify({
            "resultado": "bomba",
            "saldo": saldo,
            "bombas": [list(pos) for pos in jogo["bombas"]],
        })

    jogo["jogadas"] += 1
    mult = mines_multiplicador(jogo["num_bombas"], jogo["jogadas"])

    return jsonify({"resultado": "gema", "multiplicador": mult})


@app.route("/mines/sacar", methods=["POST"])
@login_required
def mines_sacar():

    usuario_id = session["usuario_id"]
    jogo = MINES_ATIVOS.get(usuario_id)

    if not jogo or not jogo["ativo"]:
        return jsonify({"erro": "Nenhuma rodada em andamento"}), 400

    mult = mines_multiplicador(jogo["num_bombas"], jogo["jogadas"])
    ganho = jogo["aposta"] * mult

    con = conectar()
    cursor = con.cursor()

    cursor.execute(
        "UPDATE usuarios SET saldo = saldo + ? WHERE id = ?",
        (ganho, usuario_id)
    )
    con.commit()

    cursor.execute("SELECT saldo FROM usuarios WHERE id = ?", (usuario_id,))
    saldo = cursor.fetchone()[0]
    con.close()

    session["saldo"] = saldo

    del MINES_ATIVOS[usuario_id]

    return jsonify({"saldo": saldo, "ganho": ganho})

@app.route("/games/aviator")
@login_required
def aviator():
    return render_template("games/aviator.html")

@app.route("/saldo")
@login_required
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
from flask import Flask, render_template, request, redirect, url_for, flash, session
from pathlib import Path
from flask import jsonify
import sqlite3
import hashlib
import secrets
import random
import time
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
    elif jogadas < 4:
        retorno = jogadas*(1/2)*(bomba_in_game/25)
        return retorno
    else:
        retorno = jogadas*(2/5)*(bomba_in_game/25)
        return retorno


AVIATOR_ATIVOS = {}

AVIATOR_APOSTA_MINIMA = 0.40
AVIATOR_VELOCIDADE = 2.0  # unidades de multiplicador por segundo


def aviator_gerar_crash():
    return max(1.00, round(random.expovariate(0.55), 2))


def aviator_multiplicador_atual(inicio):
    elapsed = time.time() - inicio
    return round(1.00 + elapsed * AVIATOR_VELOCIDADE, 2)


ROLETA_APOSTA_MINIMA = 0.40

# Roleta europeia: 37 casas (0 a 36, sem "00")
ROLETA_VERMELHOS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}

ROLETA_MULTIPLICADORES = {
    "numero": 36,   
    "duzia": 3, 
    "externo": 2,   
}


def roleta_cor(numero):
    if numero == 0:
        return "green"
    return "red" if numero in ROLETA_VERMELHOS else "black"


def roleta_paridade(numero):
    if numero == 0:
        return None
    return "par" if numero % 2 == 0 else "impar"


def roleta_duzia(numero):
    if numero == 0:
        return None
    if numero <= 12:
        return "1"
    if numero <= 24:
        return "2"
    return "3"


def roleta_venceu(tipo, valor, numero):
    if tipo == "numero":
        return valor == numero
    if tipo == "duzia":
        return roleta_duzia(numero) == valor
    if tipo == "externo":
        if valor in ("red", "black"):
            return roleta_cor(numero) == valor
        if valor in ("par", "impar"):
            return roleta_paridade(numero) == valor
        if valor == "1~18":
            return 1 <= numero <= 18
        if valor == "19~36":
            return 19 <= numero <= 36
    return False


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
    session["jogo_atual"] = "roleta"
    return render_template("games/roleta.html", vermelhos=ROLETA_VERMELHOS)


@app.route("/roleta/girar", methods=["POST"])
@login_required
def roleta_girar():

    usuario_id = session["usuario_id"]
    dados = request.get_json(silent=True) or {}

    tipo = dados.get("tipo")
    valor = dados.get("valor")

    try:
        aposta = round(float(dados.get("aposta")), 2)
    except (TypeError, ValueError):
        return jsonify({"erro": "Aposta inválida"}), 400

    if aposta < ROLETA_APOSTA_MINIMA:
        return jsonify({"erro": f"Aposta mínima de R$ {ROLETA_APOSTA_MINIMA:.2f}"}), 400

    multiplicador = ROLETA_MULTIPLICADORES.get(tipo)
    if multiplicador is None:
        return jsonify({"erro": "Tipo de aposta inválido"}), 400

    if tipo == "numero":
        try:
            valor = int(valor)
        except (TypeError, ValueError):
            return jsonify({"erro": "Número inválido"}), 400
        if not (0 <= valor <= 36):
            return jsonify({"erro": "Escolha um número entre 0 e 36"}), 400

    elif tipo == "duzia":
        if valor not in ("1", "2", "3"):
            return jsonify({"erro": "Dúzia inválida"}), 400

    elif tipo == "externo":
        if valor not in ("red", "black", "par", "impar", "1~18", "19~36"):
            return jsonify({"erro": "Aposta externa inválida"}), 400

    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT saldo FROM usuarios WHERE id = ?", (usuario_id,))
    saldo = cursor.fetchone()[0]

    aposta = round(aposta, 2)
    saldo = round(saldo, 2)

    if aposta > saldo:
        con.close()
        return jsonify({"erro": "Saldo insuficiente"}), 400

    numero_sorteado = random.randint(0, 36)
    venceu = roleta_venceu(tipo, valor, numero_sorteado)

    saldo -= aposta
    premio = 0.0
    if venceu:
        premio = round(aposta * multiplicador, 2)
        saldo += premio

    cursor.execute("UPDATE usuarios SET saldo = ? WHERE id = ?", (saldo, usuario_id))
    con.commit()
    con.close()

    session["saldo"] = saldo

    return jsonify({
        "numero": numero_sorteado,
        "cor": roleta_cor(numero_sorteado),
        "venceu": venceu,
        "premio": premio,
        "saldo": saldo,
    })

@app.route("/games/fortune-mines")
@login_required
def fortune_mines():
    return render_template("games/fortune-mines.html")


@app.route("/mines/status")
@login_required
def mines_status():
    usuario_id = session["usuario_id"]
    jogo = MINES_ATIVOS.get(usuario_id)

    if not jogo or not jogo["ativo"]:
        return jsonify({"ativo": False})

    mult = mines_multiplicador(jogo["num_bombas"], jogo["jogadas"])
    return jsonify({
        "ativo": True,
        "aposta": jogo["aposta"],
        "num_bombas": jogo["num_bombas"],
        "abertas": [list(pos) for pos in jogo["abertas"]],
        "multiplicador": mult,
    })


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

    aposta = round(aposta, 2)
    saldo = round(saldo, 2)

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
    session["jogo_atual"] = "aviator"
    return render_template("games/aviator.html")


@app.route("/aviator/apostar", methods=["POST"])
@login_required
def aviator_apostar():

    usuario_id = session["usuario_id"]

    dados = request.get_json(silent=True) or {}

    try:
        aposta = round(float(dados.get("aposta")), 2)
    except (TypeError, ValueError):
        return jsonify({"erro": "Aposta inválida"}), 400

    rodada = AVIATOR_ATIVOS.get(usuario_id)
    if rodada and rodada.get("ativo"):
        return jsonify({"erro": "Você já tem uma aposta em andamento"}), 400

    if aposta < AVIATOR_APOSTA_MINIMA:
        return jsonify({"erro": f"Aposta mínima de R$ {AVIATOR_APOSTA_MINIMA:.2f}"}), 400

    con = conectar()
    cursor = con.cursor()

    cursor.execute("SELECT saldo FROM usuarios WHERE id = ?", (usuario_id,))
    saldo = cursor.fetchone()[0]

    aposta = round(aposta, 2)
    saldo = round(saldo, 2)

    if aposta > saldo:
        con.close()
        return jsonify({"erro": "Saldo insuficiente"}), 400

    saldo -= aposta

    cursor.execute("UPDATE usuarios SET saldo = ? WHERE id = ?", (saldo, usuario_id))
    con.commit()
    con.close()

    session["saldo"] = saldo

    AVIATOR_ATIVOS[usuario_id] = {
        "aposta": aposta,
        "crash": aviator_gerar_crash(),
        "inicio": time.time(),
        "ativo": True,
    }

    return jsonify({"saldo": saldo})


@app.route("/aviator/status")
@login_required
def aviator_status():

    usuario_id = session["usuario_id"]
    rodada = AVIATOR_ATIVOS.get(usuario_id)

    if not rodada or not rodada.get("ativo"):
        return jsonify({"ativa": False})

    mult = aviator_multiplicador_atual(rodada["inicio"])
    crash = rodada["crash"]

    if mult >= crash:
        rodada["ativo"] = False
        return jsonify({
            "ativa": False,
            "caiu": True,
            "multiplicador": crash,
            "saldo": session.get("saldo"),
        })

    return jsonify({
        "ativa": True,
        "caiu": False,
        "multiplicador": mult,
        "saldo": session.get("saldo"),
    })


@app.route("/aviator/sacar", methods=["POST"])
@login_required
def aviator_sacar():

    usuario_id = session["usuario_id"]
    rodada = AVIATOR_ATIVOS.get(usuario_id)

    if not rodada or not rodada.get("ativo"):
        return jsonify({"erro": "Nenhuma aposta em andamento"}), 400

    mult = aviator_multiplicador_atual(rodada["inicio"])
    crash = rodada["crash"]

    if mult >= crash:
        rodada["ativo"] = False
        return jsonify({
            "ok": False,
            "caiu": True,
            "multiplicador": crash,
            "saldo": session.get("saldo"),
        })

    premio = round(rodada["aposta"] * mult, 2)

    con = conectar()
    cursor = con.cursor()

    cursor.execute(
        "UPDATE usuarios SET saldo = saldo + ? WHERE id = ?",
        (premio, usuario_id)
    )
    con.commit()

    cursor.execute("SELECT saldo FROM usuarios WHERE id = ?", (usuario_id,))
    saldo = cursor.fetchone()[0]
    con.close()

    session["saldo"] = saldo
    rodada["ativo"] = False

    return jsonify({
        "ok": True,
        "caiu": False,
        "multiplicador": mult,
        "premio": premio,
        "saldo": saldo,
    })


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

    custo = round(aposta * spins, 2)

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
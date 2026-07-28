import slot_engine as engine

CONFIG = {
    "linhas": 4,
    "colunas": 3,
    "simbolos": ["🏺","🐫","🪲","🌞","🪙","🐱"],
    "pesos":    [35, 26, 19, 12, 6, 2],
    "premios": {
        "🏺": {3: 1.20, 4: 1.30},
        "🐫": {3: 1.30, 4: 1.40},
        "🪲": {3: 1.40, 4: 1.50},
        "🌞": {3: 1.50, 4: 3.50},
        "🪙": {3: 3.50, 4: 6.00},
        "🐱": {3: 6.00, 4: 12.00},
    },
    # esse jogo não tem símbolo de bônus/giros grátis por enquanto
    "simbolo_bonus": None,
}


def jogar(aposta):
    return engine.jogar(aposta, CONFIG)

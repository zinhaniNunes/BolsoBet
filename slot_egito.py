import slot_engine as engine

CONFIG = {
    "linhas": 4,
    "colunas": 3,
    "simbolos": ["🏺","🐫","🪲","🌞","🪙","🐱"],
    "pesos":    [35, 26, 19, 12, 6, 2],
    "premios": {
        "🏺": {3: 0.30, 4: 0.50, 5: 1.00},
        "🐫": {3: 0.45, 4: 0.90, 5: 2.00},
        "🪲": {3: 0.60, 4: 1.40, 5: 3.50},
        "🌞": {3: 1.00, 4: 2.50, 5: 6.00},
        "🪙": {3: 2.00, 4: 6.00, 5: 15.00},
        "🐱": {3: 4.00, 4: 12.00, 5: 30.00},
    },
    # esse jogo não tem símbolo de bônus/giros grátis por enquanto
    "simbolo_bonus": None,
}


def jogar(aposta):
    return engine.jogar(aposta, CONFIG)

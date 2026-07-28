import slot_engine as engine

CONFIG = {
    "linhas": 5,
    "colunas": 3,
    "simbolos": ["🏺","🍇","📜","🍷","🏛️","⚡"],
    "pesos":    [35, 26, 19, 12, 6, 2],
    "premios": {
        "🏺": {3: 0.60, 4: 0.70, 5: 1.10},
        "🍇": {3: 0.70, 4: 1.10, 5: 1.40},
        "📜": {3: 1.10, 4: 1.40, 5: 3.50},
        "🍷": {3: 1.40, 4: 3.50, 5: 6.00},
        "🏛️": {3: 3.50, 4: 6.00, 5: 15.00},
        "⚡": {3: 6.00, 4: 12.00, 5: 30.00},
    },
    # esse jogo não tem símbolo de bônus/giros grátis por enquanto
    "simbolo_bonus": None,
}


def jogar(aposta):
    return engine.jogar(aposta, CONFIG)

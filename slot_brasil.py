import slot_engine as engine

CONFIG = {
    "linhas": 4,
    "colunas": 4,
    "simbolos": ["🍊","🍹","🌴","⚽","🏆","🇧🇷"],
    "pesos":    [35, 26, 19, 12, 6, 2],
    "premios": {
        "🍊": {3: 0.30, 4: 0.50},
        "🍹": {3: 0.50, 4: 0.70},
        "🌴": {3: 0.70, 4: 1.00},
        "⚽": {3: 1.00, 4: 2.00},
        "🏆": {3: 2.00, 4: 6.00},
        "🇧🇷": {3: 6.00, 4: 12.00},
    },
    # esse jogo não tem símbolo de bônus/giros grátis por enquanto
    "simbolo_bonus": None,
}


def jogar(aposta):
    return engine.jogar(aposta, CONFIG)

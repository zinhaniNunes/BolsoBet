import slot_engine as engine

CONFIG = {
    "linhas": 3,
    "colunas": 3,
    "simbolos": ["🍒","🍋","🍊","⭐","🍀","💎"],
    "pesos":    [35, 26, 19, 12, 6, 2],
    "premios": {
        "🍒": {3: 1.65},
        "🍋": {3: 1.75},
        "🍊": {3: 1.80},
        "⭐": {3: 2.50},
        "🍀": {3: 3.50},
        "💎": {3: 6.00},
    },
    # esse jogo não tem símbolo de bônus/giros grátis por enquanto
    "simbolo_bonus": None,
}


def jogar(aposta):
    return engine.jogar(aposta, CONFIG)

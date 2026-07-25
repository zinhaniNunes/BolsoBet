import slot_engine as engine

CONFIG = {
    "linhas": 3,
    "colunas": 3,
    "simbolos": ["🍒","🍋","🍊","⭐","🍀","💎"],
    "pesos":    [35, 26, 19, 12, 6, 2],
    "premios": {
        "🍒": {3: 0.30},
        "🍋": {3: 0.45},
        "🍊": {3: 0.60},
        "⭐": {3: 1.00},
        "🍀": {3: 2.00},
        "💎": {3: 4.00},
    },
    # esse jogo não tem símbolo de bônus/giros grátis por enquanto
    "simbolo_bonus": None,
}


def jogar(aposta):
    return engine.jogar(aposta, CONFIG)

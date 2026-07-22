import slot_engine as engine

CONFIG = {
    "simbolos": ["🍒", "🍊", "🪙", "🧧", "🪭", "🥁", "👑", "💎", "⭐", "🐯"],
    "pesos":    [40, 30, 22, 16, 11, 7, 3, 0.8, 0.15, 0.05],
    "premios": {
        "🍒": {3: 0.35, 4: 0.40, 5: 0.60},
        "🍊": {3: 0.50, 4: 0.65, 5: 0.90},
        "🪙": {3: 0.55, 4: 0.70, 5: 1.50},
        "🧧": {3: 0.50, 4: 1.00, 5: 2.20},
        "🪭": {3: 0.70, 4: 1.60, 5: 3.50},
        "🥁": {3: 1.10, 4: 2.80, 5: 6.00},
        "👑": {3: 1.90, 4: 5.00, 5: 12.00},
        "💎": {3: 3.60, 4: 10.00, 5: 25.00},
        "⭐": {3: 6.10, 4: 20.00, 5: 50.00},
        # 🐯 não entra na tabela de prêmios comuns: ele é o símbolo de
        # bônus, tratado por "simbolo_bonus" abaixo.
    },
    "simbolo_bonus": "🐯",
    "area_bonus": (3, 3),  # canto superior-esquerdo 3x3, igual ao original
}


def jogar(aposta):
    return engine.jogar(aposta, CONFIG)

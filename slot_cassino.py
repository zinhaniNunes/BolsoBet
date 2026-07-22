import slot_engine as engine

# Tema "fortune-cassino" — mesma estrutura do tigrinho, só troca
# símbolos, pesos e a tabela de prêmios. Ajuste os valores como quiser,
# a lógica de linha/coluna/diagonal é a mesma pra todos os jogos.
CONFIG = {
    "linhas": 3,
    "colunas": 5,
    "simbolos": ["🍒", "🎲", "🃏", "🍀", "💰", "7️⃣"],
    "pesos":    [35, 26, 19, 12, 6, 2],
    "premios": {
        "🍒": {3: 0.30, 4: 0.50, 5: 1.00},
        "🎲": {3: 0.45, 4: 0.90, 5: 2.00},
        "🃏": {3: 0.60, 4: 1.40, 5: 3.50},
        "🍀": {3: 1.00, 4: 2.50, 5: 6.00},
        "💰": {3: 2.00, 4: 6.00, 5: 15.00},
        "7️⃣": {3: 4.00, 4: 12.00, 5: 30.00},
    },
    # esse jogo não tem símbolo de bônus/giros grátis por enquanto
    "simbolo_bonus": None,
}


def jogar(aposta):
    return engine.jogar(aposta, CONFIG)

#imports
import random

#variaveis
simbolos = ["🍒","🍊","🪙","🧧","🪭","🥁","👑","💎","⭐","🐯"]
pesos = [40,30,22,16,11,7,3,0.8,0.15,0.05]
premios = {
    "🍒": {3: 0.35, 4: 0.40, 5: 0.60},
    "🍊": {3: 0.50, 4: 0.65, 5: 0.90},
    "🪙": {3: 0.55, 4: 0.70, 5: 1.50},
    "🧧": {3: 0.50, 4: 1.00, 5: 2.20},
    "🪭": {3: 0.70, 4: 1.60, 5: 3.50},
    "🥁": {3: 1.10, 4: 2.80, 5: 6.00},
    "👑": {3: 1.90, 4: 5.00, 5: 12.00},
    "💎": {3: 3.60, 4: 10.00, 5: 25.00},
    "⭐": {3: 6.10, 4: 20.00, 5: 50.00}}

#funções
def girar():
    return random.choices(simbolos, weights=pesos, k=5)

def premio(matriz):
    tigrinho = 0
    ganho = 0
    spin_bonus = 0
    posicoes = set()

    # LINHAS
    for i in range(5):
        if matriz[i][0] == matriz[i][1] == matriz[i][2] == matriz[i][3] == matriz[i][4]:
            ganho += premios[matriz[i][0]][5]
            posicoes.update({(i,0),(i,1),(i,2),(i,3),(i,4)})
        elif matriz[i][0] == matriz[i][1] == matriz[i][2] == matriz[i][3]:
            ganho += premios[matriz[i][0]][4]
            posicoes.update({(i,0),(i,1),(i,2),(i,3)})
        elif matriz[i][1] == matriz[i][2] == matriz[i][3] == matriz[i][4]:
            ganho += premios[matriz[i][1]][4]
            posicoes.update({(i,1),(i,2),(i,3),(i,4)})
        elif matriz[i][0] == matriz[i][1] == matriz[i][2]:
            ganho += premios[matriz[i][0]][3]
            posicoes.update({(i,0),(i,1),(i,2)})
        elif matriz[i][1] == matriz[i][2] == matriz[i][3]:
            ganho += premios[matriz[i][1]][3]
            posicoes.update({(i,1),(i,2),(i,3)})
        elif matriz[i][2] == matriz[i][3] == matriz[i][4]:
            ganho += premios[matriz[i][2]][3]
            posicoes.update({(i,2),(i,3),(i,4)})

    # COLUNAS
    for j in range(5):
        if matriz[0][j] == matriz[1][j] == matriz[2][j] == matriz[3][j] == matriz[4][j]:
            ganho += premios[matriz[0][j]][5]
            posicoes.update({(0,j),(1,j),(2,j),(3,j),(4,j)})
        elif matriz[0][j] == matriz[1][j] == matriz[2][j] == matriz[3][j]:
            ganho += premios[matriz[0][j]][4]
            posicoes.update({(0,j),(1,j),(2,j),(3,j)})
        elif matriz[1][j] == matriz[2][j] == matriz[3][j] == matriz[4][j]:
            ganho += premios[matriz[1][j]][4]
            posicoes.update({(1,j),(2,j),(3,j),(4,j)})
        elif matriz[0][j] == matriz[1][j] == matriz[2][j]:
            ganho += premios[matriz[0][j]][3]
            posicoes.update({(0,j),(1,j),(2,j)})
        elif matriz[1][j] == matriz[2][j] == matriz[3][j]:
            ganho += premios[matriz[1][j]][3]
            posicoes.update({(1,j),(2,j),(3,j)})
        elif matriz[2][j] == matriz[3][j] == matriz[4][j]:
            ganho += premios[matriz[2][j]][3]
            posicoes.update({(2,j),(3,j),(4,j)})

    # DIAGONAIS (\)
    # Principal (5)
    if matriz[0][0] == matriz[1][1] == matriz[2][2] == matriz[3][3] == matriz[4][4]:
        ganho += premios[matriz[0][0]][5]
        posicoes.update({(0,0),(1,1),(2,2),(3,3),(4,4)})
    elif matriz[0][0] == matriz[1][1] == matriz[2][2] == matriz[3][3]:
        ganho += premios[matriz[0][0]][4]
        posicoes.update({(0,0),(1,1),(2,2),(3,3)})
    elif matriz[1][1] == matriz[2][2] == matriz[3][3] == matriz[4][4]:
        ganho += premios[matriz[1][1]][4]
        posicoes.update({(1,1),(2,2),(3,3),(4,4)})
    elif matriz[0][0] == matriz[1][1] == matriz[2][2]:
        ganho += premios[matriz[0][0]][3]
        posicoes.update({(0,0),(1,1),(2,2)})
    elif matriz[1][1] == matriz[2][2] == matriz[3][3]:
        ganho += premios[matriz[1][1]][3]
        posicoes.update({(1,1),(2,2),(3,3)})
    elif matriz[2][2] == matriz[3][3] == matriz[4][4]:
        ganho += premios[matriz[2][2]][3]
        posicoes.update({(2,2),(3,3),(4,4)})

    # Começando na linha 1
    if matriz[1][0] == matriz[2][1] == matriz[3][2] == matriz[4][3]:
        ganho += premios[matriz[1][0]][4]
        posicoes.update({(1,0),(2,1),(3,2),(4,3)})
    elif matriz[1][0] == matriz[2][1] == matriz[3][2]:
        ganho += premios[matriz[1][0]][3]
        posicoes.update({(1,0),(2,1),(3,2)})
    elif matriz[2][1] == matriz[3][2] == matriz[4][3]:
        ganho += premios[matriz[2][1]][3]
        posicoes.update({(2,1),(3,2),(4,3)})

    # Começando na linha 2
    if matriz[2][0] == matriz[3][1] == matriz[4][2]:
        ganho += premios[matriz[2][0]][3]
        posicoes.update({(2,0),(3,1),(4,2)})

    # Começando na coluna 1
    if matriz[0][1] == matriz[1][2] == matriz[2][3] == matriz[3][4]:
        ganho += premios[matriz[0][1]][4]
        posicoes.update({(0,1),(1,2),(2,3),(3,4)})
    elif matriz[0][1] == matriz[1][2] == matriz[2][3]:
        ganho += premios[matriz[0][1]][3]
        posicoes.update({(0,1),(1,2),(2,3)})
    elif matriz[1][2] == matriz[2][3] == matriz[3][4]:
        ganho += premios[matriz[1][2]][3]
        posicoes.update({(1,2),(2,3),(3,4)})

    # Começando na coluna 2
    if matriz[0][2] == matriz[1][3] == matriz[2][4]:
        ganho += premios[matriz[0][2]][3]
        posicoes.update({(0,2),(1,3),(2,4)})

    # DIAGONAIS (/)
    # Principal inversa (5)
    if matriz[0][4] == matriz[1][3] == matriz[2][2] == matriz[3][1] == matriz[4][0]:
        ganho += premios[matriz[0][4]][5]
        posicoes.update({(0,4),(1,3),(2,2),(3,1),(4,0)})
    elif matriz[0][4] == matriz[1][3] == matriz[2][2] == matriz[3][1]:
        ganho += premios[matriz[0][4]][4]
        posicoes.update({(0,4),(1,3),(2,2),(3,1)})
    elif matriz[1][3] == matriz[2][2] == matriz[3][1] == matriz[4][0]:
        ganho += premios[matriz[1][3]][4]
        posicoes.update({(1,3),(2,2),(3,1),(4,0)})
    elif matriz[0][4] == matriz[1][3] == matriz[2][2]:
        ganho += premios[matriz[0][4]][3]
        posicoes.update({(0,4),(1,3),(2,2)})
    elif matriz[1][3] == matriz[2][2] == matriz[3][1]:
        ganho += premios[matriz[1][3]][3]
        posicoes.update({(1,3),(2,2),(3,1)})
    elif matriz[2][2] == matriz[3][1] == matriz[4][0]:
        ganho += premios[matriz[2][2]][3]
        posicoes.update({(2,2),(3,1),(4,0)})

    # Começando na linha 1
    if matriz[1][4] == matriz[2][3] == matriz[3][2] == matriz[4][1]:
        ganho += premios[matriz[1][4]][4]
        posicoes.update({(1,4),(2,3),(3,2),(4,1)})
    elif matriz[1][4] == matriz[2][3] == matriz[3][2]:
        ganho += premios[matriz[1][4]][3]
        posicoes.update({(1,4),(2,3),(3,2)})
    elif matriz[2][3] == matriz[3][2] == matriz[4][1]:
        ganho += premios[matriz[2][3]][3]
        posicoes.update({(2,3),(3,2),(4,1)})

    # Começando na linha 2
    if matriz[2][4] == matriz[3][3] == matriz[4][2]:
        ganho += premios[matriz[2][4]][3]
        posicoes.update({(2,4),(3,3),(4,2)})

    # Começando na coluna 3
    if matriz[0][3] == matriz[1][2] == matriz[2][1] == matriz[3][0]:
        ganho += premios[matriz[0][3]][4]
        posicoes.update({(0,3),(1,2),(2,1),(3,0)})
    elif matriz[0][3] == matriz[1][2] == matriz[2][1]:
        ganho += premios[matriz[0][3]][3]
        posicoes.update({(0,3),(1,2),(2,1)})
    elif matriz[1][2] == matriz[2][1] == matriz[3][0]:
        ganho += premios[matriz[1][2]][3]
        posicoes.update({(1,2),(2,1),(3,0)})

    # Começando na coluna 2
    if matriz[0][2] == matriz[1][1] == matriz[2][0]:
        ganho += premios[matriz[0][2]][3]
        posicoes.update({(0,2),(1,1),(2,0)})

    for coluna in range(3):
        for linha in range(3):
            if matriz[linha][coluna] == "🐯":
                tigrinho += 1
    
    if tigrinho >= 1:
        spin_bonus += tigrinho

    # converte para lista de listas [linha, coluna] para poder virar JSON
    posicoes_lista = [[i, j] for (i, j) in posicoes]

    return ganho, spin_bonus, posicoes_lista

def jogar(aposta):

    matriz = []

    for i in range(5):
        matriz.append(girar())

    ganho, spin_bonus, posicoes = premio(matriz)

    return {
        "matriz": matriz,
        "ganho": ganho * aposta,
        "spin_bonus": spin_bonus,
        "multiplicador": ganho,
        "posicoes": posicoes,
    }

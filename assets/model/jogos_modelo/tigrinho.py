#imports
import random
import os
import time

#variaveis
saldo = 1000.00
spin = perdas = wins = 0
matriz_resultado = [[0],[0],[0],[0],[0]]
simbolos = ["🍒","👑","🥁","🪭","🧧","🪙","🍊","💎","⭐","🐯"]
pesos = [45,32,20,14,10,6,4,2,1,0.2]
premios = {"🍒": {3:0.128,4:0.25 ,5:0.5},
           "🍊": {3:0.25,4:0.5 ,5:1},
           "🪙": {3:0.375,4:0.75 ,5:1.5},
           "🧧": {3:0.5,4:1 ,5:2},
           "🪭": {3:0.75,4:1.5 ,5:3},
           "🥁": {3:1.25,4:2.5 ,5:5},
           "👑": {3:2,4:4 ,5:8},
           "💎": {3:3.75,4:7.5 ,5:15},
           "⭐": {3:5,4:10 ,5:20}}
bonus={3:1,4:2,5:5,6:30,7:50,8:100,9:500}

#funções
def girar():
    return random.choices(simbolos, weights=pesos, k=5)

def premio(matriz):
    sim=None
    tigrinho=ganho=spin= 0

    # LINHAS
    for i in range(5):
        if matriz[i][0] == matriz[i][1] == matriz[i][2] == matriz[i][3] == matriz[i][4]:
            ganho += premios[matriz[i][0]][5]
        elif matriz[i][0] == matriz[i][1] == matriz[i][2] == matriz[i][3]:
            ganho += premios[matriz[i][0]][4]
        elif matriz[i][1] == matriz[i][2] == matriz[i][3] == matriz[i][4]:
            ganho += premios[matriz[i][1]][4]
        elif matriz[i][0] == matriz[i][1] == matriz[i][2]:
            ganho += premios[matriz[i][0]][3]
        elif matriz[i][1] == matriz[i][2] == matriz[i][3]:
            ganho += premios[matriz[i][1]][3]
        elif matriz[i][2] == matriz[i][3] == matriz[i][4]:
            ganho += premios[matriz[i][2]][3]

    # COLUNAS
    for j in range(5):
        if matriz[0][j] == matriz[1][j] == matriz[2][j] == matriz[3][j] == matriz[4][j]:
            ganho += premios[matriz[0][j]][5]
        elif matriz[0][j] == matriz[1][j] == matriz[2][j] == matriz[3][j]:
            ganho += premios[matriz[0][j]][4]
        elif matriz[1][j] == matriz[2][j] == matriz[3][j] == matriz[4][j]:
            ganho += premios[matriz[1][j]][4]
        elif matriz[0][j] == matriz[1][j] == matriz[2][j]:
            ganho += premios[matriz[0][j]][3]
        elif matriz[1][j] == matriz[2][j] == matriz[3][j]:
            ganho += premios[matriz[1][j]][3]
        elif matriz[2][j] == matriz[3][j] == matriz[4][j]:
            ganho += premios[matriz[2][j]][3]

    # DIAGONAL PRINCIPAL (\)
    if matriz[0][0] == matriz[1][1] == matriz[2][2] == matriz[3][3] == matriz[4][4]:
        ganho += premios[matriz[0][0]][5]
    elif matriz[0][0] == matriz[1][1] == matriz[2][2] == matriz[3][3]:
        ganho += premios[matriz[0][0]][4]
    elif matriz[1][1] == matriz[2][2] == matriz[3][3] == matriz[4][4]:
        ganho += premios[matriz[1][1]][4]
    elif matriz[0][0] == matriz[1][1] == matriz[2][2]:
        ganho += premios[matriz[0][0]][3]
    elif matriz[1][1] == matriz[2][2] == matriz[3][3]:
        ganho += premios[matriz[1][1]][3]
    elif matriz[2][2] == matriz[3][3] == matriz[4][4]:
        ganho += premios[matriz[2][2]][3]
    if matriz[1][0] == matriz[2][1] == matriz[3][2]:
        ganho += premios[matriz[2][1]][3]
    if matriz[0][1] == matriz[1][2] == matriz[2][3]:
        ganho += premios[matriz[1][2]][3]

    # DIAGONAL SECUNDÁRIA (/)
    if matriz[4][0] == matriz[3][1] == matriz[2][2] == matriz[1][3] == matriz[0][4]:
        ganho += premios[matriz[4][0]][5]
    elif matriz[4][0] == matriz[3][1] == matriz[2][2] == matriz[1][3]:
        ganho += premios[matriz[4][0]][4]
    elif matriz[3][1] == matriz[2][2] == matriz[1][3] == matriz[0][4]:
        ganho += premios[matriz[3][1]][4]
    elif matriz[4][0] == matriz[3][1] == matriz[2][2]:
        ganho += premios[matriz[4][0]][3]
    elif matriz[3][1] == matriz[2][2] == matriz[1][3]:
        ganho += premios[matriz[3][1]][3]
    elif matriz[2][2] == matriz[1][3] == matriz[0][4]:
        ganho += premios[matriz[2][2]][3]
    if matriz[4][3] == matriz[3][2] == matriz[2][1]:
        ganho += premios[matriz[3][2]][3]
    if matriz[3][4] == matriz[2][3] == matriz[1][2]:
        ganho += premios[matriz[2][3]][3]


    for coluna in range(3):
        for linha in range(3):
            if matriz[linha][coluna] == "🐯":
                tigrinho += 1
    
    if tigrinho >= 3 and tigrinho < 6:
        spin += bonus[tigrinho]
    if tigrinho >= 6:
        ganho += bonus[tigrinho]

            
    return ganho, spin

def imprimir_matriz(matriz):
    print(f"saldo atual:{saldo:.2f}")
    print(f"spin restantes :{spin}")
    largura = max(len(str(num)) for linha in matriz for num in linha)
    for linha in matriz:
        print(" ".join(f"{num:>{largura}}" for num in linha))

#solta carta caralho!!!
while True:
    loopA = 0
    if spin ==0 and saldo > 0:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"vc tem agr {saldo:.2f} de saldo")
            aposta = float(input("Aposta (min 0.4): "))
            if aposta < 0.4:
                aposta = 0
            spin = int(input(f"spin (max {saldo/aposta:.0f}): "))
            if spin > (saldo/aposta):
                spin = 0
            if aposta*spin <= saldo and saldo > 0 and aposta > 0 and spin > 0:
                saldo -= aposta*spin
                break
    elif spin ==0 and saldo == 0:
        break
    while True:
        if loopA > 25:
            time.sleep(0.07)
        if loopA > 45:
            time.sleep(0.08)
        os.system('cls' if os.name == 'nt' else 'clear')
        loop=5
        while loop > 0:
            resultado = girar()
            loop-=1
            matriz_resultado[loop] = resultado
        imprimir_matriz(matriz_resultado)
        loopA += 1
        if loopA == 50:
            ganho, spin_bonus = premio(matriz_resultado)
            spin += spin_bonus
            break
    if ganho != 0 or spin_bonus != 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        imprimir_matriz(matriz_resultado)
        if ganho !=0:
            print(f'parabéns vc ganhou R${aposta+(aposta*ganho):.2f}🐯')
        if spin_bonus !=0:
            print(f'parabéns vc ganhou {spin_bonus} spins🐯')
            spin += spin_bonus
        saldo += aposta+aposta*ganho
        time.sleep(1)
        ganho = 0
        spin_bonus = 0
        wins +=1

    else:
        perdas +=1
    spin -= 1
    if saldo == 0 and spin == 0:
        break
print(f"vc tem agr {saldo:.2f} de saldo")
print(f"vc tem  {wins} de vitorias")
print(f"vc tem  {perdas} de derrotas")

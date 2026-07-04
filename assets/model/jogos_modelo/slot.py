#imports
import random
import os
import time

#variaveis
saldo=1000
matriz_resultado = [[0],[0],[0],]
simbolos = ["🍒","🍋","🍊","⭐","🍀","💎"]
pesos = [30,25,20,12,8,5]

#funções
def girar():
    return random.choices(simbolos, weights=pesos, k=5)

def premio(resultado):
    if resultado[0] == resultado[1] == resultado[2] == resultado[3] == resultado[4]:
        if resultado[0] == f"{simbolos[0]}":
            return 10
        elif resultado[0] == f"{simbolos[1]}":
            return 15
        elif resultado[0] == f"{simbolos[2]}":
            return 20
        elif resultado[0] == f"{simbolos[3]}":
            return 50
        elif resultado[0] == f"{simbolos[4]}":
            return 100
        elif resultado[0] == f"{simbolos[5]}":
            return 500
    return 0

def imprimir_matriz(matriz):
    largura = max(len(str(num)) for linha in matriz for num in linha)
    for linha in matriz:
        print(" ".join(f"{num:>{largura}}" for num in linha))

#roll
while True:
    loopA = 0
    while True:
        aposta = int(input("Aposta: "))
        if aposta <= saldo and saldo > 0 and aposta > 0:
            saldo -= aposta
            break
    while True:
        if loopA > 25:
            time.sleep(0.07)
        if loopA > 45:
            time.sleep(0.08)
        os.system('cls' if os.name == 'nt' else 'clear')
        loop=3
        while loop > 0:
            resultado = girar()
            loop-=1
            matriz_resultado[loop] = resultado
        imprimir_matriz(matriz_resultado)
        loopA += 1
        if loopA == 50:
            ganho = premio(matriz_resultado)
            break
    if ganho != 0:
        print(f'parabéns vc ganhou {aposta*ganho}')
    else:
        print('vc perdeu!')
    if saldo == 0:
        break
    if input('jogar novamente?') == "n":
        break
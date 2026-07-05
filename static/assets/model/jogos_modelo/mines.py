#import
import random
import os
import time
from math import comb


#var
saldo=1000
matriz_tela = [
    ['🪨','🪨','🪨','🪨','🪨'],
    ['🪨','🪨','🪨','🪨','🪨'],
    ['🪨','🪨','🪨','🪨','🪨'],
    ['🪨','🪨','🪨','🪨','🪨'],
    ['🪨','🪨','🪨','🪨','🪨'],]
matriz_real = [
    ['💎','💎','💎','💎','💎'],
    ['💎','💎','💎','💎','💎'],
    ['💎','💎','💎','💎','💎'],
    ['💎','💎','💎','💎','💎'],
    ['💎','💎','💎','💎','💎'],]

#def
def imprimir_matriz(matriz):
    largura = max(len(str(num)) for linha in matriz for num in linha)
    for linha in matriz:
        print(" ".join(f"{num:>{largura}}" for num in linha))

def multiplicador(bomba_in_game, jogadas, rtp=0.96):
    total = 25
    justo = comb(total, jogadas) / comb(total - bomba_in_game, jogadas)
    return justo * rtp

#loop game
while True:
    num_bomba = int(input("bombas(5~20): "))
    if num_bomba >=5 and num_bomba <= 20:
        bomba_in_game = num_bomba
        break
while True:
    aposta = int(input("Aposta: "))
    if aposta <= saldo and saldo > 0 and aposta > 0:
        saldo -= aposta
        break
    if saldo == 0:
        break
jogadas = 0
while num_bomba > 0:
    linha = random.randint(0, 4)
    coluna = random.randint(0, 4)
    if matriz_real[linha][coluna] != '💣':
        matriz_real[linha][coluna] = '💣'
        num_bomba -= 1
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    mult = multiplicador(bomba_in_game, jogadas, rtp=0.96)
    imprimir_matriz(matriz_tela)
    print(f'multiplicador:{mult}')
    entrada = input("coordenadas (linha coluna) ou x x para sacar: ").split()
    if entrada == ["x", "x"]:
        run = True
        break
    i, j = map(int, entrada)
    if matriz_real[i][j] == '💣':
        os.system('cls' if os.name == 'nt' else 'clear')
        matriz_tela[i][j] = '💣'
        imprimir_matriz(matriz_tela)
        print('vc perdeu caindo na bomba!')
        run = False
        break
    elif matriz_tela[i][j] != '💎':
        matriz_tela[i][j] = '💎'
        jogadas += 1
    else:
        print('casa ja aberta')
        time.sleep(1)
if run == True:
    saldo += mult * aposta
print (saldo)
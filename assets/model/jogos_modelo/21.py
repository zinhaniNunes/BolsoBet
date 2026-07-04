#impots
import random
import os

#variavel
baralho = ['A♠','2♠','3♠','4♠','5♠','6♠','7♠','8♠','9♠','10♠','J♠','Q♠','K♠',
         'A♥','2♥','3♥','4♥','5♥','6♥','7♥','8♥','9♥','10♥','J♥','Q♥','K♥',
         'A♦','2♦','3♦','4♦','5♦','6♦','7♦','8♦','9♦','10♦','J♦','Q♦','K♦',
         'A♣','2♣','3♣','4♣','5♣','6♣','7♣','8♣','9♣','10♣','J♣','Q♣','K♣']

dealer = []
jogador = []

baralho_As = {'A♠':11,'2♠':2,'3♠':3,'4♠':4,'5♠':5,'6♠':6,'7♠':7,'8♠':8,'9♠':9,'10♠':10,'J♠':10,'Q♠':10,'K♠':10,
           'A♥':11,'2♥':2,'3♥':3,'4♥':4,'5♥':5,'6♥':6,'7♥':7,'8♥':8,'9♥':9,'10♥':10,'J♥':10,'Q♥':10,'K♥':10,
           'A♦':11,'2♦':2,'3♦':3,'4♦':4,'5♦':5,'6♦':6,'7♦':7,'8♦':8,'9♦':9,'10♦':10,'J♦':10,'Q♦':10,'K♦':10,
           'A♣':11,'2♣':2,'3♣':3,'4♣':4,'5♣':5,'6♣':6,'7♣':7,'8♣':8,'9♣':9,'10♣':10,'J♣':10,'Q♣':10,'K♣':10}

baralho_as = {'A♠':1,'2♠':2,'3♠':3,'4♠':4,'5♠':5,'6♠':6,'7♠':7,'8♠':8,'9♠':9,'10♠':10,'J♠':10,'Q♠':10,'K♠':10,
           'A♥':1,'2♥':2,'3♥':3,'4♥':4,'5♥':5,'6♥':6,'7♥':7,'8♥':8,'9♥':9,'10♥':10,'J♥':10,'Q♥':10,'K♥':10,
           'A♦':1,'2♦':2,'3♦':3,'4♦':4,'5♦':5,'6♦':6,'7♦':7,'8♦':8,'9♦':9,'10♦':10,'J♦':10,'Q♦':10,'K♦':10,
           'A♣':1,'2♣':2,'3♣':3,'4♣':4,'5♣':5,'6♣':6,'7♣':7,'8♣':8,'9♣':9,'10♣':10,'J♣':10,'Q♣':10,'K♣':10}


#funções

def pescar(baralho):
    carta = random.choice(baralho)
    baralho.remove(carta)
    return carta , baralho

def contagem(mão):
    loop=0
    num=0
    pts=0
    while True:
        try:
            pts += baralho_As[mão[num]]
            num += 1
        except IndexError:
            break
    if (pts > 21) and ('A♠' in mão or 'A♥' in mão or 'A♦' in mão or 'A♣' in mão):
        if 'A♠' in mão:
            loop += 1
            pts -= 11
        if ('A♥'in mão) and pts > 21:
            loop += 1
        if ('A♦'in mão) and pts > 21:
            loop += 1
        if ('A♣'in mão) and pts > 21:
            loop += 1
        pts=0
        num=0
        while True:
            if loop > 0:
                try:
                    pts += baralho_as[mão[num]]
                    if 'A♠' == mão[num] or 'A♥' == mão[num] or 'A♦' == mão[num] or 'A♣' == mão[num]:
                        loop -= 1
                    num +=1
                except IndexError:
                    break
            else:
                try:
                    pts += baralho_As[mão[num]]
                    num += 1
                except IndexError:
                    break
    return pts

def ver_jogo_visivel(dealer,pts_dealer,jogador,pts_jogador):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(dealer,' ',pts_dealer)
    print(jogador,' ',pts_jogador)
    return

def ver_jogo_normal(dealer,baralho_As,jogador,pts_jogador):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{dealer[0]}+? {baralho_As[dealer[0]]}+?')
    print(jogador,' ',pts_jogador)

def ações_dealer(pts_jogador,pts_dealer,dealer,jogador,baralho):
    while pts_dealer < 17:
        carta , baralho = pescar(baralho)
        dealer.append(carta)
        pts_dealer=contagem(dealer)
    ver_jogo_visivel(dealer,pts_dealer,jogador,pts_jogador)
    if pts_dealer > 21:
        print ('\033[32mvc ganhou!, o dealer estourou')
        return 170
    elif pts_jogador == 21 and pts_dealer < 21:
        print("\033[32mvc ganhou por 21!")
        return 170
    elif pts_jogador == pts_dealer:
        print("empate, msm número de pontos")
        return 100
    elif pts_dealer > pts_jogador:
        print("\033[31mvc perdeu, o dealer tem mais pontos!")
        return 0
    else:
        print("\033[32mvc ganhou, vc tem mais pontos!")
        return 170

def ações_jogador(dealer,pts_jogador,pts_dealer,jogador,baralho):
    global stts
    game=True
    if pts_jogador < 21:
        while True:
            ações = input("oq vc faz: (compra/para) \n")
            if ações == 'compra':
                carta , baralho = pescar(baralho)
                jogador.append(carta)
                break
            if ações == 'para':
                stts = ações_dealer(pts_jogador,pts_dealer,dealer,jogador,baralho)
                game = False
                break
    if pts_jogador > 21:
        print ('\033[31mvc perdeu estourando!\033[0m')
        game = False
    if pts_jogador == 21:
        if len(jogador) == 2:
            if pts_jogador != pts_dealer:
                ver_jogo_visivel(dealer,pts_dealer,jogador,pts_jogador)
                print('\033[32mvc ganhou com um BlackJack!')
                stts = 205
                game = False
            else:
                ver_jogo_visivel(dealer,pts_dealer,jogador,pts_jogador)
                print('empate!,também o dealer tem um BlackJack!')
                stts = 100
                game = False
                
        elif pts_jogador != pts_dealer:
                ver_jogo_visivel(dealer,pts_dealer,jogador,pts_jogador)
                stts = ações_dealer(pts_jogador,pts_dealer,dealer,jogador,baralho)
                game = False
        else:
            ver_jogo_visivel(dealer,pts_dealer,jogador,pts_jogador)
            print('empate!, o dealer tem um BlackJack!')
            stts = 100
            game = False
    return jogador , stts , game , baralho

#jogo
loop = 2
while loop > 0:
    carta , baralho = pescar(baralho)
    dealer.append(carta)
    loop -= 1
loop = 2
while loop > 0:
    carta , baralho = pescar(baralho)
    jogador.append(carta)
    loop -= 1

#loop game
aposta = int(input("Aposta: "))
stts = 0
while True:
    pts_dealer = contagem(dealer)
    pts_jogador = contagem(jogador)
    if pts_dealer == 21 and len(dealer) == 2:
        if pts_dealer != pts_jogador:
            ver_jogo_visivel(dealer,pts_dealer,jogador,pts_jogador)
            print("o dealer ganhou!, ele tem um Blackjack")
        else:
            ver_jogo_visivel(dealer,pts_dealer,jogador,pts_jogador)
            print("empate!,ambos tem um Blackjack")
            stts = 100
        game = False
        break
    ver_jogo_normal(dealer,baralho_As,jogador,pts_jogador)
    jogador, stts , game , baralho= ações_jogador(dealer,pts_jogador,pts_dealer,jogador,baralho)
    if game == False:
        break

#retorno
print(aposta*stts/100)
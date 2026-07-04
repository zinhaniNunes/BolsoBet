#import
import random

#var
saldo = 1000
roleta={
    '0':{
        'numero': 0,
        'cor': 'green',
        'paridade': 'nulo',
        'duzia': 'nulo',
        'linha': 'nulo' },
    '00':{
        'numero': 0,
        'cor': 'green',
        'paridade': 'nulo',
        'duzia': 'nulo',
        'linha': 'nulo' },
    '1':{
        'numero': 1,
        'cor': 'red',
        'paridade': 'impar',
        'duzia': '1',
        'linha': '1'},
    '2':{
        'numero': 2,
        'cor': 'black',
        'paridade': 'par',
        'duzia': '1',
        'linha': '2'},
    '3':{
        'numero': 3,
        'cor': 'red',
        'paridade': 'impar',
        'duzia': '1',
        'linha': '3'},
    '4':{
        'numero': 4,
        'cor': 'black',
        'paridade': 'par',
        'duzia': '1',
        'linha': '1'},
    '5':{
        'numero': 5,
        'cor': 'red',
        'paridade': 'impar',
        'duzia': '1',
        'linha': '2'},
    '6':{
        'numero': 6,
        'cor': 'black',
        'paridade': 'par',
        'duzia': '1',
        'linha': '3'},
    '7':{
        'numero': 7,
        'cor': 'red',
        'paridade': 'impar',
        'duzia': '1',
        'linha': '1'},
    '8':{
        'numero': 8,
        'cor': 'black',
        'paridade': 'par',
        'duzia': '1',
        'linha': '2'},
    '9':{
        'numero': 9,
        'cor': 'red',
        'paridade': 'impar',
        'duzia': '1',
        'linha': '3'},
    '10':{
        'numero': 10,
        'cor': 'black',
        'paridade': 'par',
        'duzia': '1',
        'linha': '1'},
    '11':{
        'numero': 11,
        'cor': 'black',
        'paridade': 'impar',
        'duzia': '1',
        'linha': '2'},
    '12':{
        'numero': 12,
        'cor': 'red',
        'paridade': 'par',
        'duzia': '1',
        'linha': '3'},
    '13':{
        'numero': 13,
        'cor': 'black',
        'paridade': 'impar',
        'duzia': '2',
        'linha': '1'},
    '14':{
        'numero': 14,
        'cor': 'red',
        'paridade': 'par',
        'duzia': '2',
        'linha': '2'},
    '15':{
        'numero': 15,
        'cor': 'black',
        'paridade': 'impar',
        'duzia': '2',
        'linha': '3'},
    '16':{
        'numero': 16,
        'cor': 'red',
        'paridade': 'par',
        'duzia': '2',
        'linha': '1'},
    '17':{
        'numero': 17,
        'cor': 'black',
        'paridade': 'impar',
        'duzia': '2',
        'linha': '2'},
    '18':{
        'numero': 18,
        'cor': 'red',
        'paridade': 'par',
        'duzia': '2',
        'linha': '3'},
    '19':{
        'numero': 19,
        'cor': 'red',
        'paridade': 'impar',
        'duzia': '2',
        'linha': '1'},
    '20':{
        'numero': 20,
        'cor': 'black',
        'paridade': 'par',
        'duzia': '2',
        'linha': '2'},
    '21':{
        'numero': 21,
        'cor': 'red',
        'paridade': 'impar',
        'duzia': '2',
        'linha': '3'},
    '22':{
        'numero': 22,
        'cor': 'black',
        'paridade': 'par',
        'duzia': '2',
        'linha': '1'},
    '23':{
        'numero': 23,
        'cor': 'red',
        'paridade': 'impar',
        'duzia': '2',
        'linha': '2'},
    '24':{
        'numero': 24,
        'cor': 'black',
        'paridade': 'par',
        'duzia': '2',
        'linha': '3'},
    '25':{
        'numero': 25,
        'cor': 'red',
        'paridade': 'impar',
        'duzia': '3',
        'linha': '1'},
    '26':{
        'numero': 26,
        'cor': 'black',
        'paridade': 'par',
        'duzia': '3',
        'linha': '2'},
    '27':{
        'numero': 27,
        'cor': 'red',
        'paridade': 'impar',
        'duzia': '3',
        'linha': '3'},
    '28':{
        'numero': 28,
        'cor': 'black',
        'paridade': 'par',
        'duzia': '3',
        'linha': '1'},
    '29':{
        'numero': 29,
        'cor': 'black',
        'paridade': 'impar',
        'duzia': '3',
        'linha': '2'},
    '30':{
        'numero': 30,
        'cor': 'red',
        'paridade': 'par',
        'duzia': '3',
        'linha': '3'},
    '31':{
        'numero': 31,
        'cor': 'black',
        'paridade': 'impar',
        'duzia': '3',
        'linha': '1'},
    '32':{
        'numero': 32,
        'cor': 'red',
        'paridade': 'par',
        'duzia': '3',
        'linha': '2'},
    '33':{
        'numero': 33,
        'cor': 'black',
        'paridade': 'impar',
        'duzia': '3',
        'linha': '3'},
    '34':{
        'numero': 34,
        'cor': 'red',
        'paridade': 'par',
        'duzia': '3',
        'linha': '1'},
    '35':{
        'numero': 35,
        'cor': 'black',
        'paridade': 'impar',
        'duzia': '3',
        'linha': '2'},
    '36':{
        'numero': 36,
        'cor': 'red',
        'paridade': 'par',
        'duzia': '3',
        'linha': '3'},
    }
tipos = [
    "straight up", "split", "street", "sorner", "six line",
    "red", "black", "par", "impar", "1~18", "19~36",
    "dúzia",'duzia', "linha"
]
tela='''

        \033[41m3\033[0m 6\033[0m \033[41m9\033[0m \033[41m12\033[0m 15\033[0m \033[41m18\033[0m \033[41m21\033[0m 24\033[0m \033[41m27\033[0m \033[41m30\033[0m 33\033[0m \033[41m36\033[0m <- linha 3
     \033[42m00\033[0m
        2\033[0m \033[41m5\033[0m 8\033[0m 11\033[0m \033[41m14\033[0m 17\033[0m 20\033[0m \033[41m23\033[0m 26\033[0m 29\033[0m \033[41m32\033[0m 35\033[0m <- linha 2
      \033[42m0\033[0m
        \033[41m1\033[0m 4\033[0m \033[41m7\033[0m 10\033[0m 13\033[0m \033[41m16\033[0m \033[41m19\033[0m 22\033[0m \033[41m25\033[0m 28\033[0m 31\033[0m \033[41m34\033[0m <- linha 1
       |duzia 1 |  duzia 2  |  duzia 3  |
       |1~18|par| red |black|impar|19~36|
'''

#def
def re(num, casa):
    escolhas = []
    while num > 0:
        escolhas.append(str(casa))
        casa += 1
        num -= 1
    return escolhas

def resultado_bom(sorteado,minhas_escolhas,externo):
    dados = roleta[sorteado]
    if dados['cor'] == 'red' or dados['cor'] == 'green' or dados['cor'] == 'black':
        if dados['cor'] == 'red':
            cor = "\033[31mred\033[0m"
        elif dados['cor'] == 'green':
            cor = "\033[32mred\033[0m"
        else:
            cor = 'black'
    print(f"""
    Número: {sorteado}
    Cor: {cor}
    Paridade: {dados['paridade']}
    Dúzia: {dados['duzia']}
    Linha: {dados['linha']}
    """)
    if sorteado in minhas_escolhas:
        return True
    elif externo != None:
        if externo == 'red':
            return roleta[sorteado]["cor"] == 'red'
        elif externo == 'black':
            return roleta[sorteado]["cor"] == 'black'
        elif externo == 'par':
            return roleta[sorteado]["paridade"] == 'par'
        elif externo == 'impar':
            return roleta[sorteado]["paridade"] == 'impar'
        elif externo == '1~18':
            if roleta[sorteado]["numero"] >= 1 and roleta[sorteado]["numero"] <= 18:
                return True
            else:
                return False
        elif externo == '19~36':
            if roleta[sorteado]["numero"] >= 19 and roleta[sorteado]["numero"] <= 36:
                return True
            else:
                return False
        elif externo == 'duzia':
            if roleta[sorteado]["duzia"] == minhas_escolhas:
                return True
            else:
                return False
        elif externo == 'linha':
            if roleta[sorteado]["linha"] == minhas_escolhas:
                return True
            else:
                return False
    else:
        return False

def premio(resultado,ganho,aposta):
    if resultado == True:
        print(f'parabéns vc ganhou {aposta*ganho}')
        return (aposta*ganho)
    else:
        print('vc perdeu')
        return 0

#jogo
while True:
    minhas_escolhas=[]
    print(tela)
    print(f'saldo:{saldo}')
    while True:
        aposta = int(input("Aposta: "))
        if aposta <= saldo and saldo > 0 and aposta > 0:
            saldo -= aposta
            break
    tipo=input('qual tipo de aposta? (Straight Up/Split/Street/Corner/Six Line)(red/black/par/impar/1~18/19~36/dúzia/linha)\n').lower()
    sorteado = random.choice(list(roleta))
    if tipo == "vermelho" or tipo == "preto":
        if tipo == 'vermelho':
            tipo = 'red'
        else:
            tipo = 'black'
    if tipo in tipos:
        if tipo in 'straight up':
            numero=int(input('numero entre 1 e 36\n'))
            minhas_escolhas.append(f'{numero}') 
            ganho = 36
        elif tipo == 'split':
            fronteira=input('tipo de fronteira: (sup↕/lat↔)\n')
            if fronteira == 'sup':
                numero=int(input('numero de baixo\n'))
                minhas_escolhas=re(2,numero)
                ganho = 18
            if fronteira == 'lat':
                numero=int(input('numero da esquerda\n'))
                minhas_escolhas.append(f'{numero}')
                numero += 3
                minhas_escolhas.append(f'{numero}')
                ganho = 18
        elif tipo == 'street':
            numero=int(input('primeiro numero da sequencia de 3 entre 1 e 34\n'))
            minhas_escolhas=re(3,numero)
            ganho = 12
        elif tipo == 'corner':
            numero=int(input('escolha o numero do canto infrior da esqueda do corner entre 1 e 32\n'))
            minhas_escolhas.append(f'{numero}')
            numero += 1
            minhas_escolhas.append(f'{numero}')
            numero += 2
            minhas_escolhas.append(f'{numero}')
            numero += 1
            minhas_escolhas.append(f'{numero}')
            ganho = 9
        elif tipo == 'six Line':
            numero=int(input('primeiro numero da sequencia de 6 entre 1 e 31\n'))
            minhas_escolhas=re(6,numero)
            ganho = 6
        elif tipo in ['dúzia','duzia']:
            minhas_escolhas = input("Escolha a dúzia: (1/2/3)\n")
            ganho = 3
        elif tipo == 'linha':
            minhas_escolhas = input("Escolha a linha: (1/2/3)\n")
            ganho = 3
        else:
            ganho = 2
    else:
        ganho = 0
    resultado = resultado_bom(sorteado,minhas_escolhas,tipo)
    premiado = premio(resultado,ganho,aposta)
    saldo += premiado
    if saldo == 0:
        print('vc quebrou')
        break
    again = input('jogar novamente (s/n)')
    if again == "n":
        break
print (f'vc tem {saldo} de saldo')
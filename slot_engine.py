"""
Motor genérico de slot machine.

A ideia é que cada jogo (tigrinho, cassino, zeus, egito, pirata, king,
brasil, classic...) tenha só um "config" com:
    - simbolos: lista de símbolos
    - pesos: peso de sorteio de cada símbolo (mesma ordem)
    - premios: dict {simbolo: {3: valor, 4: valor, 5: valor}}
    - simbolo_bonus (opcional): símbolo que dá giros extra
    - area_bonus (opcional): (linhas, colunas) da sub-área onde o
      símbolo bônus é contado (ex.: (3, 3) = canto superior esquerdo)

E chama engine.jogar(aposta, CONFIG) pra rodar um giro completo.
"""

import random


def girar(simbolos, pesos, colunas=5):
    """Sorteia uma linha de `colunas` símbolos."""
    return random.choices(simbolos, weights=pesos, k=colunas)


def sortear_matriz(simbolos, pesos, linhas=5, colunas=5):
    return [girar(simbolos, pesos, colunas) for _ in range(linhas)]


def _avaliar_sequencia(matriz, coords, premios):
    """
    Recebe uma sequência de coordenadas (linha, coluna) em ordem
    (uma linha, uma coluna ou uma diagonal do tabuleiro) e procura a
    maior combinação de símbolos iguais, do tamanho 5 até 3, sempre
    da esquerda pra direita — igual à prioridade que o tigrinho
    original usava nos elif's.
    """
    vals = [matriz[i][j] for i, j in coords]
    n = len(coords)

    for tamanho in range(min(n, 5), 2, -1):
        for inicio in range(0, n - tamanho + 1):
            fim = inicio + tamanho
            sub = vals[inicio:fim]
            if all(s == sub[0] for s in sub):
                tabela = premios.get(sub[0], {})
                if tamanho in tabela:
                    return tabela[tamanho], coords[inicio:fim]
    return 0, []


def _linhas_do_grid(n_linhas, n_colunas):
    return [[(i, j) for j in range(n_colunas)] for i in range(n_linhas)]


def _colunas_do_grid(n_linhas, n_colunas):
    return [[(i, j) for i in range(n_linhas)] for j in range(n_colunas)]


def _diagonais_do_grid(n):
    """Só funciona pra grid quadrado (n x n), que é o caso de todos
    esses jogos (5x5). Gera as diagonais \\ e / com 3+ células."""
    diagonais = []

    # diagonais "\" (offset = coluna - linha)
    for offset in range(-(n - 3), n - 2):
        diag = [(i, i + offset) for i in range(n) if 0 <= i + offset < n]
        if len(diag) >= 3:
            diagonais.append(diag)

    # diagonais "/" (soma = linha + coluna)
    for soma in range(2, 2 * n - 3):
        diag = [(i, soma - i) for i in range(n) if 0 <= soma - i < n]
        if len(diag) >= 3:
            diagonais.append(diag)

    return diagonais


def calcular_ganho(matriz, premios):
    n_linhas = len(matriz)
    n_colunas = len(matriz[0])

    sequencias = _linhas_do_grid(n_linhas, n_colunas) + _colunas_do_grid(n_linhas, n_colunas)
    if n_linhas == n_colunas:
        sequencias += _diagonais_do_grid(n_linhas)

    ganho_total = 0
    posicoes = set()

    for seq in sequencias:
        ganho, posicoes_seq = _avaliar_sequencia(matriz, seq, premios)
        if ganho:
            ganho_total += ganho
            posicoes.update(posicoes_seq)

    return ganho_total, [[i, j] for i, j in posicoes]


def contar_bonus(matriz, simbolo_bonus, area_bonus=None):
    if not simbolo_bonus:
        return 0

    limite_linha = area_bonus[0] if area_bonus else len(matriz)
    limite_coluna = area_bonus[1] if area_bonus else len(matriz[0])

    count = 0
    for i, linha in enumerate(matriz):
        if i >= limite_linha:
            break
        for j, simbolo in enumerate(linha):
            if j >= limite_coluna:
                break
            if simbolo == simbolo_bonus:
                count += 1

    return count


def jogar(aposta, config):
    """Roda um giro completo pra qualquer jogo, a partir do config."""

    linhas = config.get("linhas", 5)
    colunas = config.get("colunas", 5)

    matriz = sortear_matriz(config["simbolos"], config["pesos"], linhas, colunas)
    ganho, posicoes = calcular_ganho(matriz, config["premios"])
    spin_bonus = contar_bonus(matriz, config.get("simbolo_bonus"), config.get("area_bonus"))

    return {
        "matriz": matriz,
        "ganho": ganho * aposta,
        "spin_bonus": spin_bonus,
        "multiplicador": ganho,
        "posicoes": posicoes,
    }

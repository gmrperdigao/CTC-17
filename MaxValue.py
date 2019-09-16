from random import random
from random import uniform
from math import exp
from math import ceil
from collections import Counter
from time import time

# constante de boltzman
boltzman = 1.3806488e-23


# Funcao para pegar um vizinho aleatorio (nas proximidades entre min e max)
def move(old_posic, min, max):
    nova_posic = list(old_posic)
    for i in range(len(nova_posic)):
        nova_posic[i] = nova_posic[i] + uniform(min, max)
    return nova_posic


# Funcao para calcular a posicao com o maximo valor encontrado
def tempera_simulada(function, inic_posic, max_iteracoes, move_min, move_max, t0, a):
    posic = inic_posic
    temperatura = t0
    i = 0
    while i <= max_iteracoes:
        trocas = 0
        testes = 0
        while True:
            posic_nova = move(posic, move_min, move_max)
            delta = function(*posic) - function(*posic_nova)
            testes += 1
            if delta <= 0.0 or (exp(-delta/temperatura) > random()):
                posic = posic_nova
                trocas += 1
            if testes > max_iteracoes or trocas >= max_iteracoes:
                break
        temperatura *= a
        if trocas == 0 or temperatura == 0:
            break
    return posic


def funcao(x, y):
    return 4*exp(-x**2 -y**2) + exp(-((x-5)**2+(y-5)**2)) + exp(-((x+5)**2+(y-5)**2)) + exp(-((x-5)**2+(y+5)**2)) + exp(-((x+5)**2+(y+5)**2))


if __name__ == "__main__":
    solucoes = Counter()
    saidas = Counter()
    init = time()
    for i in range(100):
        saida = tempera_simulada(funcao, [uniform(-10, 10), uniform(-10, 10)], 100, -0.5, 0.5, 1000, boltzman)
        solucoes[ceil(funcao(saida[0], saida[1]))] += 1
        saida[0] = round(saida[0])
        saida[1] = round(saida[1])
        saidas[tuple(saida)] += 1
    print("Tempo de execucao: ", (time() - init))
    print("Frequencia de respostas: ")
    for keys in solucoes:
        print("    Valor", keys, "com frequencia", solucoes[keys])
    print("Frequencia de saidas: ")
    for keys in saidas:
        print("    Valor", keys, "com frequencia", saidas[keys])


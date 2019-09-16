from random import choice
from collections import Counter
from random import randrange
from time import time
from queue import PriorityQueue


class Nrainhas:
    # O tabuleiro e representado por um vetor de dimensao N, no qual uma rainha está na coluna estado[i] e linha i
    def __init__(self, N):
        self.N = N
        self.solucao = []

    # Cria um estado inicial aleatorio
    def cria_tab(self):
        inicial = []
        for i in range(self.N):
            inicial.append(randrange(self.N))
        return inicial

    # Heuristica usada: numero de ataques entre rainhas
    def heuristica(self, state):
        # Define os contadores, neles sao guardados as colunas e diagonais de cada rainha.
        ## Caso o contador de alguma linha ou diagonal seja maior que 1, há mais de uma rainha nesse local
        coluna = Counter()
        diagonal1 = Counter()
        diagonal2 = Counter()
        # Conta quantas rainhas ha em cada coluna e cada diagonal
        for lin, col in enumerate(state):
            coluna[col] += 1
            diagonal1[lin - col] += 1
            diagonal2[lin + col] += 1
        heu = 0
        # Procura colisoes
        for contador in [coluna, diagonal1, diagonal2]:
            for posic in contador:
                if contador[posic] > 1:
                    heu += (contador[posic] - 1)
        return heu

    # Retorna os filhos possiveis por movimentando as rainhas pelas colunas
    def filhos(self, state):
        filhos = PriorityQueue()
        for linha in range(self.N):
            for col in range(self.N):
                if col != state[linha]:
                    aux = list(state)
                    aux[linha] = col
                    filhos.put((self.heuristica(aux), aux))
        return filhos

    def hill_climbing(self):
        t0 = time()
        solucao = []
        tabuleiro = self.cria_tab()
        while int(self.heuristica(tabuleiro)) != 0:
            filhos = self.filhos(tabuleiro)
            if not filhos:
                break
            filho = filhos.get()[1]
            if self.heuristica(filho) >= self.heuristica(tabuleiro):
                break
            tabuleiro = filho
        if int(self.heuristica(tabuleiro)) == 0:
            solucao.append(tabuleiro)
        print("Tempo de execucao: ", (time() - t0))
        self.solucao = solucao

    def imprime(self):
        # Se o algoritmo nao encontrar solucao, ou seja, "subiu o pico errado"
        if not self.solucao:
            print("Solucao nao encontrada pelo Hill Climbing")
        else:
            resultado = self.solucao[0]
            tabuleiro = []
            for col in resultado:
                linha = ['-'] * len(resultado)
                linha[col] = 'R'
                tabuleiro.append(linha)
            for i in range(self.N):
                print(" ".join(tabuleiro[i]))


if __name__ == "__main__":
    # Parametro de Nrainhas e N
    rainhas = Nrainhas(10)
    rainhas.hill_climbing()
    print("Solucao:")
    rainhas.imprime()

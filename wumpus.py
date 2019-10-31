from operator import itemgetter


class Solver:
    def __init__(self, mdp):
        self.mdp = mdp

    def solve(self):
        V = self.calculo()
        solucao = max(V, key=lambda s: V[s][0])
        solucao = {solucao: V[solucao][1]}
        V = {s: V[s][1] for s in V.keys()}
        return V

    def calculo(self, epsilon=0.0001):
        v = {s: (0, '') for s in self.mdp.estados()}
        g = self.mdp.gamma()
        while True:
            d = 0
            v_new = v.copy()
            for s in self.mdp.estados():
                for a in self.mdp.acoes():
                    soma = 0
                    for j in self.mdp.estados():
                        soma += self.mdp.probabilidade(s, a, j) * v_new[j][0]
                    utilidade = self.mdp.recompensa(s) + g*soma
                    if utilidade > v[s][0]:
                        v[s] = (utilidade, a)
                d = max(d, abs(v[s][0] - v_new[s][0]))
            if d < epsilon * (1 - g) / g:
                return v_new


class Tabuleiro:
    # Todas as localizacoes sao identificadas por um par (x,y)
    def __init__(self, bordas, pit, wumpus, ouro, inicio):
        self.acoes = ["norte", "sul", "leste", "oeste"]
        self.celulas = []
        self.bordas = bordas
        self.pocos = pit
        self.wumpus = wumpus
        self.ouros = ouro
        self.posicao_inicial = inicio

    def acao(self):
        return self.acoes

    def estados(self):
        x = max(self.bordas, key=itemgetter(0))
        y = max(self.bordas, key=itemgetter(1))
        tupla = ()
        celulas = []
        for i in range(x[0] + 1):
            for j in range(y[1] + 1):
                tupla = (i, j)
                if tupla not in self.bordas:
                    celulas.append(tupla)
        return celulas

    def recompensa(self, estado):
        if estado in self.wumpus:
            return -100
        elif estado in self.pocos:
            return -50
        elif estado in self.ouros:
            return 100
        elif estado in self.bordas:
            return -1
        else:
            return -0.1

    def probabilidade(self, s, a, j):
        x, y = s
        if a == 'norte':
            esquerda = (x, y - 1)
            direita = (x, y + 1)
            quero = (x + 1, y)
        elif a == 'sul':
            esquerda = (x, y + 1)
            direita = (x, y - 1)
            quero = (x - 1, y)
        elif a == 'oeste':
            esquerda = (x -1, y)
            direita = (x + 1, y)
            quero = (x, y - 1)
        else:
            esquerda = (x + 1, y)
            direita = (x - 1, y)
            quero = (x, y + 1)

        if j in self.bordas:
            return 0

        if j == quero:
            return 0.7
        elif j == esquerda:
            return 0.2
        elif j == direita:
            return 0.1
        else:
            return 0

    def estado_inicial(self):
        return self.posicao_inicial

    def gamma(self):
        return 0.9


if __name__ == "__main__":
    mdp = Tabuleiro([(1, 1), (2, 1), (3, 1), (4, 1), (1, 8), (2, 8), (3, 8), (4, 8),
                 (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7)],
                [(1, 3), (1, 7), (3, 3), (3, 7), (4, 2), (4, 7)], [(3, 1), (2, 5)], [(3, 2), (2, 6)], (1, 1))
    s = Solver(mdp)
    policy = s.solve()
    print("politica", policy)

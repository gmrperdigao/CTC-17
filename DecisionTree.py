import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
eps = np.finfo(float).eps
from numpy import log2 as log
import random
from collections import Counter

# Classe para trabalhar com a base de dados:
class Database:
    def __init__(self):
        # Pegar tabelas, adicionar header e remover colunas desnecessarias
        self.movies = pd.read_csv("movies.dat", sep="::", header=None, engine='python')
        self.movies.columns = ["MovieID", "Title", "Genres"]
        self.ratings = pd.read_csv("ratings.dat", sep="::", header=None, engine='python')
        self.ratings.columns = ["UserID", "MovieID", "Rating", "Timestamp"]
        self.ratings = self.ratings.drop(columns='Timestamp')
        self.users = pd.read_csv("users.dat", sep="::", header=None, engine='python')
        self.users.columns = ["UserID", "Gender", "Age", "Occupation", "Zip-code"]
        self.users = self.users.drop(columns='Zip-code')
        # Juntar tabelas
        self.tabela = pd.merge(self.ratings, self.users, on='UserID')
        self.tabela = pd.merge(self.tabela, self.movies, on='MovieID')
        self.tabela = self.tabela.drop(columns=['MovieID', 'UserID'])


class ArvoreDecisao:
    def __init__(self, data):
        self.data = data
        self.objetivo = 'Rating'

    def entropia_saida(self, data):
        entropia = 0
        # Pega os possiveis valores de saida
        saidas = data[self.objetivo].unique()
        for resultado in saidas:
            aux = data[self.objetivo].value_counts()[resultado]/len(data[self.objetivo])
            entropia += -aux*np.log2(aux)
        return entropia

    def entropia_atributo(self, data, atrib):
        # Pega os pssiveis valores de saida
        resultados = data[self.objetivo].unique()
        # Pega os valores da coluna
        entradas = data[atrib].unique()
        entropia_aux = 0
        for variable in entradas:
            entropia = 0
            for resultado in resultados:
                qtd = len(data[atrib][data[atrib] == variable][data[self.objetivo] == resultado])
                total = len(data[atrib][data[atrib] == variable])
                aux = qtd/(total + eps)
                entropia += -aux*log(aux + eps)
            aux2 = total/len(data)
            entropia_aux += -aux2*entropia
        return abs(entropia_aux)

    def escolhe_atrib(self, data, atributos):
        ganho_informacao = []
        atributos.remove('Rating')
        for key in atributos:
            ganho_informacao.append(self.entropia_saida(data) - self.entropia_atributo(data, key))
        return atributos[np.argmax(ganho_informacao)]

    def particiona(self, data, node, valor):
        return data[data[node] == valor].reset_index(drop=True)

    def cria_arvore(self, data, atributos, padrao):
        _, contadores = np.unique(data['Rating'], return_counts=True)
        if data.empty:
            return padrao
        elif len(contadores) == 1:
            return data['Rating'].mode().iloc[0]
        elif len(atributos) == 0:
            return data['Rating'].mode().iloc[0]
        else:
            # Escolhe atributo com maior ganho de informacao
            melhor = self.escolhe_atrib(data, atributos)
            # Pega possiveis valores do atributo escolhido
            atrib_valores = np.unique(data[melhor])
            arvore = {}
            arvore[melhor] = {}
            for valor in atrib_valores:
                particao = self.particiona(data, melhor, valor)
                values, counts = np.unique(particao['Rating'], return_counts=True)
                # Se todos os exemplos tem a mesma classificacao
                if len(counts) == 1:
                    arvore[melhor][valor] = values[0]
                else:
                    atribs = list(data)
                    atribs.remove(melhor)
                    if len(particao.index) >= len(data.index)/1000 and len(particao.index) >= 300:
                        arvore[melhor][valor] = self.cria_arvore(particao, atribs, data['Rating'].mode().iloc[0])
                    else:
                        arvore[melhor][valor] = particao['Rating'].mode().iloc[0]
            return arvore


def calcula_rating(inst, arvore):
    for chaves in arvore.keys():
        chave2 = inst[chaves]
        if chave2 in arvore[chaves].keys():
            arvore = arvore[chaves][chave2]
            if type(arvore) is dict:
                previsto = calcula_rating(inst, arvore)
            else:
                previsto = arvore
                break
        else:
            previsto = random.choice([1, 2, 3, 4, 5])
    return previsto


def recomendados(gender, age, occupation, title, genres, arvore):
    previsto = {}
    for i in range(len(title)):
        dict = {'Gender': gender, 'Age': age, 'Occupation': occupation, 'Title': title[i], 'Genres': genres[i]}
        inst = pd.Series(dict)
        previsto[title[i]] = calcula_rating(inst, arvore)
    return pd.DataFrame(list(previsto.items()), columns=['Title', 'Rating'])


if __name__ == "__main__":
    db = Database()
    data, teste = train_test_split(db.tabela, test_size=0.4)
    # Criar arvore
    padrao = data['Rating'].mode().iloc[0]
    atribs = list(data)
    tree = ArvoreDecisao(data)
    arvore = tree.cria_arvore(tree.data, atribs, padrao)
    # Salvar arvore
    file = open("arvore.txt", "w")
    file.write(str(tree))
    file.close()
    # Testar saida
    teste = teste.reset_index(drop=True)
    corretos = 0
    Count1 = Counter()
    Count2 = Counter()
    Count3 = Counter()
    Count4 = Counter()
    Count5 = Counter()
    for i in range(len(teste)):
        line = teste.iloc[i, :].to_dict()
        rating = line.pop('Rating')
        inst = pd.Series(line)
        pred = calcula_rating(inst, arvore)
        if rating == pred:
            corretos += 1
        if rating == 5:
            Count5[pred] += 1
        elif rating == 4:
            Count4[pred] += 1
        elif rating == 3:
            Count3[pred] += 1
        elif rating == 2:
            Count2[pred] += 1
        else:
            Count1[pred] += 1
    print("Predicoes corretas:", corretos, "de", i+1, "testes")
    print("Counter 1:", Count1)
    print("Counter 2:", Count2)
    print("Counter 3:", Count3)
    print("Counter 4:", Count4)
    print("Counter 5:", Count5)
    # Calcular filmes recomendados:
    title = db.movies['Title'].tolist()
    genres = db.movies['Genres'].tolist()
    resultados = recomendados('M', 18, 4, title, genres, arvore)
    recomend = resultados.sort_values(by=['Rating'], ascending=False)
    print("**** Filmes Recomendados ****")
    print(recomend[0:3])
    # Calcular meus recomendados
    print("----------------------------------------------------------")
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Toy Story (1995)", 'Genres': 'Drama'} #5
    inst = pd.Series(df)
    print(df['Title'], calcula_rating(inst, arvore))
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Ace Ventura: When Nature Calls (1995)", 'Genres': 'Drama'} #2
    inst = pd.Series(df)
    print(df['Title'], calcula_rating(inst, arvore))
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Pocahontas (1995)", 'Genres': 'Drama'} #4
    inst = pd.Series(df)
    print(df['Title'], calcula_rating(inst, arvore))
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Jungle Book, The (1967)", 'Genres': 'Drama'} #4
    inst = pd.Series(df)
    print(df['Title'], calcula_rating(inst, arvore))
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Addams Family, The (1991)", 'Genres': 'Drama'} #4
    inst = pd.Series(df)
    print(df['Title'], calcula_rating(inst, arvore))
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Blade (1998)", 'Genres': 'Drama'} #3
    inst = pd.Series(df)
    print(df['Title'], calcula_rating(inst, arvore))
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Pink Flamingos (1972)", 'Genres': 'Drama'} #3
    inst = pd.Series(df)
    print(df['Title'], calcula_rating(inst, arvore))
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Babe: Pig in the City (1998)", 'Genres': 'Drama'} #2
    inst = pd.Series(df)
    print(df['Title'], calcula_rating(inst, arvore))
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Rambo: First Blood Part II (1985)", 'Genres': 'Drama'} #3
    inst = pd.Series(df)
    print(df['Title'], calcula_rating(inst, arvore))
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Jumanji (1995)", 'Genres': 'Drama'} #5
    inst = pd.Series(df)
    print(df['Title'], calcula_rating(inst, arvore))




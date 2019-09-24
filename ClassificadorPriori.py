import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
eps = np.finfo(float).eps
from numpy import log2 as log
import random
import pprint
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


if __name__ == "__main__":
    db = Database()
    data, teste = train_test_split(db.tabela, test_size=0.4)
    # Testar saida
    teste = teste.reset_index(drop=True)
    corretos = 0
    Count1 = Counter()
    Count2 = Counter()
    Count3 = Counter()
    Count4 = Counter()
    Count5 = Counter()
    for i in range(len(teste)):
        # Criar arvore
        new_df = data.loc[data['Title'] == teste.iloc[i, 4]]
        pred = new_df['Rating'].mode().iloc[0]
        rating = teste.iloc[i, 0]
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
    # Calcular meus recomendados
    print("----------------------------------------------------------")
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Toy Story (1995)", 'Genres': 'Drama'} #5
    new_df = data.loc[data['Title'] == df['Title']]
    pred = new_df['Rating'].mode().iloc[0]
    print(df['Title'], pred)
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Ace Ventura: When Nature Calls (1995)", 'Genres': 'Drama'} #2
    new_df = data.loc[data['Title'] == df['Title']]
    pred = new_df['Rating'].mode().iloc[0]
    print(df['Title'], pred)
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Pocahontas (1995)", 'Genres': 'Drama'} #4
    new_df = data.loc[data['Title'] == df['Title']]
    pred = new_df['Rating'].mode().iloc[0]
    print(df['Title'], pred)
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Jungle Book, The (1967)", 'Genres': 'Drama'} #4
    new_df = data.loc[data['Title'] == df['Title']]
    pred = new_df['Rating'].mode().iloc[0]
    print(df['Title'], pred)
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Addams Family, The (1991)", 'Genres': 'Drama'} #4
    new_df = data.loc[data['Title'] == df['Title']]
    pred = new_df['Rating'].mode().iloc[0]
    print(df['Title'], pred)
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Blade (1998)", 'Genres': 'Drama'} #3
    new_df = data.loc[data['Title'] == df['Title']]
    pred = new_df['Rating'].mode().iloc[0]
    print(df['Title'], pred)
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Pink Flamingos (1972)", 'Genres': 'Drama'} #3
    new_df = data.loc[data['Title'] == df['Title']]
    pred = new_df['Rating'].mode().iloc[0]
    print(df['Title'], pred)
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Babe: Pig in the City (1998)", 'Genres': 'Drama'} #2
    new_df = data.loc[data['Title'] == df['Title']]
    pred = new_df['Rating'].mode().iloc[0]
    print(df['Title'], pred)
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Rambo: First Blood Part II (1985)", 'Genres': 'Drama'} #3
    new_df = data.loc[data['Title'] == df['Title']]
    pred = new_df['Rating'].mode().iloc[0]
    print(df['Title'], pred)
    df = {'Gender': 'M', 'Age': 18, 'Occupation': 4, 'Title': "Jumanji (1995)", 'Genres': 'Drama'} #5
    new_df = data.loc[data['Title'] == df['Title']]
    pred = new_df['Rating'].mode().iloc[0]
    print(df['Title'], pred)




import random as rd
import pandas
from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import train_test_split  
from sklearn import metrics
class ga:
    dados = pandas.read_csv("diabetes.csv")
    def __init__(self, tax, num, ger):
        self.tax = tax
        self.num = num
        self.ger = ger
 
    def individado(self):
        prof = rd.randint(3, 150)
        met = rd.randint(0, 2)
        min = rd.uniform(0.001, 0.9)
        exemplo = [prof, met, min]
        return exemplo
    
    def geracao(self):
        self.lista = []
        i = 0
        while(i != self.num):
            self.lista.append(self.individado())
            i+=1

    def substituicao(self, lista):
        self.lista = lista        
    
    def selecao(self):
        a = rd.randint(0, (self.num - 1))
        self.ind1 = self.lista[a]  
        self.lista.pop(a)
        b = rd.randint(0, (self.num - 2))
        self.ind2 = self.lista[b]
        if(a == (self.num - 1)):
            self.lista.append(self.ind1)
        else:
            self.lista.insert(a, self.ind1)
        return self.lista              

    def comparar(self, n1, n2):   
        if(n1 > n2):
            return self.ind1
        else:
            return self.ind2

    def gerarXY(self):
        self.X = self.dados.iloc[:, :-1].values #pega todas as colunas menos o target
        self.y = self.dados.iloc[:, -1].values  #pega apenas a coluna do target
        self.X_treino, self.X_teste, self.y_treino, self.y_teste = train_test_split(self.X, self.y, test_size=0.3, random_state=1)

    def fitness(self):
        p = self.ind1
        tradutor = {0:"gini", 1:"entropy", 2:"log_loss"}
        arvore = DecisionTreeClassifier(max_depth=p[0], criterion=tradutor[p[1]], min_samples_split=p[2])
        arvore.fit(self.X_treino, self.y_treino)
        previsao = arvore.predict(self.X_teste)
        self.acuracia1 = metrics.accuracy_score(self.y_teste, previsao) 
        p = self.ind2
        tradutor = {0:"gini", 1:"entropy", 2:"log_loss"}
        arvore = DecisionTreeClassifier(max_depth=p[0], criterion=tradutor[p[1]], min_samples_split=p[2])
        arvore.fit(self.X_treino, self.y_treino)
        previsao = arvore.predict(self.X_teste)
        self.acuracia2 = metrics.accuracy_score(self.y_teste, previsao)
        maior = self.comparar(self.acuracia1, self.acuracia2)
        return maior

    def crossing(self, melhores):
        c = rd.randint(7, 8)
        first = melhores[0]
        second = melhores[1]
        if(c==8):
            aux11 = first[1]
            aux12 = first[2]
            first[1] = second[1]
            first[2] = second[2]
            second[1] = aux11
            second[2] = aux12
        else:
            aux1 = first[2]
            first[2] = second[2]
            second[2] = aux1
        melhores[0] = first
        melhores[1] = second    
        return melhores
    
    def melhorDaGeracao(self):
        for item in self.lista:
            maior = 0
            tradutor = {0:"gini", 1:"entropy", 2:"log_loss"}
            arvore = DecisionTreeClassifier(max_depth=item[0], criterion=tradutor[item[1]], min_samples_split=item[2])
            arvore.fit(self.X_treino, self.y_treino)
            previsao = arvore.predict(self.X_teste)
            acuracia = metrics.accuracy_score(self.y_teste, previsao)
            if(acuracia > maior):
                maior = acuracia
            return maior    

metodo = ga(2, 6, 3)
metodo.gerarXY()
metodo.geracao()
melhores = []
melhoresAcuracias = []
filhos = []
i=0
j=0
while(j != metodo.ger):

    while(i != (metodo.num/2)):
        print(metodo.lista)
        melhoresAcuracias.append(metodo.melhorDaGeracao())   
        metodo.selecao()
        melhores.append(metodo.fitness())
        metodo.selecao()
        melhores.append(metodo.fitness())
        x = metodo.crossing(melhores)
        filhos.append(x[0])
        filhos.append(x[1])
        i+=1          
metodo.substituicao(filhos)

i = 0
j+=1
print(melhoresAcuracias)        

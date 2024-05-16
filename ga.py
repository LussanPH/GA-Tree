import random as rd
import pandas
from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import train_test_split  
from sklearn import metrics
import copy
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
        return exemplo[:]
    
    def geracao(self):
        self.lista = []
        i = 0
        while(i != self.num):
            self.lista.append(self.individado())
            i+=1     
    
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
        return maior[:]

    def crossing(self, melhores, int):
        c = rd.randint(7, 8)
        first = melhores[0 + int]
        second = melhores[1 + int]
        genes1 = []
        genes2 = []
        genes1.append(first[1])
        genes1.append(first[2])
        genes2.append(second[1])
        genes2.append(second[2])
        if(c == 8):
            first.pop(1)
            first.pop(1)
            first.append(genes2[0])
            first.append(genes2[1])
            second.pop(1)
            second.pop(1)
            second.append(genes1[0])
            second.append(genes1[1])
        else:
            first.pop(2) 
            first.append(genes2[1])
            second.pop(2)
            second.append(genes1[1])
        melhores[0 + int] = first
        melhores[1 + int] = second
        self.mutacao(first)
        self.mutacao(second) 
    
    def mutacao(self, ind):
        z = 0
        while(z != len(ind)):
            mutacao = rd.randint(1, 100)
            if(mutacao <= self.tax):
                exe = self.individado()
                if(z == 0):
                    ind[0] = exe[0]
                if(z == 1):
                    ind[1] = exe[1]
                if(z == 2):
                    ind[2] = exe[2]
            z+=1            
                            
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

metodo = ga(20, 100, 20)
melhores = []
selecionados = []
i=0
j=0
k=0
f=0

metodo.gerarXY()
metodo.geracao()
melhores.append(metodo.melhorDaGeracao())
while(f != metodo.num):
    print(metodo.lista[f],metodo.lista[f+1],metodo.lista[f+2],metodo.lista[f+3],metodo.lista[f+4])
    f+=5
f=0
print("---------------------------------------------")
print("---------------------------------------------")
while(j != metodo.ger):
    while(i != metodo.num/2):    
        metodo.selecao()
        selecionados.append(metodo.fitness())
        metodo.selecao()
        selecionados.append(metodo.fitness())
        metodo.crossing(selecionados, k)
        k+=2
        i+=1
    metodo.lista = selecionados[:]
    while(f != metodo.num):
       print(selecionados[f],selecionados[f+1],selecionados[f+2],selecionados[f+3],selecionados[f+4])
       f+=5
    f=0
    print("---------------------------------------------")
    print("---------------------------------------------")   
    selecionados.clear()
    melhores.append(metodo.melhorDaGeracao())
    k=0
    i=0
    j+=1
print("------------LISTA----------------")
print(melhores)        

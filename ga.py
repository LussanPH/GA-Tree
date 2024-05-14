import random as rd
class ga:
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
        lista = []
        i = 0
        while(i != self.num):
            lista.append(self.individado())
            i+=1
        return lista
    def selecao(self, lista):
        a = rd.randint(0, (self.num - 1))
        ind1 = lista[a]
        lista.pop(a)
        b = rd.randint(0, (self.num - 2))
        ind2 = lista[b]
        if(a == (self.num - 1)):
            lista.append(ind1)
        else:
            lista.insert(a, ind1)    
        pessoa = [ind1, ind2]
        return pessoa    
metodo = ga(2, 6, 3)
individuos = metodo.geracao()
selecionados = metodo.selecao(individuos)
print(selecionados)
print(individuos)                   

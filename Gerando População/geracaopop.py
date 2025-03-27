import numpy as np  


def newpop(Nind, Ncrom, CromLim):
    # Inicializando a população
    newpop = np.zeros((Nind, Ncrom))
   
    # Gerando a população aleatória
    for i in range(Nind):
        for j in range(Ncrom):
            inf = CromLim[j, 0]  # Limite inferior do cromossomo
            sup = CromLim[j, 1]  # Limite superior do cromossomo
            newpop[i, j] = np.random.uniform(inf, sup)  # Geração do valor aleatório dentro do intervalo
    return newpop




Nind = 10  # Número de indivíduos na população
Ncrom = 5  # Número de cromossomos por indivíduo
CromLim = np.array([[0, 10], [5, 15], [1, 7], [3, 8], [0, 5]])  # Limites para os cromossomos


populacao_inicial = newpop(Nind, Ncrom, CromLim)
print(populacao_inicial)
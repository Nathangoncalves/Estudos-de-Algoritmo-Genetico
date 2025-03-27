import random

def single_point_crossover(binpop, selected):
    """
    Realiza cruzamento em ponto único.
    :param binpop: População binária (lista de strings binárias)
    :param selected: Índices dos indivíduos selecionados para cruzamento
    :return: Nova população após cruzamento
    """
    Nind = len(selected)  # Número de indivíduos selecionados
    Lind = len(binpop[0])  # Comprimento do cromossomo
    new_population = []
    
    for i in range(0, Nind, 2):  # Processa em pares
        if i + 1 >= Nind:
            break  # Garante número par de indivíduos
        
        parent1 = binpop[selected[i]]
        parent2 = binpop[selected[i+1]]
        cp = random.randint(1, Lind - 1)  # Ponto de corte
        
        child1 = parent1[:cp] + parent2[cp:]
        child2 = parent2[:cp] + parent1[cp:]
        
        new_population.extend([child1, child2])
    
    return new_population


def mutation(binpop, pmut):
    """
    Realiza mutação com probabilidade pmut.
    :param binpop: População binária (lista de strings binárias)
    :param pmut: Probabilidade de mutação
    :return: População após mutação
    """
    Nind = len(binpop)
    Lind = len(binpop[0])
    
    for i in range(Nind):
        if random.random() < pmut:
            mp = random.randint(0, Lind - 1)  # Ponto de mutação
            individual = list(binpop[i])  # Transforma em lista para modificar
            individual[mp] = '1' if individual[mp] == '0' else '0'  # Invertemos o bit
            binpop[i] = ''.join(individual)  # Converte de volta para string
    
    return binpop

# Exemplo de uso:
population = ["11010", "10101", "01100", "10011"]
selected = [0, 1, 2, 3]  # Todos selecionados para cruzamento
new_population = single_point_crossover(population, selected)
print("População após cruzamento:", new_population)

mutated_population = mutation(new_population, 0.1)  # Probabilidade de mutação de 10%
print("População após mutação:", mutated_population)
import numpy as np

# -----------------------------------------------------------------------------
# Inicialização da população (codificação por valores)
def newpop(Nind, Ncrom, CromLim):
    """
    Gera uma população de indivíduos com valores reais.
    :param Nind: Número de indivíduos na população.
    :param Ncrom: Número de cromossomos por indivíduo.
    :param CromLim: Matriz (Nx2) com os limites inferior e superior de cada cromossomo.
    :return: Matriz com a população inicial.
    """
    pop = np.zeros((Nind, Ncrom))
    for i in range(Nind):
        for j in range(Ncrom):
            inf = CromLim[j, 0]
            sup = CromLim[j, 1]
            pop[i, j] = np.random.uniform(inf, sup)
    return pop

# -----------------------------------------------------------------------------
# Função de Erradicação da Epidemia
# Aqui definimos uma função que representa o tempo de erradicação.
# O objetivo é minimizar esse tempo. No exemplo, usamos uma função dummy
# baseada na distância em relação a um vetor ótimo (valores ideais).
optimal = np.array([5, 10, 4, 5.5, 2.5])  # Valores ótimos hipotéticos para cada parâmetro

def epidemic_eradication_time(x):
    """
    Calcula o tempo de erradicação da epidemia para um conjunto de parâmetros.
    Quanto menor o tempo, melhor.
    :param x: Vetor de parâmetros do indivíduo.
    :return: Tempo de erradicação (valor a ser minimizado).
    """
    # Exemplo: soma dos quadrados das diferenças em relação ao vetor ótimo
    return np.sum((x - optimal)**2)

# -----------------------------------------------------------------------------
# Função Fitness
def fitness(pop):
    """
    Calcula os valores de fitness para cada indivíduo da população.
    Como queremos minimizar o tempo de erradicação, o fitness é definido como 1/(tempo + epsilon).
    :param pop: População de indivíduos (matriz de valores reais).
    :return: Vetor de fitness.
    """
    epsilon = 1e-6  # Evita divisão por zero
    Nind = len(pop)
    fitness_values = np.zeros(Nind)
    for i in range(Nind):
        t = epidemic_eradication_time(pop[i])
        fitness_values[i] = 1.0 / (t + epsilon)
    return fitness_values

# -----------------------------------------------------------------------------
# Operador de Seleção por Torneio
def tournament_selection(pop, fitness_values, tournament_size):
    """
    Realiza a seleção dos indivíduos usando o operador de torneio.
    Em cada torneio, sorteia-se 'tournament_size' indivíduos e seleciona-se o com melhor fitness.
    :param pop: População atual.
    :param fitness_values: Vetor de fitness dos indivíduos.
    :param tournament_size: Número de indivíduos participantes de cada torneio.
    :return: Lista de índices dos indivíduos selecionados.
    """
    N = len(pop)
    selected_indices = []
    for _ in range(N):
        competitors = np.random.choice(N, tournament_size, replace=False)
        best_index = competitors[0]
        for idx in competitors:
            if fitness_values[idx] > fitness_values[best_index]:
                best_index = idx
        selected_indices.append(best_index)
    return selected_indices

# -----------------------------------------------------------------------------
# Operador de Cruzamento Aritmético
def arithmetic_crossover(pop, selected_indices):
    """
    Realiza o cruzamento aritmético entre indivíduos selecionados.
    Em cada par, gera dois filhos por combinação linear dos pais.
    :param pop: População atual.
    :param selected_indices: Lista de índices dos indivíduos selecionados para cruzamento.
    :return: Nova população (filhos) gerada pelo cruzamento.
    """
    new_population = []
    N = len(selected_indices)
    for i in range(0, N, 2):
        if i + 1 < N:
            parent1 = pop[selected_indices[i]]
            parent2 = pop[selected_indices[i+1]]
            alpha = np.random.rand()
            child1 = alpha * parent1 + (1 - alpha) * parent2
            child2 = alpha * parent2 + (1 - alpha) * parent1
            new_population.extend([child1, child2])
        else:
            new_population.append(pop[selected_indices[i]])
    return np.array(new_population)

# -----------------------------------------------------------------------------
# Operador de Mutação para Codificação por Valores
def real_mutation(pop, mutation_rate, CromLim):
    """
    Realiza mutação em cada gene com probabilidade 'mutation_rate',
    atribuindo um novo valor aleatório dentro dos limites definidos.
    :param pop: População atual (matriz de valores reais).
    :param mutation_rate: Probabilidade de mutação para cada gene.
    :param CromLim: Matriz com os limites de cada cromossomo.
    :return: Nova população após mutação.
    """
    new_pop = pop.copy()
    Nind, Ncrom = pop.shape
    for i in range(Nind):
        for j in range(Ncrom):
            if np.random.rand() < mutation_rate:
                inf = CromLim[j, 0]
                sup = CromLim[j, 1]
                new_pop[i, j] = np.random.uniform(inf, sup)
    return new_pop

# -----------------------------------------------------------------------------
# Parâmetros do AG
Nind = 10            # Número de indivíduos
Ncrom = 5            # Número de cromossomos por indivíduo
CromLim = np.array([
    [0, 10],
    [5, 15],
    [1, 7],
    [3, 8],
    [0, 5]
])                   # Limites para cada parâmetro
tournament_size = 3  # Tamanho do torneio
mutation_rate = 0.1  # Probabilidade de mutação
num_generations = 50 # Número de gerações

# -----------------------------------------------------------------------------
# Inicialização da população
pop = newpop(Nind, Ncrom, CromLim)

# Loop do AG
for generation in range(num_generations):
    fit_values = fitness(pop)
    best_index = np.argmax(fit_values)
    best_fitness = fit_values[best_index]
    best_individual = pop[best_index]
    print(f"Geração {generation}: Melhor Fitness = {best_fitness:.6f}, Melhor Indivíduo = {best_individual}")
    
    # Seleção por torneio
    selected_indices = tournament_selection(pop, fit_values, tournament_size)
    
    # Cruzamento aritmético
    offspring = arithmetic_crossover(pop, selected_indices)

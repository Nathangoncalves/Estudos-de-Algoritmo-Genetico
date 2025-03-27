import numpy as np
import random

# Parâmetros do ambiente e do AG
m = 40  # Ordem da matriz (grid), ou seja, o grid possui m x m células
grid_size = m * m

# Para simulação, definimos um grid que representa a presença de indivíduos suscetíveis.
# Por exemplo, vamos assumir que 70% das células contêm indivíduos suscetíveis (valor 1).
susceptible_ratio = 0.7
grid = np.random.choice([0, 1], size=(m, m), p=[1 - susceptible_ratio, susceptible_ratio])

# Número de genes (agentes de controle). Segundo o artigo, g = a, onde a ≈ 0.04 × n.
# Exemplo: se n = 300, g ≈ 12.
g = 12

# Parâmetros do AG
pop_size = 150        # Tamanho da população
num_generations = 50  # Número de gerações
tournament_size = 3   # Tamanho do torneio para seleção
crossover_rate = 0.6  # Taxa de crossover (60%)
mutation_rate = 0.01  # Taxa de mutação (1%)

# -----------------------------------------------------------------------------
# Geração da população inicial (codificação inteira)
def newpop_int(pop_size, g, grid_size):
    """
    Gera uma população onde cada indivíduo é um vetor de g genes inteiros,
    representando posições únicas na matriz (amostradas sem reposição).
    """
    population = []
    for _ in range(pop_size):
        individual = random.sample(range(grid_size), g)
        population.append(individual)
    return population

# -----------------------------------------------------------------------------
# Função de Fitness: Avaliação segundo a equação (5.6)
def fitness_individual(individual, grid, m):
    """
    Calcula a adequabilidade (fitness) de um indivíduo.
    Para cada gene, soma-se o número de indivíduos suscetíveis na vizinhança (8 vizinhos).
    """
    total_fitness = 0
    # Offsets para os 8 vizinhos (vizinhança de raio unitário)
    offsets = [(-1, -1), (-1, 0), (-1, 1),
               (0, -1),           (0, 1),
               (1, -1),  (1, 0),  (1, 1)]
    
    for gene in individual:
        row = gene // m
        col = gene % m
        neighbor_sum = 0
        for dr, dc in offsets:
            r = row + dr
            c = col + dc
            if 0 <= r < m and 0 <= c < m:
                neighbor_sum += grid[r, c]
        total_fitness += neighbor_sum
    return total_fitness

def fitness_population(population, grid, m):
    """
    Calcula os valores de fitness para todos os indivíduos da população.
    """
    fitness_values = []
    for individual in population:
        fitness_values.append(fitness_individual(individual, grid, m))
    return fitness_values

# -----------------------------------------------------------------------------
# Seleção por Torneio
def tournament_selection(population, fitness_values, tournament_size):
    """
    Seleciona indivíduos utilizando torneio: para cada seleção, sorteia-se
    'tournament_size' indivíduos e escolhe-se o de maior fitness.
    """
    selected = []
    pop_size = len(population)
    for _ in range(pop_size):
        competitors = random.sample(range(pop_size), tournament_size)
        best = competitors[0]
        for idx in competitors:
            if fitness_values[idx] > fitness_values[best]:
                best = idx
        selected.append(population[best])
    return selected

# -----------------------------------------------------------------------------
# Operador de Cruzamento: One-Point Crossover
def one_point_crossover(parent1, parent2):
    """
    Realiza o crossover de um ponto entre dois pais.
    """
    gene_length = len(parent1)
    cp = random.randint(1, gene_length - 1)
    child1 = parent1[:cp] + parent2[cp:]
    child2 = parent2[:cp] + parent1[cp:]
    return child1, child2

def crossover_population(population, crossover_rate):
    """
    Aplica o operador de crossover à população selecionada.
    """
    new_population = []
    pop_size = len(population)
    indices = list(range(pop_size))
    random.shuffle(indices)
    for i in range(0, pop_size - 1, 2):
        parent1 = population[indices[i]]
        parent2 = population[indices[i+1]]
        if random.random() < crossover_rate:
            child1, child2 = one_point_crossover(parent1, parent2)
            new_population.extend([child1, child2])
        else:
            new_population.extend([parent1, parent2])
    # Se o número de indivíduos for ímpar, adiciona o último sem cruzamento
    if pop_size % 2 == 1:
        new_population.append(population[indices[-1]])
    return new_population

# -----------------------------------------------------------------------------
# Operador de Mutação: Alteração aleatória de um gene
def mutation_population(population, mutation_rate, grid_size):
    """
    Para cada gene de cada indivíduo, com probabilidade 'mutation_rate' o gene é
    substituído por um novo valor inteiro aleatório dentro do domínio [0, grid_size-1].
    """
    new_population = []
    for individual in population:
        new_individual = individual.copy()
        for i in range(len(new_individual)):
            if random.random() < mutation_rate:
                new_individual[i] = random.randint(0, grid_size - 1)
        new_population.append(new_individual)
    return new_population

# -----------------------------------------------------------------------------
# Loop principal do AG
population = newpop_int(pop_size, g, grid_size)

for generation in range(num_generations):
    fit_values = fitness_population(population, grid, m)
    best_index = np.argmax(fit_values)
    best_fitness = fit_values[best_index]
    print(f"Geração {generation}: Melhor Fitness = {best_fitness}, Melhor Indivíduo = {population[best_index]}")
    
    # Seleção por torneio
    selected_population = tournament_selection(population, fit_values, tournament_size)
    
    # Cruzamento (one-point)
    offspring = crossover_population(selected_population, crossover_rate)
    
    # Mutação
    population = mutation_population(offspring, mutation_rate, grid_size)

# Resultado final
fit_values = fitness_population(population, grid, m)
best_index = np.argmax(fit_values)
best_fitness = fit_values[best_index]
print("\nResultado final:")
print(f"Melhor Fitness = {best_fitness}, Melhor Indivíduo = {population[best_index]}")

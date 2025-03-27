import numpy as np

# Função Objetiva: 10 - x^2
def obj_function(x):
    Ncrom = len(x)
    obj_function_value = 10
    for j in range(Ncrom):
        obj_function_value -= x[j] ** 2
    return obj_function_value

# Função de Avaliação: Calcula o fitness de cada indivíduo na população
def fitness(pop):
    Nind = len(pop)  # Número de indivíduos
    Ncrom = len(pop[0])  # Número de cromossomos em cada indivíduo
    fitness_values = np.zeros(Nind)

    for i in range(Nind):
        fitness_values[i] = obj_function(pop[i])
    
    return fitness_values

# Método da Roleta para seleção de indivíduos
def roleta(fitness_values):
    # Normaliza os valores de fitness para probabilidades
    total_fitness = sum(fitness_values)
    probabilities = fitness_values / total_fitness
    
    # Geração de um número aleatório para simular a roleta
    random_value = np.random.rand()
    cumulative_probability = 0.0
    
    # Seleciona um indivíduo com base na roleta
    for i in range(len(fitness_values)):
        cumulative_probability += probabilities[i]
        if random_value <= cumulative_probability:
            return i  # Retorna o índice do indivíduo selecionado
    
    return len(fitness_values) - 1  # Caso de segurança

# Exemplo de uso
def main():
    # Definindo a população de indivíduos (cromossomos)
    pop = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])  # População de exemplo
    Ncrom = len(pop[0])  # Número de cromossomos em cada indivíduo
    
    # Calculando o fitness dos indivíduos na população
    fitness_values = fitness(pop)
    print("Fitness dos indivíduos:", fitness_values)

    # Selecionando um indivíduo usando o método da roleta
    selected_index = roleta(fitness_values)
    print("Índice do indivíduo selecionado pela roleta:", selected_index)
    print("Indivíduo selecionado:", pop[selected_index])

if __name__ == "__main__":
    main()
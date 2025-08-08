import random
import networkx as nx

# Classe de Algoritmo Genético para rotulação L(3,2,1)
class Genetic_Algorithm_L321:

  # Construtor
  def __init__(self, graph, population_rate, generations, crossover_rate, mutation_rate, elitism_rate):
    self.graph = graph # Grafo
    self.population_rate = population_rate # Número entre 0 e 1 que será multiplicado pelo número de vértices do grafo
    self.population_size = int(len(self.graph) * population_rate) # tamanho da população
    self.generations = generations # Número de gerações
    self.crossover_rate = crossover_rate # Taxa de cruzamento - One Point Crossover (POP)
    self.mutation_rate = mutation_rate # Taxa de mutação 
    self.elitism_rate = elitism_rate # Taxa de elitismo
    self.population = [] # Lista da população atual
    self.new_population = [] # Lista da nova população
    self.fitness_scores = [] # Lista dos valores de fitness
    self.best_solution = None # Melhor solução encontrada
    self.best_fitness = None # Melhor valor de fitness encontrado
    self.best_labeling = None # Melhor rotulação
    self.labelings = [] # lista com as rotulações
    self.dict1 = self._neighbors_at_distance_1() # Dicionário dos vizinhos distância 1
    self.dict2 = self._neighbors_at_distance_2() # Dicionário dos vizinhos distância 2
    self.dict3 = self._neighbors_at_distance_3() # Dicionário dos vizinhos distância 3
    # self.solution_history = []


  # Função run.
  # Inicializa a população.
  # Calcula o fitness da população.
  # Executa a atualização.
  # Retorna o melhor fitness.
  def run(self):
    count = 0
    count_repeat = 0
    max_count_repeat = 100
    
    self.inicialize_population()
    self.calculate_fitness()
    
    self.best_fitness = min(self.fitness_scores)
    best_fitness_previous = self.best_fitness
    # self.solution_history.append((0, self.best_fitness))  # Registro da 1ª geração
    
    while count < self.generations:
      self.update_population()
      chromosomes_fitness = list(zip(self.labelings, self.fitness_scores))
      melhor_par = min(chromosomes_fitness, key=lambda x: x[1])

      self.best_fitness = melhor_par[1]
      self.best_labeling = melhor_par[0] 
      
      if self.best_fitness >= best_fitness_previous:
        count_repeat += 1
      else:
        count_repeat = 0 
        best_fitness_previous = self.best_fitness 
        # self.solution_history.append((count + 1, self.best_fitness))  # Registro da melhoria

        # print(f"Geração {count + 1}: Novo melhor fitness = {self.best_fitness}")

      if count_repeat >= max_count_repeat:

        break

      count += 1
      
    return self.best_fitness, self.best_labeling


  # retorna um dicionário contendo os vizinhos na distância 1
  # para cada vértice
  def _neighbors_at_distance_1(self):
    dict1 = dict()
    for v in self.graph:
        dict1[v] = []
        for u in self.graph[v]:
            dict1[v].append(u)
    return dict1


  # retorna um dicionário contendo os vizinhos na distância 2
  # para cada vértice. Essa função requer que a função 
  # neighbors_at_distance_1(self) tenha sido executada antes dela
  def _neighbors_at_distance_2(self):
    dict2 = dict()
    for v in self.graph:
        dict2[v] = []
        for u in self.graph[v]:
            for w in self.graph[u]:
                if w != v and w not in self.dict1[v]:
                    dict2[v].append(w)
    return dict2


  # retorna um dicionário contendo os vizinhos na distância 3
  # para cada vértice. Essa função requer que as funções 
  # neighbors_at_distance_1(self) e neighbors_at_distance_2(self) 
  # tenham sido executadas antes dela
  def _neighbors_at_distance_3(self):
    dict3 = dict()
    for v in self.graph:
        dict3[v] = []
        for u in self.graph[v]:
            for w in self.graph[u]:
                for z in self.graph[w]:
                    if z != u and z != v and z not in self.dict2[v] and z not in self.dict1[v]:
                        dict3[v].append(z)
    return dict3


  # Função para inicializar a população de cromossomos.
  # Cada cromossomo é uma permutação dos vértices do grafo.
  # Pré-condições: self.graph e self.population_rate
  # Pós-condições: retorna uma lista com a população gerada.
  def inicialize_population(self):

    for i in range(0, self.population_size):
      chromosome = [x for x in range(0, len(self.graph))]
      random.shuffle(chromosome)
      self.population.append(chromosome)

    return self.population


  # Função para calcular o fitness de cada cromossomo da população.
  # Recebe a população.
  # Calcula a função fitness de cada cromossomo.
  # Retorna uma lista com os valores de fitness.
  # Atribui o menor fitness na lista best_fitness.
  def calculate_fitness(self):

    def condition_satisfied(neighbors_dict, vertex, color_list, value, newcolor):    
      for w in neighbors_dict[vertex]:
        if color_list[w] != -1 and abs(newcolor - color_list[w]) < value:
            return False
      return True

    def greedy_coloring_L321(vertex_permutation, neighbors1, neighbors2, neighbors3):
      color_list = [-1] * len(vertex_permutation)
      max_color = 0
      for v in vertex_permutation:
        color = 0
        while True:
            if condition_satisfied(neighbors1, v, color_list, 3, color) and condition_satisfied(neighbors2, v, color_list, 2, color) and condition_satisfied(neighbors3, v, color_list, 1, color):
               color_list[v] = color
               break
            else:
                color += 1
        max_color = max(max_color, color)
      return max_color, color_list

    self.fitness_scores = []
    self.labelings = []
    for chromosome in self.population:
      span, labeling = greedy_coloring_L321(chromosome, self.dict1, self.dict2, self.dict3)
      self.fitness_scores.append(span)
      self.labelings.append(labeling)


  # Função de elitismo por fitness.
  # Calcula a quantidade da elite.
  # Ordena os cromossomos pelo valor de fitness.
  # Adiciona a elite na nova população.
  def elitism(self):
    num_elite = int(len(self.population) * self.elitism_rate)
    chromosomes_fitness = list(zip(self.population, self.fitness_scores))
    chromosomes_fitness.sort(key=lambda x: x[1])

    for i in range(num_elite):
      self.new_population.append(chromosomes_fitness[i][0])


  # Função de seleção por torneio.
  # Compara dois cromossomos e salva o que tiver menor fitness.
  # Executa 2 vezes e retorna dois competidores.
  def selection(self):

      tournament = []

      for i in range(2):

        competitor_1 = random.choice(list(zip(self.population, self.fitness_scores)))
        competitor_2 = random.choice(list(zip(self.population, self.fitness_scores)))

        if competitor_1[1] < competitor_2[1]:
          tournament.append(competitor_1[0])
        else:
          tournament.append(competitor_2[0])

      return tournament[0], tournament[1]


  # Função de crossover POP.
  # Seleciona dois pais, define um ponto de corte para cada.
  # Gera dois novos filhos.
  def crossover(self, chromosome1, chromosome2):

    offspring = []

    # Primeiro filho
    cut_point = random.randint(0, len(chromosome1) - 2)
    permutation_list = chromosome1[:cut_point + 1]
    sublist = chromosome1[cut_point + 1:]
    for v in chromosome2:
        if v in sublist:
            permutation_list.append(v)
    offspring1 = permutation_list
    offspring.append(offspring1)

    # Segundo filho
    cut_point = random.randint(0, len(chromosome2) - 2)
    permutation_list = chromosome2[:cut_point + 1]
    sublist = chromosome2[cut_point + 1:]
    for v in chromosome1:
        if v in sublist:
            permutation_list.append(v)
    offspring2 = permutation_list
    offspring.append(offspring2)

    return offspring[0], offspring[1]
  

  # seleciona um vértice v aleatoriamente e 
  # embaralha os seus vizinhos
  def neighbors_swap_mutation(self, chromosome):
    v = random.randint(0, len(chromosome)-1)
    # Obter vizinhos e permutar
    neighbors = list(self.graph.neighbors(v))
    random.shuffle(neighbors)
    for i in range(0,len(neighbors)-1,2):
      idx_u = chromosome.index(neighbors[i])
      idx_w = chromosome.index(neighbors[i+1])
      chromosome[idx_u], chromosome[idx_w] = chromosome[idx_w], chromosome[idx_u]


  # Função de atualização da população.
  # Executa todos operadores do GA.
  # Gera uma nova população.
  def update_population(self):
    self.new_population = []
    self.elitism()

    while len(self.new_population) < self.population_size:
      parent1, parent2 = self.selection()

      if random.random() < self.crossover_rate:
        child1, child2 = self.crossover(parent1, parent2)
      else:
        child1, child2 = parent1, parent2
      if random.random() < self.mutation_rate:
         self.neighbors_swap_mutation(child1)
      if random.random() < self.mutation_rate:
         self.neighbors_swap_mutation(child2)
      self.new_population.append(child1)
      if len(self.new_population) < self.population_size:
        self.new_population.append(child2)

    self.population = self.new_population
    self.new_population = [] # limpa essa população que não será mais necessária
    self.calculate_fitness()
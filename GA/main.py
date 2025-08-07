import networkx as nx
import os
import argparse
import time
from ga_L321 import Genetic_Algorithm_L321

# Essa função recebe o caminho de um arquivo que 
# contém o grafo como uma lista de adjacências e 
# remove laços e arestas múltiplas do grafo, já que
# esse tipo de aresta é irrelevante para o problema
# de rotulação-L(3,2,1)
def ler_grafo(caminho_arquivo):
    G = nx.Graph()

    with open(caminho_arquivo, 'r') as f:
        for linha in f:
            if not linha.strip():
                continue  # ignora linhas em branco
            u, v = map(int, linha.strip().split())

            if u == v:
                continue  # ignora laços
            if G.has_edge(u, v):
                continue  # ignora arestas múltiplas

            G.add_edge(u, v)

    return G


# # essa função supõe que os vértices estão normalizados, 
# # que são consecutivos no intervalo de 0 a n-1.
# def labeling_is_valid(graph, color_list):
#     # retorna um dicionário contendo os vizinhos na distância 1
#     # para cada vértice
#     def _neighbors_at_distance_1(graph):
#         dict1 = dict()
#         for v in graph:
#             dict1[v] = []
#             for u in graph[v]:
#                 dict1[v].append(u)
#         return dict1

#     # retorna um dicionário contendo os vizinhos na distância 2
#     # para cada vértice. Essa função requer que a função 
#     # neighbors_at_distance_1(self) tenha sido executada antes dela
#     def _neighbors_at_distance_2(graph, dict1):
#         dict2 = dict()
#         for v in graph:
#             dict2[v] = []
#             for u in graph[v]:
#                 for w in graph[u]:
#                     if w != v and w not in dict1[v]:
#                         dict2[v].append(w)
#         return dict2

#     # retorna um dicionário contendo os vizinhos na distância 3
#     # para cada vértice. Essa função requer que as funções 
#     # neighbors_at_distance_1(self) e neighbors_at_distance_2(self) 
#     # tenham sido executadas antes dela
#     def _neighbors_at_distance_3(graph, dict1, dict2):
#         dict3 = dict()
#         for v in graph:
#             dict3[v] = []
#             for u in graph[v]:
#                 for w in graph[u]:
#                     for z in graph[w]:
#                         if z != u and z != v and z not in dict2[v] and z not in dict1[v]:
#                             dict3[v].append(z)
#         return dict3
    
#     dict1 = _neighbors_at_distance_1(graph)
#     dict2 = _neighbors_at_distance_2(graph, dict1)
#     dict3 = _neighbors_at_distance_3(graph, dict1, dict2)

#     for v in range(0, len(graph)):
#         for u in dict1[v]:
#             if abs(color_list[u] - color_list[v]) < 3:
#                 return False
#         for u in dict2[v]:
#             if abs(color_list[u] - color_list[v]) < 2:
#                 return False
#         for u in dict3[v]:
#             if abs(color_list[u] - color_list[v]) < 1:
#                 return False
    
#     return True

# Função para executar o algoritmo genético e salvar os resultados em um arquivo.
def run_experiment(graph_name, graph, population_rate, generations, crossover_rate, mutation_rate, elitism_rate, out_filename, trial):

    ga_l321 = Genetic_Algorithm_L321(graph=graph,
                                     population_rate=population_rate,
                                     generations=generations,
                                     crossover_rate=crossover_rate,
                                     mutation_rate=mutation_rate,
                                     elitism_rate=elitism_rate)

    start_time = time.time()
    best_fitness, best_labeling = ga_l321.run()
    end_time = time.time()
    execution_time = end_time - start_time

    graus = [d for _, d in graph.degree()]
    Delta = max(graus)
    delta = min(graus)
    upper_bound = Delta**3 + 2*Delta
    
    regular = all(g == graus[0] for g in graus)
    if regular:
        lower_bound = 2*Delta + 2
    else:
        lower_bound = 2*Delta + 1

    # is_valid = labeling_is_valid(graph, best_labeling)

    #print(f"best labeling = {best_labeling}")

    print(f"{trial},{graph_name},{len(graph)},{len(graph.edges())},{nx.density(graph):.5f},{best_fitness},{execution_time:.5f},{Delta},{delta},{lower_bound},{upper_bound}")


def main():
    parser = argparse.ArgumentParser(description="Lê um grafo de um arquivo e remove laços e arestas múltiplas.")
    parser.add_argument("arquivo", help="Caminho para o arquivo .txt contendo o grafo")

    args = parser.parse_args()
    graph = ler_grafo(args.arquivo)

    input_filename = os.path.basename(args.arquivo)
    nome_sem_extensao = os.path.splitext(input_filename)[0] 

    population_rate = 0.25 # equivalente a (1/4)
    generations = 150
    crossover_rate = 0.8
    mutation_rate = 0.2
    elitism_rate = 0.1
    trials = 30
    out_filename = "result_" + nome_sem_extensao + ".csv"

    print("trial,filename,order,size,density,fitness,time(seconds),Max_degree,Min_Degree,LB,UB")

    for t in range(1, trials+1):
        run_experiment(nome_sem_extensao, graph, population_rate, generations, crossover_rate, mutation_rate, elitism_rate, out_filename, t)

if __name__ == "__main__":
    main()



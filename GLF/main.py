import networkx as nx
import os
import argparse
import time
from glf_l321 import Greedy_Largest_First_L321

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

# Função para executar o algoritmo guloso random e salvar os resultados em um arquivo.
def run_experiment(graph_name, graph, out_filename):
    iterations = 150
    greedy_random_l321 = Greedy_Largest_First_L321(graph=graph)
    best_fitness, time_of_best_fitness, best_labeling = greedy_random_l321.run(iterations)

    # # Verifica validade da rotulação
    # is_valid = labeling_is_valid(graph, best_labeling)

    print(f"{graph_name},{best_fitness},{time_of_best_fitness:.5f}")

def main():
    parser = argparse.ArgumentParser(description="Lê um grafo de um arquivo e remove laços e arestas múltiplas.")
    parser.add_argument("arquivo", help="Caminho para o arquivo .txt contendo o grafo")

    args = parser.parse_args()
    graph = ler_grafo(args.arquivo)

    input_filename = os.path.basename(args.arquivo)
    nome_sem_extensao = os.path.splitext(input_filename)[0] 

    out_filename = "result_" + nome_sem_extensao + ".csv"

    print("Filename,Fitness,Time(seconds)")

    run_experiment(nome_sem_extensao, graph, out_filename)

if __name__ == "__main__":
    main()



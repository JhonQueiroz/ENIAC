import networkx as nx
import random
import sys
import time

# Algoritmo guloso para rotulação L(3,2,1) com suporte a vértices com rótulos arbitrários.

class Greedy_Random_L321:

    # Inicializa a classe com o grafo e precomputação de vizinhos a distâncias 1, 2 e 3.
    def __init__(self, graph):
        self.G = graph
        self.nodes = sorted(graph.nodes())
        self.node_to_index = {node: i for i, node in enumerate(self.nodes)}
        self.index_to_node = {i: node for i, node in enumerate(self.nodes)}
        self.dict1 = self.neighbors_at_distance_1()
        self.dict2 = self.neighbors_at_distance_2()
        self.dict3 = self.neighbors_at_distance_3()
    
    # Executa o algoritmo n vezes com permutações aleatórias.
    # Retorna: melhor valor de span encontrado e tempo de execução da melhor solução.
    def run(self, iterations):
        minimum_color_so_far = sys.maxsize
        time_of_best_solution = sys.maxsize
        best_coloring = None

        for _ in range(iterations):
            permutation = self.nodes.copy()
            random.shuffle(permutation)

            start_time = time.time()
            span, color_list = self.greedy_coloring_L321(permutation, self.dict1, self.dict2, self.dict3)
            end_time = time.time()
            execution_time = end_time - start_time

            if span < minimum_color_so_far:
                minimum_color_so_far = span
                time_of_best_solution = execution_time
                best_coloring = color_list.copy()  # <- guarda a melhor solução

        return minimum_color_so_far, time_of_best_solution, best_coloring
    
    # Verifica se o vértice pode receber a cor newcolor respeitando as restrições L(3,2,1).
    def condition_satisfied(self, neighbors_dict, vertex, color_list, value, newcolor):
        for w in neighbors_dict.get(vertex, []):
            index_w = self.node_to_index[w]
            if color_list[index_w] != -1 and abs(newcolor - color_list[index_w]) < value:
                return False
        return True

    # Retorna dicionário com vizinhos a distância 1.
    def greedy_coloring_L321(self, vertex_permutation, neighbors1, neighbors2, neighbors3):
        color_list = [-1] * len(self.nodes)

        for v in vertex_permutation:
            color = 0
            index_v = self.node_to_index[v]
            while True:
                if self.condition_satisfied(neighbors1, v, color_list, 3, color) and \
                   self.condition_satisfied(neighbors2, v, color_list, 2, color) and \
                   self.condition_satisfied(neighbors3, v, color_list, 1, color):
                    color_list[index_v] = color
                    break
                color += 1

        return max(color_list) + 1, color_list

    def neighbors_at_distance_1(self):
        return {v: list(self.G.neighbors(v)) for v in self.G.nodes()}

    # Retorna dicionário com vizinhos a distância 2 (exclui vizinhos a distância 1).
    def neighbors_at_distance_2(self):
        dist2 = {v: set() for v in self.G.nodes()}
        for v in self.G.nodes():
            for u in self.G.neighbors(v):
                dist2[v].update(self.G.neighbors(u))
            dist2[v].discard(v)
            dist2[v].difference_update(self.G.neighbors(v))
        return {v: list(dist2[v]) for v in self.G.nodes()}

    # Retorna dicionário com vizinhos a distância 3 (exclui vizinhos a distância 1 e 2).
    def neighbors_at_distance_3(self):
        dist3 = {v: set() for v in self.G.nodes()}
        for v in self.G.nodes():
            visited = set([v])
            frontier = set(self.G.neighbors(v))
            visited.update(frontier)
            second = set()
            for u in frontier:
                second.update(self.G.neighbors(u))
            visited.update(second)
            third = set()
            for u in second:
                third.update(self.G.neighbors(u))
            third.difference_update(visited)
            dist3[v] = third
        return {v: list(dist3[v]) for v in self.G.nodes()}

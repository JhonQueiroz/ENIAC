import os
from pathlib import Path

def ler_dimacs(path_arquivo):
    arestas = []
    n_vertices = 0
    with open(path_arquivo, 'r') as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith('c'):
                continue
            elif linha.startswith('p'):
                partes = linha.split()
                n_vertices = int(partes[2])
            elif linha.startswith('e'):
                _, u, v = linha.split()
                # Converte para base 0
                arestas.append((int(u)-1, int(v)-1))
    return n_vertices, arestas

def salvar_txt(nome, arestas, pasta_saida):
    Path(pasta_saida).mkdir(parents=True, exist_ok=True)
    caminho_saida = os.path.join(pasta_saida, nome + '.txt')
    with open(caminho_saida, 'w') as f:
        for u, v in arestas:
            f.write(f"{u} {v}\n")

def normalizar_dimacs(pasta_entrada, pasta_saida):
    for raiz, _, arquivos in os.walk(pasta_entrada):
        for arquivo in arquivos:
            if arquivo.endswith('.col'):
                caminho = os.path.join(raiz, arquivo)
                nome = Path(arquivo).stem
                n, arestas = ler_dimacs(caminho)
                salvar_txt(nome, arestas, os.path.join(pasta_saida, "DIMACS"))
                print(f"[✔] {nome} convertido para .txt")

if __name__ == "__main__":
    normalizar_dimacs("benchmark/DIMACS", "benchmark_normalizado")
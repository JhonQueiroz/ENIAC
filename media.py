import pandas as pd
import os

# Caminho da pasta onde estão os arquivos
pasta_resultados = "Resultados/GA_resultados/DIMACS"  # ajuste se necessário
arquivos = [f for f in os.listdir(pasta_resultados) if f.endswith(".csv")]

resumos = []

for nome_arquivo in arquivos:
    caminho = os.path.join(pasta_resultados, nome_arquivo)
    df = pd.read_csv(caminho)

    # Dados principais
    melhor_idx = df["fitness"].idxmin()
    melhor_fitness = df.loc[melhor_idx, "fitness"]
    tempo_melhor = df.loc[melhor_idx, "time(seconds)"]
    media_fitness = df["fitness"].mean()
    desvio_fitness = df["fitness"].std()

    # Formatar média e DP como no artigo
    media_dp_formatado = f"{media_fitness:.2f} (±{desvio_fitness:.2f})"

    grafo = df.loc[0, "filename"]

    resumos.append({
        "Grafo": grafo,
        "Melhor_Fitness": melhor_fitness,
        "Tempo_Melhor_Fitness": tempo_melhor,
        "GA_AVG (±DP)": media_dp_formatado
    })

# Gerar CSV consolidado
df_resumo = pd.DataFrame(resumos)
df_resumo.to_csv("consolidado_resultados_GA.csv", index=False)
print("✅ Arquivo 'consolidado_resultados_GA.csv' gerado com sucesso.")
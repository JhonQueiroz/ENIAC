#!/bin/bash

# Caminhos
PROGRAMA_PY="GA/main.py"
ENTRADA_DIR="Benchmark"
SAIDA_DIR="Resultados/GA_resultados"

# Detectar sistema operacional
SO=$(uname)
if [[ "$SO" == "Darwin" ]]; then
    # macOS
    get_file_size() {
        stat -f%z "$1"
    }
else
    # Linux (assumindo GNU coreutils)
    get_file_size() {
        stat -c%s "$1"
    }
fi

# Cria diretório de saída se não existir
mkdir -p "$SAIDA_DIR"

# Percorre cada subpasta dentro de benchmark
for subdir in "$ENTRADA_DIR"/*/; do
    nome_subdir=$(basename "$subdir")
    mkdir -p "$SAIDA_DIR/$nome_subdir"

    echo "Processando arquivos em: $subdir"

    # Monta lista com tamanho e caminho do arquivo
    arquivos_ordenados=$(find "$subdir" -type f -name "*.txt" | while read -r arquivo; do
        tamanho=$(get_file_size "$arquivo")
        echo "$tamanho $arquivo"
    done | sort -n | cut -d' ' -f2-)

    # Processa arquivos ordenados
    while read -r arquivo_txt; do
        nome_arquivo=$(basename "$arquivo_txt" .txt)
        saida_csv="$SAIDA_DIR/$nome_subdir/$nome_arquivo.csv"

        echo "Executando $arquivo_txt → $saida_csv"

        # Executa o programa Python com o arquivo como entrada e salva no CSV
        python3 "$PROGRAMA_PY" "$arquivo_txt" > "$saida_csv"
    done <<< "$arquivos_ordenados"
done



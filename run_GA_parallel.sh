#!/opt/homebrew/bin/bash

# Número máximo de execuções paralelas (default: 2)
MAX_JOBS=${1:-7}

# Caminhos
PROGRAMA_PY="GA/main.py"
ENTRADA_DIR="Benchmark"
SAIDA_DIR="Resultados"

# Detectar sistema operacional
SO=$(uname)
if [[ "$SO" == "Darwin" ]]; then
    # macOS
    get_file_size() {
        stat -f%z "$1"
    }
else
    # Linux
    get_file_size() {
        stat -c%s "$1"
    }
fi

# Cria diretório de saída se não existir
mkdir -p "$SAIDA_DIR"

# Contador de jobs
job_count=0

# Função para executar uma instância
executar_instancia() {
    local arquivo_txt="$1"
    local subdir_relativo="$2"
    local nome_arquivo
    nome_arquivo=$(basename "$arquivo_txt" .txt)
    local saida_csv="$SAIDA_DIR/$subdir_relativo/$nome_arquivo.csv"

    echo "Executando $arquivo_txt → $saida_csv"
    python3 "$PROGRAMA_PY" "$arquivo_txt" > "$saida_csv"
}

# Percorre cada subpasta
for subdir in "$ENTRADA_DIR"/*/; do
    nome_subdir=$(basename "$subdir")
    mkdir -p "$SAIDA_DIR/$nome_subdir"

    echo "Processando arquivos em: $subdir"

    arquivos_ordenados=$(find "$subdir" -type f -name "*.txt" | while read -r arquivo; do
        tamanho=$(get_file_size "$arquivo")
        echo "$tamanho $arquivo"
    done | sort -n | cut -d' ' -f2-)

    while read -r arquivo_txt; do
        # Executa em segundo plano
        executar_instancia "$arquivo_txt" "$nome_subdir" &

        ((job_count++))
        # Se atingir o limite de jobs, espera terminar
        if [[ "$job_count" -ge "$MAX_JOBS" ]]; then
            wait -n
            ((job_count--))
        fi
    done <<< "$arquivos_ordenados"
done

# Espera o restante
wait

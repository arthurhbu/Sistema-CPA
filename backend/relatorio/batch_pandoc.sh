# !/bin/bash

#Comando no terminal: sudo bash batch_pandoc.sh EAD2021_AvaliaçãoDistância(nome da pasta do instrumento)

# Diretório que contém os arquivos .md (pode ser alterado conforme necessário)
if [ -z "$1" ]; then 
  echo "Por favor, forneça o nome do diretório específico"
  exit 1
fi

nomeInstrumento="$1"
directory="./markdowns/$1/"

# Lista todos os arquivos .md no diretório e armazena seus nomes no array 'files'
files=()
while IFS= read -r -d $'\0' file; do
    files+=("$file")
done < <(find "$directory" -maxdepth 1 -name '*.md' -print0)

# Nome do contêiner Podman a ser usado
container="docker.io/pandoc/extra:3.1.1"

# Template a ser usado
template="eisvogel"

# Loop através dos arquivos fornecidos na linha de comando
for file in "${files[@]}"; do
  # Verifica se o arquivo existe
  if [ -f "$file" ]; then
    # Extrai o nome do arquivo sem a extensão para usar no nome do arquivo PDF de saída
    filename=$(basename "$file" .md)
    echo "$filename"
    # Executa o comando Podman com os argumentos fornecidos
    # sudo docker run --rm --volume "$(pwd):/data" pandoc/extra "$file" -o "./pdf/${filename}.pdf" --template "$template" --listingsls -l relatorio/markdowns/EAD2021/FigurasGraficos_EAD2021/

    sudo podman run --rm --volume "$(pwd):/data:z" "$container" "$file" -o "./pdfs/${nomeInstrumento}/${filename}.pdf" --template "$template" --listings

  else
    echo "Arquivo '$file' não encontrado."
  fi
done

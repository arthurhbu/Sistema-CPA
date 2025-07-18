#!/bin/bash

echo "🧪 TESTE DO NOVO REQUIREMENTS.TXT"
echo "=================================="

# Nome do container de teste
TEST_CONTAINER_NAME="cpa-backend-test"
TEST_IMAGE_NAME="cpa-backend-test"

echo "📦 Construindo imagem de teste..."
docker build -t $TEST_IMAGE_NAME ./backend

if [ $? -eq 0 ]; then
    echo "✅ Imagem construída com sucesso!"
    
    echo "🚀 Iniciando container de teste..."
    docker run --rm -d \
        --name $TEST_CONTAINER_NAME \
        -p 5001:5000 \
        $TEST_IMAGE_NAME
    
    if [ $? -eq 0 ]; then
        echo "✅ Container de teste iniciado na porta 5001"
        echo "🌐 Teste acessando: http://localhost:5001"
        
        echo "⏳ Aguardando 10 segundos para o container inicializar..."
        sleep 10
        
        echo "🔍 Verificando logs do container..."
        docker logs $TEST_CONTAINER_NAME
        
        echo "🧹 Limpando container de teste..."
        docker stop $TEST_CONTAINER_NAME
        docker rmi $TEST_IMAGE_NAME
        
        echo "✅ Teste concluído! Container atual não foi afetado."
    else
        echo "❌ Erro ao iniciar container de teste"
        docker rmi $TEST_IMAGE_NAME
        exit 1
    fi
else
    echo "❌ Erro ao construir imagem de teste"
    exit 1
fi 
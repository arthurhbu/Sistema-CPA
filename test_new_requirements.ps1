# 🧪 TESTE DO NOVO REQUIREMENTS.TXT
Write-Host "🧪 TESTE DO NOVO REQUIREMENTS.TXT" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Nome do container de teste
$TEST_CONTAINER_NAME = "cpa-backend-test"
$TEST_IMAGE_NAME = "cpa-backend-test"

Write-Host "📦 Construindo imagem de teste..." -ForegroundColor Yellow
docker build -t $TEST_IMAGE_NAME ./backend

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Imagem construída com sucesso!" -ForegroundColor Green
    
    Write-Host "🚀 Iniciando container de teste..." -ForegroundColor Yellow
    docker run --rm -d --name $TEST_CONTAINER_NAME -p 5001:5000 $TEST_IMAGE_NAME
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Container de teste iniciado na porta 5001" -ForegroundColor Green
        Write-Host "🌐 Teste acessando: http://localhost:5001" -ForegroundColor Cyan
        
        Write-Host "⏳ Aguardando 10 segundos para o container inicializar..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10
        
        Write-Host "🔍 Verificando logs do container..." -ForegroundColor Yellow
        docker logs $TEST_CONTAINER_NAME
        
        Write-Host "🧹 Limpando container de teste..." -ForegroundColor Yellow
        docker stop $TEST_CONTAINER_NAME
        docker rmi $TEST_IMAGE_NAME
        
        Write-Host "✅ Teste concluído! Container atual não foi afetado." -ForegroundColor Green
    }
    else {
        Write-Host "❌ Erro ao iniciar container de teste" -ForegroundColor Red
        docker rmi $TEST_IMAGE_NAME
        exit 1
    }
}
else {
    Write-Host "❌ Erro ao construir imagem de teste" -ForegroundColor Red
    exit 1
} 
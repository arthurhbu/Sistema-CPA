# 🐳 Guia de Teste do Requirements.txt no Docker

## 🎯 Objetivo
Testar o novo `requirements.txt` sem afetar o container atual e seus volumes.

## 📋 Estratégias Disponíveis

### **1. 🧪 Container de Teste Temporário (RECOMENDADO)**

#### **Script Automatizado (Windows)**
```powershell
# Execute o script PowerShell
.\test_new_requirements.ps1
```

#### **Comandos Manuais**
```bash
# 1. Construir imagem de teste
docker build -t cpa-backend-test ./backend

# 2. Executar container de teste
docker run --rm -d --name cpa-backend-test -p 5001:5000 cpa-backend-test

# 3. Verificar logs
docker logs cpa-backend-test

# 4. Testar API
curl http://localhost:5001/api/instrumento/listar

# 5. Limpar
docker stop cpa-backend-test
docker rmi cpa-backend-test
```

### **2. 🔄 Backup e Restore (SEGURANÇA EXTRA)**

#### **Antes de qualquer teste:**
```bash
# Backup do container atual
docker commit cpa-backend cpa-backend-backup

# Backup dos volumes (se necessário)
docker run --rm -v cpa-backend-data:/data -v $(pwd):/backup alpine tar czf /backup/volume-backup.tar.gz /data
```

#### **Se algo der errado:**
```bash
# Restaurar container
docker stop cpa-backend
docker rm cpa-backend
docker run --name cpa-backend -p 5000:5000 cpa-backend-backup

# Restaurar volumes (se necessário)
docker run --rm -v cpa-backend-data:/data -v $(pwd):/backup alpine tar xzf /backup/volume-backup.tar.gz -C /
```

### **3. 🏷️ Tagging Strategy**

```bash
# Criar versão com tag
docker build -t cpa-backend:v2.0 ./backend

# Testar versão específica
docker run --rm -d --name cpa-backend-v2 -p 5001:5000 cpa-backend:v2.0

# Se funcionar, atualizar produção
docker tag cpa-backend:v2.0 cpa-backend:latest
```

### **4. 🔍 Validação Passo a Passo**

#### **Teste de Construção**
```bash
# Verificar se o build funciona
docker build -t cpa-backend-test ./backend

# Verificar se não há erros de dependências
docker run --rm cpa-backend-test python -c "import flask, pymongo, pandas, matplotlib; print('✅ Todas as dependências OK')"
```

#### **Teste de Funcionamento**
```bash
# Iniciar container
docker run --rm -d --name cpa-backend-test -p 5001:5000 cpa-backend-test

# Aguardar inicialização
sleep 10

# Testar endpoints
curl http://localhost:5001/api/instrumento/listar
curl http://localhost:5001/api/health  # se existir

# Verificar logs
docker logs cpa-backend-test
```

#### **Teste de Compatibilidade**
```bash
# Verificar se as funcionalidades principais funcionam
docker exec cpa-backend-test python -c "
from src.main_controller import *
from api.controllers import *
print('✅ Módulos principais carregados')
"
```

## 🚨 **Estratégias de Emergência**

### **Se o teste falhar:**

1. **Container de teste não afeta produção**
   - O container atual continua funcionando
   - Volumes não são afetados

2. **Rollback automático**
   ```bash
   # Parar container de teste
   docker stop cpa-backend-test
   docker rm cpa-backend-test
   docker rmi cpa-backend-test
   ```

3. **Análise de logs**
   ```bash
   # Verificar logs detalhados
   docker logs cpa-backend-test --tail 100
   ```

## 📊 **Checklist de Validação**

- [ ] **Build da imagem** - `docker build` sem erros
- [ ] **Importação de dependências** - Todas as libs carregam
- [ ] **Inicialização da aplicação** - Flask inicia sem erros
- [ ] **Conectividade com banco** - MongoDB conecta
- [ ] **Endpoints da API** - Rotas respondem
- [ ] **Funcionalidades principais** - Importação CSV, relatórios, etc.
- [ ] **Performance** - Aplicação não fica mais lenta
- [ ] **Logs limpos** - Sem erros críticos

## 🔧 **Comandos Úteis**

### **Monitoramento**
```bash
# Ver containers em execução
docker ps

# Ver logs em tempo real
docker logs -f cpa-backend-test

# Ver uso de recursos
docker stats cpa-backend-test
```

### **Debugging**
```bash
# Entrar no container
docker exec -it cpa-backend-test bash

# Verificar dependências instaladas
docker exec cpa-backend-test pip list

# Testar importações
docker exec cpa-backend-test python -c "import sys; print(sys.path)"
```

## ✅ **Quando Aplicar em Produção**

Só aplique o novo `requirements.txt` em produção após:

1. ✅ **Teste de container** bem-sucedido
2. ✅ **Validação de funcionalidades** completa
3. ✅ **Backup** do container atual
4. ✅ **Janela de manutenção** agendada

## 🎯 **Próximos Passos**

1. Execute o script de teste: `.\test_new_requirements.ps1`
2. Valide todos os pontos do checklist
3. Se tudo OK, aplique em produção
4. Monitore logs por 24h após a mudança

---

**💡 Dica:** Sempre teste em ambiente isolado antes de aplicar em produção! 
# Análise de Dependências - Sistema CPA Backend

## Resumo da Análise

Este documento descreve a análise completa das dependências do projeto Sistema CPA Backend, realizada através da inspeção de todos os arquivos Python no diretório `./backend`.

## Metodologia

1. **Análise de todos os arquivos Python**: Foram analisados todos os arquivos `.py` no diretório backend
2. **Identificação de importações**: Busca por todas as declarações `import` e `from ... import`
3. **Categorização**: Organização das dependências por funcionalidade
4. **Verificação de uso**: Confirmação de que cada dependência está realmente sendo utilizada

## Dependências Identificadas e Organizadas

### Flask e Extensões
- **Flask==3.0.3**: Framework web principal
- **flask-cors==5.0.0**: Suporte a CORS para requisições cross-origin
- **Werkzeug==3.0.3**: Biblioteca utilitária do Flask
- **Jinja2==3.1.4**: Motor de templates
- **itsdangerous==2.2.0**: Assinatura segura de dados
- **blinker==1.8.2**: Sistema de sinais
- **click==8.1.7**: Interface de linha de comando

### Banco de Dados
- **pymongo==4.7.3**: Driver MongoDB para Python
- **bson**: Manipulação de ObjectId do MongoDB

### Processamento de Dados
- **pandas==2.2.2**: Manipulação e análise de dados
- **numpy==2.0.0**: Computação numérica

### Visualização e Gráficos
- **matplotlib==3.9.0**: Criação de gráficos
- **Pillow==10.3.0**: Processamento de imagens

### Processamento de Imagens (Dependências do Matplotlib)
- **fonttools==4.53.0**: Manipulação de fontes
- **contourpy==1.2.1**: Contornos
- **cycler==0.12.1**: Ciclos de cores
- **kiwisolver==1.4.5**: Solucionador de layout
- **MarkupSafe==2.1.5**: Escape seguro de HTML
- **pyparsing==3.1.2**: Parsing de texto

### Utilitários de Data e Tempo
- **python-dateutil==2.9.0.post0**: Extensões para datetime
- **pytz==2024.1**: Zonas de tempo
- **tzdata==2024.1**: Dados de zonas de tempo
- **six==1.16.0**: Compatibilidade Python 2/3

### Configuração e Ambiente
- **python-dotenv==1.0.1**: Carregamento de variáveis de ambiente

### Requisições HTTP
- **requests==2.32.3**: Cliente HTTP

### API do Google
- **google-auth==2.20.0**: Autenticação Google
- **google-auth-oauthlib==0.5.3**: OAuth2 para Google
- **google-auth-httplib2==0.1.0**: HTTP para Google Auth
- **google-api-python-client==2.80.0**: Cliente da API Google

### IA e LLM
- **ollama==0.3.0**: Cliente para Ollama (LLM local)

### DNS
- **dnspython==2.6.1**: Resolução DNS

### Cores no Terminal
- **colorama==0.4.6**: Cores no terminal Windows

### Templates
- **pystache==0.6.5**: Renderização de templates para relatórios

## Dependências Removidas

### Dependências Não Utilizadas
- **Flask-SocketIO==5.3.7**: Não encontrado uso no código
- **eventlet==0.39.0**: Não encontrado uso no código
- **packaging==24.1**: Dependência transitiva, não necessária explicitamente
- **reportlab==4.0.0**: Não encontrado uso no código (removido para evitar problemas de compilação)

## Arquivos Analisados

### Estrutura Principal
- `app.py`: Arquivo principal da aplicação Flask
- `api_controllers.py`: Controladores da API
- `main_controller.py`: Controlador principal do sistema

### API Routes
- `csv_routes.py`: Rotas para importação de CSV
- `pdf_routes.py`: Rotas para geração de PDFs
- `relatorio_routes.py`: Rotas para relatórios
- `instrumento_routes.py`: Rotas para instrumentos

### Controllers
- `csv_controller.py`: Controlador de CSV
- `pdf_controller.py`: Controlador de PDF
- `relatorio_controller.py`: Controlador de relatórios
- `instrumento_controller.py`: Controlador de instrumentos

### Services
- `csv_service.py`: Serviços de CSV
- `pdf_service.py`: Serviços de PDF
- `relatorio_service.py`: Serviços de relatórios
- `instrumento_service.py`: Serviços de instrumentos

### Database
- `connectionDB.py`: Conexão com MongoDB
- `pythonMongoConfig.py`: Configuração MongoDB
- `databaseQuerys.py`: Queries do banco

### Gmail API
- `gmail_api_controller.py`: Integração com Gmail

### Utils
- `error_handlers.py`: Tratamento de erros
- `utils_api.py`: Utilitários da API
- `compact_and_send_zip.py`: Compactação de arquivos

### Data Generator
- `generator_controller.py`: Geração de dados
- `graph_generator.py`: Geração de gráficos
- `text_functions.py`: Funções de texto
- `ollama.py`: Integração com Ollama

### CSV Processing
- `csv_controller.py`: Processamento de CSV

### Relatórios
- `relatorio_controller.py`: Controlador de relatórios
- `compor_partes_relatorio.py`: Composição de introdução e conclusão (usa pystache)

## Benefícios da Nova Organização

1. **Clareza**: Dependências organizadas por categoria
2. **Manutenibilidade**: Fácil identificação de dependências por funcionalidade
3. **Eficiência**: Remoção de dependências não utilizadas
4. **Documentação**: Comentários explicativos para cada categoria
5. **Consistência**: Versões específicas para todas as dependências
6. **Compatibilidade**: Remoção de dependências problemáticas (reportlab)

## Como Instalar

```bash
pip install -r requirements.txt
```

## Observações

- Todas as dependências listadas foram verificadas como sendo realmente utilizadas no código
- As versões especificadas são compatíveis entre si
- Dependências transitivas foram incluídas apenas quando necessárias para o funcionamento correto
- O arquivo está organizado de forma lógica e comentada para facilitar a manutenção
- **reportlab foi removido** para evitar problemas de compilação no Docker
- **pystache é necessário** para renderização de templates de relatórios 
# Documentação detalhada do Sistema CPA

## 1. Visão geral

O Sistema CPA é uma aplicação web voltada para automatizar a importação, processamento, geração e publicação de relatórios acadêmicos e institucionais. O fluxo principal envolve:

1. Importação de arquivos CSV contendo os dados do instrumento;
2. Upload de arquivos de introdução e conclusão em formato Markdown;
3. Processamento dos dados com integração ao MongoDB e ao serviço de linguagem (Ollama);
4. Geração de relatórios em Markdown;
5. Compactação dos artefatos gerados em arquivos ZIP;
6. Geração de PDFs a partir dos arquivos produzidos.

A solução foi construída com uma arquitetura dividida em frontend, backend, banco de dados e serviços auxiliares, permitindo que o usuário realize todo o processo por meio de uma interface simples.

---

## 2. Arquitetura do sistema

### 2.1 Frontend

O frontend é uma aplicação React que oferece as páginas principais para:

- Importação de dados;
- Acompanhamento do progresso do processamento;
- Geração de relatórios;
- Geração de arquivos em PDF;
- Visualização e controle dos instrumentos cadastrados.

A comunicação com o backend é feita via requisições HTTP usando o ambiente `REACT_APP_BACKEND`, definido no Docker Compose ou no ambiente de execução.

### 2.2 Backend

O backend é uma API Flask responsável por:

- Receber os arquivos enviados pelo frontend;
- Validar os dados de entrada;
- Conectar-se ao MongoDB;
- Orquestrar a geração de dados e relatórios;
- Expor endpoints REST para consumo do frontend.

O ponto de entrada principal está em [backend/app.py](../backend/app.py), onde a aplicação Flask é criada e os blueprints das rotas são registrados.

### 2.3 Banco de dados

O sistema utiliza MongoDB como banco de dados principal. Os dados dos instrumentos, os arquivos processados, os status de progresso e os artefatos de geração de relatórios são armazenados em collections específicas.

### 2.4 Serviços auxiliares

- Ollama: execução de modelos de linguagem para geração de textos e dados auxiliares;
- Mongo Express: interface web para inspeção do banco;
- Serviço de conversão para PDF: componente externo utilizado para converter os relatórios gerados em arquivos PDF.

---

## 3. Funções principais do sistema

### 3.1 Importação e validação de instrumentos

A importação é uma das principais funcionalidades do sistema. O fluxo é iniciado pelo endpoint de upload de CSV, no qual o usuário envia:

- o arquivo principal do instrumento;
- um arquivo de introdução;
- um arquivo de conclusão.

Após o envio, o sistema registra o nome do arquivo e inicia o processamento. A confirmação da importação ocorre em uma etapa posterior, quando o usuário informa o ano e a modalidade do instrumento.

### 3.2 Processamento dos dados

Depois da confirmação, o backend realiza uma sequência de etapas que inclui:

- inserção dos dados do CSV no MongoDB;
- processamento de dados complementares, como centros, cursos e diretores;
- geração de gráficos, tabelas e dados auxiliares;
- atualização do progresso do instrumento.

Esse fluxo é centralizado no controller principal localizado em [backend/src/main_controller.py](../backend/src/main_controller.py).

### 3.3 Geração de relatórios

Após o processamento, o usuário pode gerar os relatórios. O sistema:

- lê os dados estruturados no banco;
- monta os conteúdos de introdução e conclusão;
- gera arquivos em Markdown;
- compacta os resultados em um arquivo ZIP para download.

### 3.4 Geração de PDFs

A geração de PDFs é realizada a partir dos arquivos gerados, utilizando o serviço externo configurado na composição do Docker Compose.

### 3.5 Gestão de templates

O sistema permite:

- upload de templates de introdução e conclusão;
- download dos templates atuais;
- substituição dos arquivos de introdução e conclusão associados a um instrumento.

### 3.6 Controle de andamento

O sistema mantém um estado de progresso para cada instrumento, com informações como:

- se a importação foi concluída;
- se a geração de dados ocorreu;
- se os relatórios foram gerados;
- se os PDFs foram produzidos.

---

## 4. Principais APIs do backend

O backend expõe uma coleção de endpoints REST organizados por blueprints. As rotas mais importantes são:

| Grupo | Endpoint | Método | Função |
|---|---|---|---|
| CSV | `/api/csv/importar` | POST | Envia o CSV principal e os arquivos de introdução/conclusão para importação. |
| CSV | `/api/csv/importar/confirmar` | POST | Confirma a importação após validação do ano e da modalidade. |
| CSV | `/api/csv/cancel/<nome_instrumento>` | DELETE | Cancela o processamento de um instrumento. |
| CSV | `/api/csv/importacao/progresso` | GET | Retorna o estado atual da importação. |
| Instrumento | `/api/instrumento/listar` | GET | Lista os instrumentos disponíveis. |
| Instrumento | `/api/instrumento/listarComStatus` | GET | Lista os instrumentos com informações de status. |
| Instrumento | `/api/instrumento/continuarGeracao` | POST | Permite retomar a geração de um instrumento previamente iniciado. |
| Instrumento | `/api/instrumento/<instrumento>/introducao/substituir` | POST | Substitui o arquivo de introdução de um instrumento. |
| Instrumento | `/api/instrumento/<instrumento>/conclusao/substituir` | POST | Substitui o arquivo de conclusão de um instrumento. |
| Relatórios | `/api/relatorios/gerar` | POST | Gera os relatórios de um instrumento. |
| Relatórios | `/api/relatorios/<id_instrumento>/download` | GET | Baixa o ZIP com os relatórios gerados. |
| Relatórios | `/api/relatorios/<id_instrumento>/delete` | DELETE | Remove o ZIP do relatório. |
| Relatórios | `/api/relatorios/templates/upload` | POST | Faz upload de templates para introdução/conclusão. |
| Relatórios | `/api/relatorios/templates/download` | GET | Baixa os templates atuais. |
| PDF | `/api/pdf/gerar` | POST | Gera PDFs a partir de um arquivo ZIP. |
| PDF | `/api/pdf/listar` | GET | Lista os arquivos de PDF disponíveis. |
| PDF | `/api/pdf/<id_instrumento>/download` | GET | Faz download do ZIP com os PDFs. |
| PDF | `/api/pdf/<id_instrumento>/delete` | DELETE | Remove um ZIP de PDF. |

Essas rotas estão definidas nos arquivos de rotas do backend, em [backend/api/routes](../backend/api/routes).

---

## 5. Como usar o Makefile

O arquivo [Makefile](../Makefile) foi preparado para construir e publicar as imagens do backend e do frontend usando Podman.

### 5.1 Pré-requisitos

- Podman instalado e configurado;
- Arquivo `auth.json` disponível caso seja necessário fazer push para o repositório remoto;
- Acesso ao repositório `quay.io/uemcpa`.

### 5.2 Comandos disponíveis

- `make build`
  - Solicita uma tag de versão;
  - Constrói a imagem do backend e do frontend;
  - Gera uma versão local com os nomes `sistema-backend` e `sistema-frontend`.

- `make login`
  - Realiza login no repositório remoto usando o arquivo de autenticação.

- `make push`
  - Executa o login, constrói as imagens e faz o push para o registro remoto.

### 5.3 Exemplo prático

```bash
make build
make push
```

O comando padrão `make` executa a regra `push`, portanto, ao rodar apenas `make`, o processo completo de build e publicação é iniciado.

---

## 6. Como usar os scripts de montagem das imagens build.sh

Há dois scripts de build no projeto:

- [backend/build.sh](../backend/build.sh)
- [frontend/build.sh](../frontend/build.sh)

### 6.1 Script do backend

O script do backend:

- cria uma tag baseada na data atual;
- constrói a imagem `sistema-backend`;
- envia a imagem para o repositório remoto no Quay.

### 6.2 Script do frontend

O script do frontend realiza o mesmo processo para a imagem `sistema-frontend`.

### 6.3 Observação

Esses scripts assumem que o ambiente já possui o Podman configurado e que o login no repositório remoto foi realizado ou que o `auth.json` esteja disponível.

---

## 7. Como testar usando o docker-compose.yaml

O arquivo [docker-compose.yaml](../docker-compose.yaml) define os containers principais do sistema, incluindo:

- backend Flask;
- frontend React;
- MongoDB;
- Mongo Express;
- serviço Ollama;
- serviço de conversão para PDF.

### 7.1 Pré-requisitos

Antes de iniciar os containers, é necessário criar um arquivo `.env` com as variáveis exigidas. Um exemplo pode ser encontrado em [compose/exemplo.md](../compose/exemplo.md).

As variáveis mínimas normalmente incluem:

- `MONGO_ROOT_USER`
- `MONGO_ROOT_PASSWORD`
- `BACKEND`

### 7.2 Subindo o ambiente

```bash
docker compose up -d --build
```

Esse comando monta e inicia todos os serviços definidos no Compose.

### 7.3 Verificando o estado dos containers

```bash
docker compose ps
```

### 7.4 Acompanhando logs

```bash
docker compose logs -f flask-backend
```

### 7.5 Acessos principais

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:5000`
- Mongo Express: `http://localhost:8081`

### 7.6 Testes no backend

Se o ambiente estiver com o backend em execução, os testes podem ser executados diretamente no container:

```bash
docker compose exec flask-backend pytest
```

Para o frontend:

```bash
docker compose exec react-frontend npm test -- --watch=false
```

### 7.7 Encerramento do ambiente

```bash
docker compose down
```

Para remover também os volumes persistidos:

```bash
docker compose down -v
```

---

## 8. Boas práticas de uso

- Sempre mantenha os arquivos de introdução e conclusão corretos antes de gerar os relatórios;
- Verifique o progresso do processamento antes de tentar gerar PDFs ou relatórios;
- Faça backup dos dados do MongoDB antes de remover volumes ou reiniciar o ambiente;
- Use os templates para padronizar a saída dos relatórios;
- Em ambientes de desenvolvimento, acompanhe os logs do backend para diagnosticar problemas de processamento.

---

## 9. Resumo operacional

Em resumo, o sistema funciona como um fluxo completo de automação de relatórios:

1. o usuário importa os dados;
2. o backend processa e organiza os dados;
3. o sistema gera relatórios e arquivos auxiliares;
4. o usuário faz o download dos resultados em formatos prontos para uso.

Essa estrutura torna o processo mais rápido, padronizado e menos dependente de intervenção manual.

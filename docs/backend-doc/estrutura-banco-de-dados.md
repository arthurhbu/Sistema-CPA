# Documentação da Estrutura do Banco de Dados NoSQL MongoDB

## Visão Geral
O sistema utiliza múltiplos bancos de dados MongoDB, onde cada banco representa um instrumento de avaliação específico, como por exemplo `Discentes_2023` ou `EAD_2022`. Cada banco de dados contém diversas collections que armazenam diferentes tipos de dados relacionados ao instrumento de avaliação.

## Estrutura de Bancos de Dados
Cada banco de dados representa um instrumento de avaliação e geralmente segue o padrão de nomenclatura:
- `[Tipo]_[Ano]` (Ex: `Discentes_2023`, `EAD_2022`)

## Collections Padrão
As collections típicas presentes em cada banco de dados são:

### 1. centro_por_ano
Contém informações estatísticas sobre os centros de ensino por ano.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| centro_descricao | String | Nome descritivo do centro de ensino |
| respondentes | Integer | Número de respondentes da avaliação |
| matriculados | Integer | Número total de matriculados |
| centro_de_ensino | String | Sigla do centro de ensino |
| porcentagem | Float | Porcentagem de respondentes em relação aos matriculados |

```javascript
// Exemplo de documento em centro_por_ano
{
  "centro_descricao": "Centro de Ciências Agrárias",
  "respondentes": 120,
  "matriculados": 500,
  "centro_de_ensino": "CCA",
  "porcentagem": 24.0
}
```

### 2. centros_e_diretores
Armazena informações sobre os centros de ensino e seus diretores.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| centro_de_ensino | String | Sigla do centro de ensino |
| centro_descricao | String | Nome descritivo do centro de ensino |
| diretor | String | Nome do diretor do centro |
| diretor_adjunto | String | Nome do diretor adjunto do centro |
| ano_da_direcao | String | Ano de referência da gestão |

```javascript
// Exemplo de documento em centros_e_diretores
{
  "centro_de_ensino": "CSA",
  "centro_descricao": "Centro de Ciências Sociais Aplicadas",
  "diretor": "João Silva",
  "diretor_adjunto": "Maria Oliveira",
  "ano_da_direcao": "2020-2024"
}
```

### 3. cursos_e_centros
Contém informações sobre os cursos oferecidos e seus respectivos centros.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| cd_curso | Integer | Código identificador do curso |
| codigo_mec | Integer | Código do curso no MEC |
| centro_de_ensino | String | Sigla do centro ao qual o curso pertence |
| nm_curso | String | Nome do curso |
| matriculados | Integer | Número total de matriculados no curso |
| ano_referencia | Integer | Ano de referência dos dados |

```javascript
// Exemplo de documento em cursos_e_centros
{
  "cd_curso": 8,
  "codigo_mec": 3393,
  "centro_de_ensino": "CSA",
  "nm_curso": "Administração",
  "matriculados": 736,
  "ano_referencia": 2020
}
```

### 4. cursos_por_centro
Apresenta estatísticas sobre cursos agrupados por centro de ensino.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| nm_curso | String | Nome do curso |
| centro_de_ensino | String | Sigla do centro ao qual o curso pertence |
| matriculados | Integer | Número total de matriculados no curso |
| respondentes | Integer | Número de respondentes da avaliação |
| porcentagem | Float | Porcentagem de respondentes em relação aos matriculados |

```javascript
// Exemplo de documento em cursos_por_centro
{
  "nm_curso": "Agronomia",
  "centro_de_ensino": "CCA",
  "matriculados": 453,
  "respondentes": 35,
  "porcentagem": 7.73
}
```

### 5. etapas
Controla o status das etapas de processamento do instrumento de avaliação.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| 'Inserção/Análise do instrumento' | Boolean | Status da etapa de inserção e análise |
| 'Geração de Relatórios' | Boolean | Status da etapa de geração de relatórios |
| 'Revisão de Relatórios' | Boolean | Status da etapa de revisão dos relatórios |
| 'Correção de possíveis erros' | Boolean | Status da etapa de correção de erros |
| 'Geração de PDFs' | Boolean | Status da etapa de geração de PDFs |
| 'Entrega dos Relatórios' | Boolean | Status da etapa de entrega dos relatórios |
| Finalizado | Boolean | Indica se todo o processo foi finalizado |

```javascript
// Exemplo de documento em etapas
{
  "Inserção/Análise do instrumento": false,
  "Geração de Relatórios": false,
  "Revisão de Relatórios": false,
  "Correção de possíveis erros": false,
  "Geração de PDFs": false,
  "Entrega dos Relatórios": false,
  "Finalizado": false
}
```

### 6. instrumento
Armazena os dados detalhados das perguntas e respostas da avaliação.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| cd_curso | Integer | Código identificador do curso |
| nm_curso | String | Nome do curso |
| centro_de_ensino | String | Sigla do centro de ensino |
| cd_grupo | Integer | Código do grupo de perguntas |
| nm_grupo | String | Nome do grupo de perguntas |
| cd_subgrupo | Integer | Código do subgrupo de perguntas |
| nm_subgrupo | String | Nome do subgrupo de perguntas |
| cd_disciplina | Integer | Código da disciplina (0 quando não se aplica) |
| nm_disciplina | String | Nome da disciplina ('-' quando não se aplica) |
| ordem_pergunta | Integer | Ordem da pergunta no questionário |
| cd_pergunta | Integer | Código identificador da pergunta |
| nm_pergunta | String | Texto da pergunta |
| ordem_opcoes | Integer | Ordem das opções de resposta |
| total_do_curso | Integer | Total de respondentes do curso |
| pct_por_opcao | Object | Percentual de respostas para cada opção |
| path | String | Caminho para o arquivo da figura do gráfico |
| relatorioGraficoAI | String | Legenda gerada por IA para o gráfico |
| tabela | String | Tabela formatada em markdown com os resultados |
| tituloGraficoAI | String | Título gerado por IA para o gráfico |

```javascript
// Exemplo de documento em instrumento
{
  "cd_curso": 56,
  "nm_curso": "Pedagogia",
  "centro_de_ensino": "EAD",
  "cd_grupo": 68,
  "nm_grupo": "Avaliação discente geral",
  "cd_subgrupo": 237,
  "nm_subgrupo": "1. Avaliação discente sobre a autoavaliação",
  "cd_disciplina": 0,
  "nm_disciplina": "-",
  "ordem_pergunta": 1,
  "cd_pergunta": 1831,
  "nm_pergunta": "1.1- Sua frequência nas disciplinas presenciais",
  "ordem_opcoes": 8139,
  "total_do_curso": 7,
  "pct_por_opcao": {
    "Bom": 85.71,
    "Regular": 14.29,
    "Ruim": 0,
    "Péssimo": 0
  },
  "path": "./figurasGrafico/fig_56_237_1831",
  "relatorioGraficoAI": "Legenda gerada por ia, é uma str",
  "tabela": "| Indicador | Bom | Regular | Ruim | Péssimo | Respondentes | \n|---|---|---|---|---|---| \n| Sua frequência nas disciplinas presenciais | 85,71% | 14,29% | 0,0% | 0,0% | 7 | ",
  "tituloGraficoAI": "-"
}
```

### 7. progresso_da_inserção
Rastreia o progresso das etapas de inserção e processamento de dados.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| instrumento | String | Nome do instrumento de avaliação |
| Insercao_Main_CSV | String | Status da inserção do CSV principal |
| Insercao_Curso_Centro_Database | String | Status da inserção na collection cursos_e_centros |
| Insercao_Centro_Diretor_Database | String | Status da inserção na collection centros_e_diretores |
| Geracao_de_Dados | String | Status da geração de dados processados |
| Criacao_Cursos_por_Centro_Database | String | Status da criação da collection cursos_por_centro |
| Criacao_Centro_por_Ano_Database | String | Status da criação da collection centro_por_ano |

```javascript
// Exemplo de documento em progresso_da_inserção
{
  "instrumento": "EAD2021_AvaliaçãoDistância",
  "Insercao_Main_CSV": "Finalizado",
  "Insercao_Curso_Centro_Database": "Finalizado",
  "Insercao_Centro_Diretor_Database": "Finalizado",
  "Geracao_de_Dados": "Finalizado",
  "Criacao_Cursos_por_Centro_Database": "Finalizado",
  "Criacao_Centro_por_Ano_Database": "Finalizado"
}
```

## Relacionamentos Implícitos

Embora o MongoDB seja um banco de dados NoSQL sem relacionamentos formais, existem relacionamentos implícitos entre as collections:

- `centro_de_ensino` é utilizado como chave de referência entre as collections, relacionando centros, cursos e instrumentos
- `cd_curso` relaciona os cursos entre as collections cursos_e_centros e instrumento
- O campo `instrumento` na collection progresso_da_inserção corresponde ao nome do banco de dados

## Consultas Comuns

### Consulta de cursos por centro de ensino
```javascript
db.cursos_e_centros.find({ centro_de_ensino: "CSA" })
```

### Consulta de perguntas por curso
```javascript
db.instrumento.find({ cd_curso: 56 })
```

### Consulta de estatísticas por centro
```javascript
db.centro_por_ano.find({ centro_de_ensino: "CCA" })
```

### Verificação do status de progresso
```javascript
db.progresso_da_inserção.findOne({ instrumento: "EAD2021_AvaliaçãoDistância" })
```

## Criação de Índices

Para otimizar o desempenho do banco de dados, é recomendável criar os seguintes índices:

```javascript
// Índices para cursos_e_centros
db.cursos_e_centros.createIndex({ centro_de_ensino: 1 })
db.cursos_e_centros.createIndex({ cd_curso: 1 })
db.cursos_e_centros.createIndex({ nm_curso: 1 })

// Índices para instrumento
db.instrumento.createIndex({ cd_curso: 1 })
db.instrumento.createIndex({ centro_de_ensino: 1 })
db.instrumento.createIndex({ cd_grupo: 1 })
db.instrumento.createIndex({ cd_subgrupo: 1 })
db.instrumento.createIndex({ cd_pergunta: 1 })

// Índices para outros collections
db.cursos_por_centro.createIndex({ centro_de_ensino: 1 })
db.centro_por_ano.createIndex({ centro_de_ensino: 1 })
```

## Fluxo de Processamento de Dados

Baseando-se na collection `progresso_da_inserção`, o fluxo típico de processamento parece ser:
1. Inserção do CSV principal
2. Inserção de dados de cursos e centros
3. Inserção de dados de centros e diretores
4. Geração de dados processados
5. Criação de collections agregadas (cursos_por_centro, centro_por_ano)
6. Seguimento das etapas na collection `etapas` até a finalização


Esta documentação fornece uma visão geral da estrutura do banco de dados MongoDB utilizado para armazenar e processar dados de instrumentos de avaliação institucional.
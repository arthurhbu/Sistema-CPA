# Estrutura do Backend  

Nosso sistema foi inicialmente construído utilizando apenas Python e MongoDB, sendo executado localmente com o auxílio de algumas bibliotecas que facilitam seu funcionamento. Com o avanço do desenvolvimento, incorporamos o Flask para a construção da API, permitindo a comunicação com o frontend e o processamento das requisições.  

O backend é dividido em duas camadas principais: **a Camada da API** e **a Camada de Processamento e Logística do Sistema**.  

## **Camada da API**  

Essa camada é responsável pela comunicação com o frontend e pela chamada das funções da camada de Processamento. Ela contém um **Controller**, que centraliza todas as rotas e suas respectivas funções.  

Se for necessário modificar alguma rota ou função, elas podem ser encontradas dentro do Controller. Essa camada é relativamente simples, lidando apenas com as requisições vindas do frontend; toda a lógica de processamento está na camada seguinte.  

## **Camada de Processamento**  

A camada de Processamento representa a maior parte do backend e está localizada no diretório `./src/`. Como seu escopo é extenso, foi subdividida nos seguintes repositórios:  

### **📂 /csv**  
- Responsável pela filtragem e inserção dos arquivos CSV no sistema.  
- Trata tanto os CSVs principais (instrumento) quanto os CSVs auxiliares usados na geração de relatórios.  

### **📂 /data_generator**  
- Gera informações para os relatórios, incluindo gráficos e tabelas.  
- Possui um **Controller** que gerencia essas funções e envia os dados gerados para o banco de dados do instrumento.  

### **📂 /ollama**  
- Armazena funções específicas para a geração de informações provenientes da LLM (Large Language Model).  
- Essas funções também são utilizadas pelo Controller de geração de dados.  

### **📂 /relatorio**  
- Contém todas as funções relacionadas à geração de relatórios em Markdown.  

### **📂 /utils**  
- Armazena funções auxiliares utilizadas nos demais repositórios.  

Cada um desses repositórios desempenha um papel específico no processamento e na geração de dados do sistema.  

O **Main Controller** gerencia essas camadas, implementando funções consumidas diretamente pela API. Ele atua como uma camada intermediária entre a API e a Camada de Processamento, garantindo a integração e a organização do fluxo de dados.  

---

## **Documentação de Funções**  

Cada função do sistema está documentada com **docstrings**, contendo descrições detalhadas e informações sobre os parâmetros utilizados.  

Caso precise compreender o funcionamento de uma função específica, consulte a documentação no próprio código-fonte.  

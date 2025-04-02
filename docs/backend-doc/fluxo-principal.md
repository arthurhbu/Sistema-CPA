# # Fluxo Principal do Sistema

O fluxo do sistema da CPA é construído com base nas etapas que existem para gerar um relatório completo: 

- Importar arquivo CSV
- Gerar relatórios em formato MD
- Gerar arquivos PDFs por meio dos Markdowns

Cada uma dessas etapas está implementada no arquivo Main Controller e pode ser consumida separadamente pela API. Ou seja, as etapas não são executadas de forma contínua, mas sim sob demanda.

## Fluxograma da importação

O fluxo de importação é feito a partir de nosso frontend, onde o usuário precisa mandar o arquivo CSV, definir o ano daquele instrumento e escolher qual o tipo/modal do instrumento.


![](./Fluxo%20Importação.png)

## Fluxograma da geração de dados

A geração de dados ocorre **automaticamente** após a inserção dos arquivos CSV. Assim, o usuário não precisa fazer nenhuma requisição manual para iniciar essa etapa. 

![](./Fluxo%20Geração%20de%20dados.png)

## Fluxograma de geração de relatórios

A geração de relatórios é iniciada manualmente pelo usuário. Ele pode selecionar um instrumento já processado e solicitar a geração do relatório, enviando apenas o ano correspondente do instrumento.

![](./Fluxo%20Geração%20de%20Relatórios.png)

# 

O fluxo principal do sistema é relativamente simples quando observado por suas etapas individuais. No entanto, para um entendimento mais aprofundado do funcionamento interno, consulte o arquivo main_controller.py.

Além disso, no Controller da API, é possível visualizar todas as rotas disponíveis e suas respectivas funções utilizadas pelo frontend.
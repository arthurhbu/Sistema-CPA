# Projeto Relatórios CPA

Sistema de automação dos relatórios da UEM CPA. 

Para iniciar, sugiro que configure as variáveis de ambiente.

[Variáveis environment][compose/exemplo.md]

# Uso com Podman-Compose

Na pasta Compose você pode executar os composes em dois níveis:

Backend

```
podman-compose -f backend.yaml pull

podman-compose -f backend.yaml up -d
```

Tomar cuidado para importar o banco de dados original, caso haja necessidade.

Frontend

```
podman-compose -f frontend.yaml pull

podman-compose -f frontend.yaml up -d
```

## Portas que devem ser abertas

- Acesso ao FrontEnd - 3000
- Acesso ao Mongo Express - 8081

# Pendências

    PRIORIDADE:
        - Tela home adicionar o passo a passo do que fazer (PROXIMO A FAZER). Parte das etapas foi adicionado, mas o Tutotrial pode ficar melhor eu acho.
        - Melhorar a tela Home
        - Tentar aprimorar o cabeçalho futuramente
        - Terminar o backend Gerar Relatórios, com a parte de enviar no email os relatórios gerados(Falta testar no servidor da uem para ver se realmente está enviando.)

    PARA FAZER:
    - Melhorar o footer
    - Criar a tela Gerar PDFs e o backend 
    - Autenticação para Login de funcionários da CPA    
    
    - Pagina para alterar arquivos de introdução e conclusao
    - Página para correção de possíveis problemas envolvendo formatação e afins.
    - Realizar um teste completo, onde faça cada etapa necessária.
    - Talvez ter que criar uma slidebar para escolher qual csv estara sendo importado para que não haja problemas na hora da importação. Mas isso podemos esperar a próxima leva de CSVs

# Finalizados

    - Confirmação se o cabeçalho está correto com o padrão (POPUP DE IMPORTAÇAO FINALIZADO, ACREDITO QUE SEJA ISSO NO MOMENTO PARA A PAGINA)
    - Tela de progresso, adicionar logs (ACREDITO ESTAR FINALIZADO, CONFIRMAR PARA VER O QUE O PROFESSOR ACHA COMO FICOU)

    

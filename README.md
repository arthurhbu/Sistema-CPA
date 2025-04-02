# Sistema de Geração de Relatórios CPA

  

Sistema de automação dos relatórios da UEM CPA com o auxílio de uma LLM.

Um sistema desenvolvido com o intuito de agilizar e automatizar processos que envolvem a geração de relatórios provenientes do departamento da CPA (Comissão Própria de Avaliação).

# Tecnologias Utilizadas

- Flask
- React.js
- MongoDB
- Pandas
- Ollama
- GoogleAPI
- Docker
	
	

		

 
# Status do projeto: 

O projeto atualmente já está em produção mas certar partes ainda estão sendo desenvolvidas.

# Requisitos

Os requisitos para se rodar o Sistema é ter o Podman instalado em sua máquina e no caso de usar Windows, tenha Podman Desktop instalado.

# Documentação

O Sistema possui um diretório somente para documentação do código contendo detalhadamente os principais fluxos do sistema e sobre cada função.

Em caso de futura refatoração ou mudança de alguma parte do sistema, confira a documentação pois tudo que for necessário para realizar tal tarefa estará nesse diretório.


  




  

# Uso com Podman-Compose

 Para iniciar, sugiro que configure as variáveis de ambiente. [Variáveis environment][compose/exemplo.md]



Na pasta Compose você pode executar os composes em dois níveis:

  

- Backend

  

```

podman-compose -f backend.yaml pull

  

podman-compose -f backend.yaml up -d

```

  

Tomar cuidado para importar o banco de dados original, caso haja necessidade.

  

- Frontend

  

```

podman-compose -f frontend.yaml pull

  

podman-compose -f frontend.yaml up -d

```

  

## Portas que devem ser abertas
  
- Acesso ao FrontEnd - 3000

- Acesso ao Mongo Express - 8081

  



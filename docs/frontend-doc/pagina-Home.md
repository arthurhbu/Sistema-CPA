# Documentação da Página Home

## Visão Geral
O componente `Home` serve como a página inicial do sistema da Comissão Própria de Avaliação (CPA). Ele permite que os usuários selecionem um instrumento e acompanhem o progresso das etapas de avaliação, além de fornecer um tutorial passo a passo sobre como utilizar o sistema.

## Funcionalidades
- Seleção de um instrumento para visualizar as etapas de avaliação
- Exibição de uma checklist das etapas do processo de avaliação
- Atualização do estado das etapas ao interagir com a checklist
- Tutorial passo a passo para guiar os usuários na geração de relatórios
- Informações sobre a CPA e o sistema de geração automática de relatórios

## Dependências
- React Hooks: `useEffect`, `useState`
- Componentes personalizados: `SelectAutoWidth`
- Biblioteca de UI: `@mui/material` (para o componente `Checkbox`)
- Imagem: `cpa_banner.png` para o banner da CPA
- React Router: `Link` para navegação entre páginas

## API Consumida
O componente consome as seguintes APIs:
- **Endpoint para obter instrumentos**: `${process.env.REACT_APP_BACKEND}/api/instrumentos`
  - **Método**: GET
  - **Resposta esperada**:
    ```json
    [
      "instrumento1",
      "instrumento2",
      ...
    ]
    ```

- **Endpoint para obter etapas de um instrumento**: `${process.env.REACT_APP_BACKEND}/api/instrumento/etapas`
  - **Método**: POST
  - **Corpo da requisição**:
    ```json
    {
      "instrumento": "string"
    }
    ```
  - **Resposta esperada**:
    ```json
    {
      "etapas": {
        "Inserção/Análise do instrumento": boolean,
        "Geração de Relatórios": boolean,
        ...
      }
    }
    ```

- **Endpoint para atualizar o estado de uma etapa**: `${process.env.REACT_APP_BACKEND}/api/instrumento/etapa/atualizar`
  - **Método**: POST
  - **Corpo da requisição**:
    ```json
    {
      "instrumento": "string",
      "etapa": "string",
      "novoValor": boolean
    }
    ```

## Estados (States)
| Estado        | Tipo     | Descrição                                               |
|---------------|----------|---------------------------------------------------------|
| `instrumento` | String   | Instrumento selecionado pelo usuário                   |
| `databases`   | Array    | Lista de instrumentos disponíveis                       |
| `etapas`      | Object   | Objeto contendo o estado das etapas do instrumento      |

## Fluxo de Dados
1. Ao montar o componente, `fetchDatabase()` é chamado para buscar a lista de instrumentos disponíveis.
2. Quando um instrumento é selecionado, `getStepsDatabase(instrumento)` é chamado para buscar as etapas associadas a esse instrumento.
3. O usuário pode interagir com a checklist para atualizar o estado das etapas, que chama `handleCheckboxChange(etapa)` para enviar a atualização ao backend.
4. As etapas são exibidas em uma lista, permitindo que o usuário visualize o progresso.

## Interface do Usuário
O componente exibe as seguintes seções principais:

### Seção: Boas-vindas e Seleção de Instrumento
- Mensagem de boas-vindas ao sistema da CPA.
- Dropdown para seleção do instrumento.
- Checklist das etapas do processo de avaliação, onde cada etapa pode ser marcada ou desmarcada.

### Seção: Tutorial Passo a Passo
- Título "Tutorial Passo a Passo" com instruções sobre como gerar relatórios.
- Quatro passos detalhados, cada um com uma descrição e um botão que leva a páginas específicas do sistema:
  1. Inserir arquivo do instrumento (link para a página de importação).
  2. Acompanhar o progresso da inserção (link para a página de progresso).
  3. Gerar relatórios (link para a página de geração de relatórios).
  4. Gerar PDFs (link para a página de geração de PDFs).

### Seção: Informações sobre a CPA e o Sistema
- Informações sobre a Comissão Própria de Avaliação (CPA) e suas funções.
- Descrição do sistema de geração automática de relatórios, incluindo seu objetivo e funcionalidades.

## Estilos
Os estilos são gerenciados através de CSS Modules no arquivo `Home.module.css`, garantindo o escopo local dos estilos.

## Exemplo de Uso
```jsx
import Home from './components/Home';

function App() {
  return (
    <div className="App">
      <Home />
    </div>
  );
}
```

## Considerações de Performance
- O componente utiliza `useEffect` para buscar dados apenas quando necessário, evitando chamadas desnecessárias à API.
- A atualização do estado das etapas é feita de forma otimizada, garantindo que o estado local seja atualizado antes de enviar a requisição ao backend.
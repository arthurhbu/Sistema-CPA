# Documentação da Página Importar

## Visão Geral
O componente `Importar` permite que os usuários façam upload de arquivos CSV e Markdown para processamento. Ele fornece uma interface para selecionar a modalidade do instrumento, inserir o ano do relatório e acompanhar o progresso da inserção.

## Funcionalidades
- Permite o upload de arquivos CSV e Markdown através de uma interface de arrastar e soltar (dropzone).
- Exibe os arquivos selecionados e suas informações.
- Valida o cabeçalho do arquivo CSV em relação aos cabeçalhos esperados.
- Exibe popups para mensagens de erro e sucesso durante o processo de importação.
- Acompanha o status de processamento de inserções em andamento.

## Dependências
- React Hooks: `useEffect`, `useState`, `useMemo`
- Componentes personalizados: `StyledInput`, `UploadButton`, `SelectAutoWidth`, `HeaderPopup`
- Ícones: `FaFileCsv` e `BsMarkdownFill` para representar arquivos CSV e Markdown, respectivamente.
- Imagem: `upload_logo.png` para o logo de upload

## API Consumida
O componente consome as seguintes APIs:
- **Endpoint para verificar o status de processamento**: `${process.env.REACT_APP_BACKEND}/api/csv/importacao/progresso`
  - **Método**: GET
  - **Resposta esperada**:
    ```json
    {
      "processing": boolean
    }
    ```

- **Endpoint para importar CSV**: `${process.env.REACT_APP_BACKEND}/api/csv/importar`
  - **Método**: POST
  - **Corpo da requisição**:
    ```json
    {
      "file": File,
      "ano": string
    }
    ```
  - **Resposta esperada**:
    ```json
    {
      "header": Array,
      "error": string
    }
    ```

- **Endpoint para importar CSV**: `${process.env.REACT_APP_BACKEND}/api/csv/cancel/${fileNameWithoutExtension}`
  - **Método**: DELETE
  - **Resposta esperada**:
    ```json
    {
      "message": string,
      "error": string
    }
    ```

- **Endpoint para confirmar a importação**: `${process.env.REACT_APP_BACKEND}/api/csv/importar/confirmar`
  - **Método**: POST
  - **Corpo da requisição**:
    ```json
    {
      "ano": string,
      "modalidade": string
    }
    ```
  - **Resposta esperada**:
    ```json
    {
      "message": string
    }
    ```

## Estados (States)
| Estado                   | Tipo     | Descrição                                               |
|--------------------------|----------|---------------------------------------------------------|
| `files`                  | Array    | Lista de arquivos selecionados para upload              |
| `ano`                    | String   | Ano do relatório a ser gerado                           |
| `popupHeaderVisible`     | Boolean  | Indica se o popup do cabeçalho está visível             |
| `popupImportVisible`     | Boolean  | Indica se o popup de importação está visível            |
| `popupImportMessage`     | String   | Mensagem a ser exibida no popup de importação           |
| `importStatus`           | Number   | Status da importação (ex: 200 para sucesso)             |
| `popupErrorVisible`      | Boolean  | Indica se o popup de erro está visível                  |
| `header`                 | Array    | Cabeçalho do arquivo CSV importado                      |
| `errorMessage`           | String   | Mensagem de erro a ser exibida                          |
| `isProcessing`           | Boolean  | Indica se a importação está em andamento                |
| `selectedCsvType`        | String   | Modalidade do instrumento selecionado                   |

## Fluxo de Dados
1. O usuário seleciona a modalidade do instrumento e faz o upload dos arquivos CSV e Markdown.
2. O cabeçalho do arquivo CSV é verificado em relação aos cabeçalhos esperados.
3. O usuário insere o ano do relatório e clica no botão de importação.
4. O sistema envia os arquivos para o backend e aguarda a resposta.
5. Se a importação for bem-sucedida, um popup de sucesso é exibido; caso contrário, um popup de erro é mostrado.

## Interface do Usuário
O componente exibe as seguintes seções principais:

### Seção: Informações da Página
- Título "Inserir Arquivo" e descrição sobre o processo de inserção.
- Instruções sobre a necessidade de inserir um arquivo CSV e um arquivo ZIP com a introdução e conclusão.

### Seção: Seleção da Modalidade
- Dropdown para selecionar a modalidade do instrumento a ser processado.

### Seção: Upload de Arquivos
- Área de dropzone para arrastar e soltar arquivos.
- Exibição dos arquivos CSV e Markdown selecionados.

### Seção: Input de Ano e Botão de Importação
- Campo de entrada para o ano do relatório.
- Botão "Importar" para iniciar o processo de importação.

### Popups
- Popup para exibir o cabeçalho do CSV e compará-lo com o cabeçalho modelo.
- Popup de erro para exibir mensagens de erro durante o processo de importação.
- Popup de sucesso para exibir mensagens de confirmação após a importação.

## Estilos
Os estilos são gerenciados através de CSS Modules no arquivo `Importar.module.css`, garantindo o escopo local dos estilos.

## Exemplo de Uso
```jsx
import Importar from './components/Importar';

function App() {
  return (
    <div className="App">
      <Importar />
    </div>
  );
}
```

## Considerações de Performance
- O componente utiliza `useEffect` para verificar o status de processamento a cada 15 segundos.
- A validação do cabeçalho do CSV é feita antes de prosseguir com a importação, garantindo que os dados estejam no formato correto.
- O uso de `useMemo` para otimizar o estilo da dropzone com base no estado atual.
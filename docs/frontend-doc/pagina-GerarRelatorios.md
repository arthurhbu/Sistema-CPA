# Documentação da Página Gerar Relatório

## Visão Geral
O componente `GerarRelatorio` permite que os usuários gerem relatórios a partir de instrumentos selecionados. Ele coleta informações como ano, tipo de introdução e conclusão, e fornece opções para download e exclusão de relatórios gerados.

## Funcionalidades
- Permite a seleção de um instrumento para geração de relatórios
- Coleta informações sobre ano e tipo de introdução/conclusão
- Gera relatórios e os envia para o email da secretaria
- Exibe uma lista de relatórios gerados com opções para download e exclusão
- Atualiza a lista de relatórios disponíveis

## Dependências
- React Hooks: `useEffect`, `useState`
- Componentes personalizados: `StyledInput`, `SelectAutoWidth`
- CSS Modules: `GerarRelatorio.module.css`
- Imagem: `trash.png` para o ícone de exclusão

## API Consumida
O componente consome as seguintes APIs:
- **Endpoint para zips disponíveis**: `${process.env.REACT_APP_BACKEND}/api/relatorios/zips`
  - **Método**: GET
  - **Resposta esperada**:
    ```json
    {
      "zips": [
        {
          "id": string,
          "filename": string,
          "size": number
        }
      ]
    }
    ```

- **Endpoint para gerar relatório**: `${process.env.REACT_APP_BACKEND}/api/relatorio/gerar`
  - **Método**: POST
  - **Corpo da requisição**:
    ```json
    {
      "ano": string,
      "introConcl": string,
      "instrumento": string
    }
    ```
  - **Resposta esperada**:
    ```json
    {
      "id_instrumento": string,
      "error": string
    }
    ```

- **Endpoint para download de zip**: `${process.env.REACT_APP_BACKEND}/api/relatorios/${idInstrumento}/download`
  - **Método**: GET

- **Endpoint para deletar zip**: `${process.env.REACT_APP_BACKEND}/api/relatorios/${idInstrumento}/delete`
  - **Método**: DELETE
  - **Resposta esperada**:
    ```json
    {
      "error": string
    }
    ```

## Estados (States)
| Estado              | Tipo     | Descrição                                               |
|---------------------|----------|---------------------------------------------------------|
| `ano`               | String   | Ano do relatório a ser gerado                           |
| `introConcl`       | String   | Tipo de introdução e conclusão selecionado              |
| `databases`         | Array    | Lista de instrumentos disponíveis                        |
| `instrumento`       | String   | Instrumento selecionado                                 |
| `response`          | String   | Mensagem de resposta da API                             |
| `popupVisible`      | Boolean  | Indica se o popup de resposta está visível              |
| `errorMessage`      | String   | Mensagem de erro a ser exibida                          |
| `isProcessing`      | Boolean  | Indica se a geração do relatório está em andamento      |
| `idInstrumento`     | String   | ID do instrumento gerado                                |
| `isLoadingZips`     | Boolean  | Indica se a lista de zips está sendo carregada         |
| `avaliableZips`     | Array    | Lista de zips disponíveis para download                 |

## Fluxo de Dados
1. Ao montar o componente, `fetchDatabase()` é chamado para buscar a lista de instrumentos disponíveis.
2. O usuário seleciona um instrumento, ano e tipo de introdução/conclusão.
3. Ao clicar em "Gerar relatórios", `handleSubmit()` é chamado, que valida os campos e chama `handleGenerate()`.
4. O relatório é gerado e a resposta é exibida em um popup.
5. A lista de zips disponíveis é atualizada periodicamente ou ao clicar no botão de atualização.

## Interface do Usuário
O componente exibe as seguintes seções principais:

### Seção: Informações Iniciais
- Título "Gerar relatório"
- Descrição sobre o que o relatório contém e instruções para o usuário.

### Seção: Seleção de Instrumento
- Um dropdown para selecionar o instrumento a ser utilizado.

### Seção: Escolha de Introdução e Conclusão
- Um dropdown para selecionar o tipo de introdução e conclusão.
- Um campo de entrada para o ano do relatório.

### Seção: Botões de Ação
- Botão "Gerar relatórios" para iniciar o processo de geração.
- Mensagem de erro se os campos não forem preenchidos corretamente.

### Seção: Relatórios Gerados
- Tabela com a lista de zips disponíveis
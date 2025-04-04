# Documentação do Componente GerarPdf

## Visão Geral
O componente `GerarPdf` permite aos usuários fazer upload de arquivos compactados (ZIP, RAR, etc.) contendo relatórios markdown e figuras, para gerar PDFs a partir desses arquivos. O componente também exibe os arquivos ZIP de relatórios previamente gerados, permitindo download ou exclusão.

## Funcionalidades
- Upload de arquivos compactados via interface drag-and-drop
- Validação de tipos de arquivos aceitos
- Envio de arquivos para processamento no backend
- Listagem de arquivos ZIP de relatórios previamente gerados
- Download de arquivos ZIP
- Exclusão de arquivos ZIP
- Feedback visual através de popups de status

## Dependências
- React Hooks: `useState`, `useMemo`, `useEffect`
- react-dropzone: `useDropzone` para a funcionalidade de arrastar e soltar
- react-icons: `RiFileZipFill` para ícones de arquivos
- CSS Modules: `GerarPdf.module.css`
- Utilitários: `formatFileSize` (importado de `./GerarRelatorio`)

## API Consumida
O componente consome as seguintes APIs:

### Listar PDFs disponíveis
- **Endpoint**: `${process.env.REACT_APP_BACKEND}/api/pdfs`
- **Método**: GET
- **Resposta esperada**:
  ```json
  {
    "pdfs": [
      {
        "id": string,
        "filename": string,
        "size": number
      }
    ]
  }
  ```

### Gerar PDF
- **Endpoint**: `${process.env.REACT_APP_BACKEND}/api/pdf/gerar`
- **Método**: POST
- **Corpo**: FormData contendo arquivo compactado
- **Resposta esperada**:
  ```json
  {
    "message": string,
    "id_instrumento_pdf": string
  }
  ```

### Download de PDF
- **Endpoint**: `${process.env.REACT_APP_BACKEND}/api/pdf/{idInstrumento}/download`
- **Método**: GET (via link de download)

### Deletar PDF
- **Endpoint**: `${process.env.REACT_APP_BACKEND}/api/pdf/{idInstrumento}/delete`
- **Método**: DELETE
- **Resposta esperada**:
  ```json
  {
    "message": string
  }
  ```

## Estados (States)
| Estado | Tipo | Descrição |
|--------|------|-----------|
| `popupVisible` | Boolean | Controla a visibilidade do popup de mensagens |
| `popupMessage` | String | Mensagem exibida no popup |
| `compressArchive` | Array | Armazena o arquivo compactado selecionado pelo usuário |
| `error` | String | Mensagem de erro para exibição |
| `idInstrumentoPdf` | String | ID do instrumento PDF gerado |
| `avaliablePdfs` | Array | Lista de PDFs disponíveis para download |
| `isLoadingZips` | Boolean | Indica se está carregando a lista de ZIPs |

## Fluxo de Dados
1. Ao montar o componente, `fetchPdfsAvaliable()` é chamado para buscar a lista de PDFs disponíveis
2. O usuário seleciona um arquivo via drag-and-drop ou botão de upload, atualizando o estado `compressArchive`
3. Ao clicar em "Gerar PDFs", a função `handleGeneratePDF()` é chamada:
   - Valida se um arquivo foi selecionado
   - Chama `generatePDFRequest()` para enviar o arquivo ao backend
   - Atualiza estados com base na resposta
4. A lista de PDFs pode ser atualizada manualmente via botão de atualização
5. Cada PDF listado pode ser baixado ou excluído via funções `downloadPdfZip()` e `deletePdfZip()`

## Componentes da Interface
### Área de Upload
- Dropzone para arrastar e soltar arquivos
- Suporte para vários formatos de compressão (.zip, .rar, .7z, etc.)
- Feedback visual durante o arrastar (mudança de cores de borda)
- Exibição do arquivo selecionado

### Lista de PDFs Gerados
- Tabela com informações de arquivos (nome, tamanho)
- Botões para download e exclusão
- Botão para atualizar a lista
- Estado de carregamento

### Sistema de Feedback
- Popup para exibir mensagens de sucesso ou erro
- Mensagens de erro inline para erros de validação

## Estilos
Os estilos são gerenciados através de CSS Modules no arquivo `GerarPdf.module.css`, com alguns estilos inline para componentes específicos.

## Considerações de Performance
- Usa `useMemo` para calcular estilos do dropzone apenas quando os estados relevantes mudam
- Limpeza adequada dos recursos após o download de arquivos
- Estado de carregamento para operações assíncronas

## Tratamento de Erros
- Validação da presença de arquivo antes de enviar
- Tratamento de erros nas requisições HTTP
- Exibição de mensagens de erro através de popup ou mensagem inline
- Verificação adequada de respostas da API


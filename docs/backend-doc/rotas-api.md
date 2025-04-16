# Rotas API

Aqui estará toda as rotas da API, definindo seu método e o que ela utiliza

Aqui está a tabela atualizada com uma coluna para o método HTTP:

Com base no código fornecido, aqui está a tabela atualizada com as rotas, funções e métodos:

| Rota | Função | Método | Descrição |
|------|--------|--------|-----------|
| `/api/pdf/<id_instrumento_pdf>/delete` | `delete_pdf` | DELETE | Deleta o arquivo zip contendo os PDFs de acordo com o ID do instrumento. |
| `/api/pdf/<id_instrumento_pdf>/download` | `download_pdf_zip` | GET | Realiza o download do arquivo zip contendo os PDFs gerados para o instrumento escolhido. |
| `/api/pdfs` | `list_pdfs` | GET | Lista os PDFs temporários disponíveis para download. |
| `/api/pdf/gerar` | `generate_pdf` | POST | Recebe um arquivo zip e envia para uma API em GO que realiza a geração de PDFs dos relatórios. |
| `/api/templates/download` | `download_templates_intro_concl` | GET | Realiza o download do arquivo .md contendo os templates de introdução conclusão dos tipos de instrumentos. |
| `/api/csv/importar` | `import_csv` | POST | Importa o instrumento para o backend, retornando o header do instrumento para comparação com o header correto. |
| `/api/csv/importar/confirmar` | `confirm_csv_importation` | POST | Confirma a importação do instrumento após a verificação do header pelo usuário. |
| `/api/csv/cancel/<nome_instrumento>` | `cancel_csv_importation` | DELETE | Cancela a importação removendo os arquivos que foram alocados em nosso sistema. |
| `/csv/importacao/progresso` | `get_status_csv_import` | GET | Verifica o status do instrumento que está sendo processado. |
| `/api/instrumento/listar` | `list_instrumentos` | GET | Lista os instrumentos disponíveis no banco MongoDB para o usuário. |
| `/api/relatorio/gerar` | `generate_reports` | POST | Gera relatórios para um instrumento específico, requerendo: ano do instrumento, introdução e conclusão do modal, e nome do instrumento. |
| `/api/relatorios/<id_instrumento>/download` | `download_file_zip` | GET | Realiza o download do arquivo zip contendo os relatórios gerados. |
| `/api/relatorios/<id_instrumento>/delete` | `delete_zip` | DELETE | Deleta o arquivo zip de relatórios com base no ID do instrumento. |
| `/api/limparArquvosZip` | `cleanup` | POST | Remove os arquivos zip temporários que foram gerados há mais de 24 horas. |
| `/api/relatorios/zips` | `get_avaliable_zips` | GET | Lista todos os arquivos zip de relatórios disponíveis. |
| `/api/<string:instrumento>/introducao/download` | `download_introducao_instrumentos` | GET | Faz download do arquivo markdown da introdução do instrumento que será gerado. |
| `/api/<string:instrumento>/conclusao/download` | `download_conclusao_instrumentos` | GET | Faz download do arquivo markdown da conclusão do instrumento que será gerado. |
| `/api/instrumento/etapas` | `get_steps_instrument` | POST | Lista as etapas já finalizadas de um instrumento específico. |
| `/api/instrumento/etapa/atualizar` | `update_step_instrument` | POST | Atualiza as etapas do instrumento selecionado. |
from api.services.csv_service import CsvService

class CsvController: 
    def __init__(self):
        self.csv_service = CsvService()

    # def import_csv(self, request):
    #     '''
    #     Importa o instrumento para o backend onde é retornado o header desse instrumento para poder ser feito uma comparação do header correto com o desse instrumento.
        
    #     - Rota utilizada na tela de inserção, onde é feita a requisição.
        
    #     '''
    #     global filename
    #     try:
    #         csv_file = request.files['file']
    #         filename = csv_file.filename
    #         csv_file_path = os.path.join(CSV_UPLOAD_FOLDER, csv_file.filename)
            
    #         database_name = filename.replace('.csv', '');
    #         databases_existentes = client.list_database_names();
            
    #         if database_name in databases_existentes:
    #             return jsonify({'error': 'Database already exists', 'message': 'Instrumento já existe em nosso banco de dados, confira se o instrumento já foi importado, caso não tenha, apenas altere o nome do arquivo csv.'})

    #         csv_file.save(csv_file_path)
            
    #         intro_conclusao_foldername = csv_file.filename.replace('.csv', '')
    #         intro_conclusao_diretorio = f'relatorio_componentes/{intro_conclusao_foldername}'
    #         arquivo_introducao_diretorio = f'{intro_conclusao_diretorio}/introducao'
    #         arquivo_conclusao_diretorio = f'{intro_conclusao_diretorio}/conclusao'
    #         os.makedirs(arquivo_introducao_diretorio, exist_ok=True)
    #         os.makedirs(arquivo_conclusao_diretorio, exist_ok=True)
            
    #         if 'arquivo_introducao' in request.files:
    #             intro_file = request.files['arquivo_introducao']
    #             if intro_file and intro_file.filename != '':
    #                 intro_path = os.path.join(arquivo_introducao_diretorio, intro_file.filename)
    #                 intro_file.save(intro_path)
            
    #         if 'arquivo_conclusao' in request.files:
    #             conclusao_file = request.files['arquivo_conclusao']
    #             if conclusao_file and conclusao_file.filename != '':
    #                 concl_path = os.path.join(arquivo_conclusao_diretorio, conclusao_file.filename)
    #                 conclusao_file.save(concl_path)
            
    #         try:
    #             with open(f'{csv_file_path}', newline='', encoding='utf-8') as csvFile:
    #                 reader = csv.reader(csvFile)
    #                 header = next(reader)
                
    #             return jsonify({'header': header, 'error': ''}), 200 
    #         except Exception as e:
    #             return jsonify({'header': '', 'error': f'Erro na leitura do cabeçalho: {e}'}), 400
        
    #     except Exception as e:
    #         return jsonify({'header': '', 'error': f'Erro ao tentar salvar os arquivos: {e}'}),400
              
                
    # def confirm_csv_importation():
    #     '''
    #     Confirma a importação do instrumento com a requisição vinda do usuário após ter sido conferido o header.
        
    #     - Rota utilizada na tela de inserção.
    #     '''
    #     global processing, filename
    #     ano = request.json.get('ano')
    #     modalidade = request.json.get('modalidade')
    #     print(ano, modalidade)
    #     if filename and ano and modalidade:
    #         if processing: 
    #             return jsonify({'message': 'Importação já em andamento'}), 400
            
    #         processing = True
    #         thread = Thread(target=process_csv, args=(filename, ano, modalidade))
    #         thread.start()
            
    #         print('Thread iniciada')
    #         return jsonify({'message': 'Importação iniciada com sucesso'}), 200
    #     return jsonify({'message': 'faltando nome do arquivo ou ano ou modalidade'}), 400


    # def cancel_csv_importation(nome_instrumento):
    #     try:
    #         csv_file_name = f'{nome_instrumento}.csv';
    #         csv_file_path: Path = os.path.join(CSV_UPLOAD_FOLDER, csv_file_name);
    #         os.remove(csv_file_path);
            
    #         intro_conclusao_diretorio: str = f'relatorio_componentes/{nome_instrumento}';
    #         shutil.rmtree(intro_conclusao_diretorio);
            
    #         return jsonify({'message': 'Importação cancelada com sucesso.', 'error': ''}), 200
    #     except Exception as e: 
    #         return jsonify({'error': f'Não foi possível cancelar importação: {e}'})
        
        
    # def get_status_csv_import():
    #     '''
    #     Confere o status do instrumento que está sendo processado.
        
    #     - Utilizada na tela de progresso do frontend, onde é feita a requisição nessa rota para poder ser visualizado o progresso do csv que está sendo inserido.
    #     '''
    #     global filename
    #     global processing
    #     progresso = {}
    #     if processing == True:
    #         progresso = get_progresso_insercao(filename, client)
    #         progresso = converteObjectIDToStr(progresso)  
    #         progresso = removeKeys(progresso, ['_id', 'instrumento'])
            
    #     return {'processing': processing, 'file': filename, 'progresso': progresso}, 200

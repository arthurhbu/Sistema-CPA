from flask import request, jsonify, send_file
from api.utils_api import converteObjectIDToStr, removeKeys
from src.main_controller import *
from api.gmail_api.gmail_api_controller import send_email_via_gmail_api
import os, csv
from threading import Thread
import time
import requests
from flask import Flask
import shutil

filename: str = ''
processing: bool = False

CSV_UPLOAD_FOLDER = 'src/csv/CSVs'
if not os.path.exists(CSV_UPLOAD_FOLDER):
    os.makedirs(CSV_UPLOAD_FOLDER)

def setup_routes(app: Flask, client: MongoClient): 
    """
    Configura as rotas para o backend.
    
    rotas e funções (Veja melhor detalhado na documentação do sistema):
    
        - /api/importar: importCsv, importa o instrumento para o backend onde é retornado o header desse instrumento para poder ser feito uma comparação do header correto com o desse instrumento.
        
        - /api/confirmarImportacao: confirmImportation, confirma a importação do instrumento com a requisição vinda do usuário após ter sido conferido o header.
        
        - /progresso: getStatusCsvImport, confere o status do instrumento que está sendo processado.
        
        - /api/instrumentos: listInstrumentos, lista os instrumentos disponíveis no banco MongoDB para o usuário.
        
        - /api/gerarRelatorios: generateReports, gera os relatórios para certo instrumento com a requisição feita pelo usuário, sendo necessário informações como:
            - ano do instrumento
            - Introdução e Conclusão do modal do instrumento (EAD, DISCENTES, EGRESSOS, ETC)
            - Nome do instrumento que o liga ao banco de dados com as informações dele
            
        - /api/download/<id_instrumento>: download_file_zip, baixa o arquivo zip com os relatórios gerados.
        
        - /api/limparArquvosZip: cleanup, limpa os arquivos zip temporários gerados.
        
        - /api/etapasInstrumento: getStepsInstrument, lista as etapas já finalizadas daquele instrumento de acordo com o usuário que o preenche.
        
        - /api/atualizarEtapa: updateStepInstrument, atualiza as etapas do instrumento escolhido.

    """
    
    def process_pdf_generation(file_path, id_instrumento_pdf: str):
        try: 
            url_api_pdf = os.getenv("URL_API_PDF")
            
            with open(file_path, 'rb') as zip_file_md:
                response = requests.post(url_api_pdf, files={'file': zip_file_md}, timeout=1800)
            
            if response.status_code == 200:
                
                path = os.path.join('relatorio', 'pdfs', 'pdfs_zip_temp_files', f'{id_instrumento_pdf}.zip')
                
                with open(path, 'wb') as f:
                    f.write(response.content)
       
                send_email_via_gmail_api(
                    '', 
                    'sec-cpa@uem.br', 
                    'PDFs dos relatórios.', 
                    f'Os PDFs dos relatórios foram gerados com sucesso e já estão disponíveis em nosso sistema para download. \n\nSistema CPA'
                )
                
            else:
                send_email_via_gmail_api(
                    '', 'sec-cpa@uem.br', 
                    'Ocorreu um erro ao tentar gerar os PDFs', 
                    f'Ocorreu um erro ao tentar gerar os PDFs dos relatórios.\n\n Confira o erro que ocorreu na api para gerar os PDFs: \n\n {response.text} \n {response.status_code}'
                )
                
        except requests.exceptions.Timeout:
            send_email_via_gmail_api(
                '', 
                'sec-cpa@uem.br', 
                'Ocorreu um erro ao tentar gerar os PDFs', 
                f'Ocorreu uma exceção de timeout, ou seja, o tempo limite de requisição foi excedido. \n\n Confira o sistema para entender melhor o problema'
            )          
            
        except requests.exceptions.RequestException as e:
            send_email_via_gmail_api(
                '', 'sec-cpa@uem.br', 
                'Ocorreu um erro ao tentar gerar os PDFs', 
                f'Ocorreu um erro na requisição, confira a exceção: \n\n {str(e)}'
            )      
        finally: 
            if os.path.exists(file_path):
                os.remove(file_path)


    @app.route('/api/pdf/<string:id_instrumento_pdf>/delete', methods=['DELETE'])
    def delete_pdf(id_instrumento_pdf):
        '''
        Delete o Zip contendo os PDFs de acordo com o id do instrumento.
        '''
        
        try:
            filename = f'{id_instrumento_pdf}.zip'
            path = os.path.join('relatorio', 'pdfs', 'pdfs_zip_temp_files', filename)
            
            if not os.path.exists(path):
                return jsonify({'error': 'Diretório ou arquivo não encontrado.', 'details': ''}), 404
            
            os.remove(path)
            
            return jsonify({'message': 'Arquivo deletado com sucesso.'}), 200
        
        except Exception as e:
            return jsonify({'error': f'Erro ao tentar deletar(Internal Server Error)', 'details': f'Detalhes do erro: \n {e}'}), 400
    
    
    @app.route('/api/pdf/<string:id_instrumento_pdf>/download', methods=['GET'])
    def download_pdf_zip(id_instrumento_pdf):
        '''
        Baixa o Zip contendo os PDFs gerado para o instrumento escolhido.
        '''
        
        try:
            filename = f'{id_instrumento_pdf}.zip'
            path = os.path.join('relatorio', 'pdfs', 'pdfs_zip_temp_files', filename)
            
            if not os.path.exists(path): 
                return jsonify({'error': 'Diretório não encontrado ou não existe', 'details': ''}), 404
            
            return send_file(path, as_attachment=True, download_name=filename, mimetype='application/zip')
        except Exception as e: 
            print({'error': 'Erro ao baixar o arquivo (Server Internal Errror)', 'details': f'Detalhes do erro: \n {e}'})
            return jsonify({'error': 'Erro ao baixar o arquivo (Server Internal Errror)', 'details': f'Detalhes do erro: \n {e}'}), 400
    
    
    @app.route('/api/pdfs', methods=['GET'])
    def list_pdfs():
        '''
        Lista os PDFs temporarios disponíveis para download.
        '''
        
        try:
            pdfs_directory_path = os.path.join('relatorio', 'pdfs', 'pdfs_zip_temp_files')
            
            if not os.path.exists(pdfs_directory_path):
                return jsonify({'error': 'Diretório que contém os PDFs não encontrado', 'details': ''}), 404

            pdfs = []
            
            for filename in os.listdir(pdfs_directory_path):
                filepath = os.path.join(pdfs_directory_path, filename)            
                file_stats = os.stat(filepath)
                
                pdfs.append({
                    'id': filename.replace('.zip', ''),
                    'filename': filename,
                    'size': file_stats.st_size,
                })
                
            return jsonify({'pdfs': pdfs}), 200
        except Exception as e: 
            return jsonify({'error': 'Erro ao listar PDFs.', 'details': f'Detalhes do erro: \n {e}'}), 500


    @app.route('/api/pdf/gerar', methods=['POST'])
    def generate_pdf():
        '''
        Recebe o arquivo Zip e manda para uma API feita em GO que realiza a geração do PDF dos relatórios.
        '''
        
        zip_file_md = request.files['compressArchive']
        if not zip_file_md:
            return jsonify({'error': 'Arquivo não encontrado'}), 400
        
        temp_dir = 'temp_uploads'
        os.makedirs(temp_dir, exist_ok=True)
        
        temp_file_path = os.path.join(temp_dir, zip_file_md.filename)
        
        zip_file_md.save(temp_file_path)
        
        id_instrumento_pdf = f'{zip_file_md.filename.replace(".zip", "")}_pdf'
        
        thread = Thread(target=process_pdf_generation, args=(temp_file_path, id_instrumento_pdf))     
        thread.start()
        
        return jsonify({
            'message': 'Processamento iniciado. Um email será enviado quando finalizar.',
            'id_instrumento_pdf': id_instrumento_pdf
        }), 200


    @app.route('/api/templates/download', methods=['GET'])
    def download_templates_intro_concl():
        '''
        Faz download de um arquivo .md contendo os templates de introdução e conclusão dos tipos de instrumentos.
        '''
        try:
            template_path = os.path.join('relatorio_componentes', 'templates_intro_e_concl.md')
            if not os.path.exists(template_path):
                return jsonify({'error': 'Arquivo template não encontrado'}), 404
            
            return send_file(template_path, as_attachment=True, download_name='templats_intro_e_concl.md', mimetype='text/markdown')
        except Exception as e: 
            return jsonify({'error': f'Erro ao tentar baixar o arquivo template: \n {e}'}), 400
        
        
    @app.route('/api/csv/importar', methods=["POST"])
    def import_csv():
        '''
        Importa o instrumento para o backend onde é retornado o header desse instrumento para poder ser feito uma comparação do header correto com o desse instrumento.
        
        - Rota utilizada na tela de inserção, onde é feita a requisição.
        
        '''
        global filename
        try:
            csv_file = request.files['file']
            filename = csv_file.filename
            csv_file_path = os.path.join(CSV_UPLOAD_FOLDER, csv_file.filename)
            
            database_name = filename.replace('.csv', '');
            databases_existentes = client.list_database_names();
            
            if database_name in databases_existentes:
                return jsonify({'error': 'Database already exists', 'message': 'Instrumento já existe em nosso banco de dados, confira se o instrumento já foi importado, caso não tenha, apenas altere o nome do arquivo csv.'})

            csv_file.save(csv_file_path)
            
            intro_conclusao_foldername = csv_file.filename.replace('.csv', '')
            intro_conclusao_diretorio = f'relatorio_componentes/{intro_conclusao_foldername}'
            arquivo_introducao_diretorio = f'{intro_conclusao_diretorio}/introducao'
            arquivo_conclusao_diretorio = f'{intro_conclusao_diretorio}/conclusao'
            os.makedirs(arquivo_introducao_diretorio, exist_ok=True)
            os.makedirs(arquivo_conclusao_diretorio, exist_ok=True)
            
            if 'arquivo_introducao' in request.files:
                intro_file = request.files['arquivo_introducao']
                if intro_file and intro_file.filename != '':
                    intro_path = os.path.join(arquivo_introducao_diretorio, intro_file.filename)
                    intro_file.save(intro_path)
            
            if 'arquivo_conclusao' in request.files:
                conclusao_file = request.files['arquivo_conclusao']
                if conclusao_file and conclusao_file.filename != '':
                    concl_path = os.path.join(arquivo_conclusao_diretorio, conclusao_file.filename)
                    conclusao_file.save(concl_path)
            
            try:
                with open(f'{csv_file_path}', newline='', encoding='utf-8') as csvFile:
                    reader = csv.reader(csvFile)
                    header = next(reader)
                
                return jsonify({'header': header, 'error': ''}), 200 
            except Exception as e:
                return jsonify({'header': '', 'error': f'Erro na leitura do cabeçalho: {e}'}), 400
        
        except Exception as e:
            return jsonify({'header': '', 'error': f'Erro ao tentar salvar os arquivos: {e}'}),400
              
                
    @app.route('/api/csv/importar/confirmar', methods=['POST'])
    def confirm_csv_importation():
        '''
        Confirma a importação do instrumento com a requisição vinda do usuário após ter sido conferido o header.
        
        - Rota utilizada na tela de inserção.
        '''
        global processing, filename
        ano = request.json.get('ano')
        modalidade = request.json.get('modalidade')
        print(ano, modalidade)
        if filename and ano and modalidade:
            if processing: 
                return jsonify({'message': 'Importação já em andamento'}), 400
            
            processing = True
            thread = Thread(target=process_csv, args=(filename, ano, modalidade))
            thread.start()
            
            print('Thread iniciada')
            return jsonify({'message': 'Importação iniciada com sucesso'}), 200
        return jsonify({'message': 'faltando nome do arquivo ou ano ou modalidade'}), 400


    @app.route('/api/csv/cancel/<string:nome_instrumento>', methods=['DELETE'])
    def cancel_csv_importation(nome_instrumento):
        try:
            csv_file_name = f'{nome_instrumento}.csv';
            csv_file_path: Path = os.path.join(CSV_UPLOAD_FOLDER, csv_file_name);
            os.remove(csv_file_path);
            
            intro_conclusao_diretorio: str = f'relatorio_componentes/{nome_instrumento}';
            shutil.rmtree(intro_conclusao_diretorio);
            
            return jsonify({'message': 'Importação cancelada com sucesso.', 'error': ''}), 200
        except Exception as e: 
            return jsonify({'error': f'Não foi possível cancelar importação: {e}'})
        
        
    @app.route('/api/csv/importacao/progresso', methods=['GET'])
    def get_status_csv_import():
        '''
        Confere o status do instrumento que está sendo processado.
        
        - Utilizada na tela de progresso do frontend, onde é feita a requisição nessa rota para poder ser visualizado o progresso do csv que está sendo inserido.
        '''
        global filename
        global processing
        progresso = {}
        if processing == True:
            progresso = get_progresso_insercao(filename, client)
            progresso = converteObjectIDToStr(progresso)  
            progresso = removeKeys(progresso, ['_id', 'instrumento'])
            
        return {'processing': processing, 'file': filename, 'progresso': progresso}, 200


    @app.route('/api/instrumentos', methods=['GET'])
    def list_instrumentos():
        '''
        Lista os instrumentos disponíveis no banco MongoDB para o usuário.
        
        '''
        dbs = list_databases(client)
        return jsonify(dbs)


    @app.route('/api/relatorio/gerar', methods=['POST'])
    def generate_reports(): 
        '''
        Gera os relatórios para certo instrumento com a requisição feita pelo usuário, sendo necessário informações como:
        
            - ano do instrumento
            - Introdução e Conclusão do modal do instrumento (EAD, DISCENTES, EGRESSOS, ETC)
            - Nome do instrumento que o liga ao banco de dados com as informações dele
        '''
        try: 
            
            if not request.form or 'introConcl' not in request.form:
                return jsonify({'error': 'Está faltando o tipo modal do instrumento'}), 400
            elif not request.form or 'ano' not in request.form:
                return jsonify({'error': 'Está faltando o ano do instrumento'}), 400
            elif not request.form or 'instrumento' not in request.form:
                return jsonify({'error': 'Está faltando o nome do instrumento'}), 400
            
            ano = request.form.get('ano')
            introConcl = request.form.get('introConcl')
            instrumento = request.form.get('instrumento')
            
            id_instrumento = f'{instrumento}_id'
            
            res: dict = setup_to_generate_reports(instrumento, client, int(ano), introConcl, id_instrumento)
            
            if res['Success'] == True:
                send_email_via_gmail_api('', 'sec-cpa@uem.br', 'Relatórios gerados', f'Os relatórios do instrumento {instrumento} foram gerados com sucesso.')
                                
                return jsonify({
                    'success': True, 
                    'id_instrumento': id_instrumento,
                    'download_url': f'/api/download/{id_instrumento}',
                })
            
            return jsonify({
                'error': f'Erro ao tentar gerar relatórios.'
            })
            
        except Exception as e:
            return jsonify({'error': f'Erro ao gerar relatórios (Internal Server Error): {e}'}), 400


    @app.route('/api/relatorios/<string:id_instrumento>/download', methods=['GET'])
    def download_file_zip(id_instrumento):
        
        try: 
            filename_zip = f'{id_instrumento}.zip'
            result_filepath = os.path.join('relatorio', 'markdowns', 'zip_temp_files', filename_zip)
            
            if not os.path.exists(result_filepath):
                return jsonify({'error': 'Arquivo não encontrado'}), 404
            
            return send_file(result_filepath, as_attachment=True, download_name=filename_zip, mimetype='application/zip')
        except Exception as e: 
            return jsonify({'message': f'Erro ao baixar arquivo (Internal Server Error): {e}'}), 400
    
    
    @app.route('/api/relatorios/<string:id_instrumento>/delete', methods=['DELETE'])
    def delete_zip(id_instrumento):
        
        try:
            filename_zip = f'{id_instrumento}.zip'
            result_filepath = os.path.join('relatorio', 'markdowns', 'zip_temp_files', filename_zip)
            
            if not os.path.exists(result_filepath):
                return jsonify({'error': 'Arquivo não encontrado'}), 404
            
            os.remove(result_filepath)
            
            return jsonify({'message': 'Arquivo deletado com sucesso'}), 200
        except Exception as e:
            return jsonify({'error': f'Erro ao deletar arquivo (Internal Server Error): {e}'}), 400
    
    
    @app.route('/api/limparArquvosZip', methods=['POST'])
    def cleanup():
        try:
            now = time.time()
            count = 0 
            
            path = './relatorio/markdown/arquivos_zipados_temporarios/'
            if not os.path.exists(path):
                return jsonify({'error': 'Diretório não encontrado'}), 404
            
            for filename in os.listdir('./relatorio/markdown/arquivos_zipados_temporarios/'):
                filepath = os.path.join('./relatorio/markdown/arquivos_zipados_temporarios/', filename)
                if os.path.isfile(filepath) and now - os.path.getmtime(filepath) > 24 * 3600:
                    os.remove(filepath)
                    count += 1
            
            return jsonify({'removed_files': count})
        
        except Exception as e:
            return jsonify({'error': 'Erro na limpeza de arquivos'}), 500
     
        
    @app.route('/api/relatorios/zips', methods=['GET'])
    def get_avaliable_zips():
        try:
            zip_directory = './relatorio/markdowns/zip_temp_files/'
            
            files = [f for f in os.listdir(zip_directory) if f.endswith('.zip')]
            
            zips = []
            
            for filename in files:
                file_path = os.path.join(zip_directory, filename)
                file_stats = os.stat(file_path)
                
                file_id = filename.replace('.zip', '')
                
                zips.append({
                    'id': file_id,
                    'filename': filename,
                    'size': file_stats.st_size,
                })
                
            return jsonify({'zips': zips}), 200
        except Exception as e:
            return jsonify({'error': f'Erro ao listar arquivos: {e}'}), 500
        
    
    @app.route('/api/<string:instrumento>/introducao/download', methods=['GET'])
    def download_introducao_instrumento(instrumento):
        '''
        Faz download do arquivo markdown contendo a introdução do instrumento escolhido.
        '''
        
        try:
            introducao_path: Path = os.path.join('relatorio_componentes', instrumento, 'introducao')
            
            if not os.path.exists(introducao_path):
                return jsonify({'error': 'Diretório não encontrado'}), 404
            
            arquivos: list = os.listdir(introducao_path)
            
            if not arquivos:
                return jsonify({'error': 'Diretório vazio'}), 404
            
            nome_arquivo = arquivos[0]
            full_path_intro = os.path.join(introducao_path, nome_arquivo)
            
            return send_file(full_path_intro, as_attachment=True, download_name=nome_arquivo, mimetype='text/markdown')
            
        except Exception as e: 
            return jsonify({'error': f'Erro ao baixar arquivo: {e}'}), 400
    
    
    @app.route('/api/<string:instrumento>/conclusao/download', methods=['GET'])
    def download_conclusao_instrumento(instrumento):
        '''
        Faz download do arquivo markdown contendo a introdução do instrumento escolhido.
        '''
        
        try:
            conclusao_path: Path = os.path.join('relatorio_componentes', instrumento, 'conclusao')
            
            if not os.path.exists(conclusao_path):
                return jsonify({'error': 'Diretório não encontrado'}), 404
            
            arquivos: list = os.listdir(conclusao_path)
            
            if not arquivos:
                return jsonify({'error': 'Diretório vazio'}), 404
            
            nome_arquivo = arquivos[0]
            full_path_concl = os.path.join(conclusao_path, nome_arquivo)
            
            return send_file(full_path_concl, as_attachment=True, download_name=nome_arquivo, mimetype='text/markdown')
            
        except Exception as e: 
            return jsonify({'error': f'Erro ao baixar arquivo: {e}'}), 400
    
    
    @app.route('/api/<string:instrumento>/introducao/substituir', methods=['POST'])
    def replace_introducao_instrumento(instrumento):
        try: 
            intro_file = request.files['arquivo_introducao']
            intro_filename = intro_file.filename
            
            introducao_path = os.path.join('relatorio_componentes', instrumento, 'introducao')
            
            if not os.path.exists(introducao_path):
                return jsonify({'error': 'Diretório não encontrado'}), 404
            
            arquivos: list = os.listdir(introducao_path)
            full_path_intro = os.path.join(introducao_path, intro_filename)
            
            if not arquivos:
                intro_file.save(full_path_intro)
                return jsonify({'message': 'Introdução substituida com sucesso.'}), 200
            
            os.remove(os.path.join(introducao_path, arquivos[0]))
            intro_file.save(full_path_intro)
            
            return jsonify({'message': 'Introdução substituída com sucesso.'}), 200
        except Exception as e: 
            return jsonify({'error': f'Erro ao substituir arquivo: {e}'}), 400
        
        
    @app.route('/api/<string:instrumento>/conclusao/substituir', methods=['POST'])
    def replace_conclusao_instrumento(instrumento):
        try: 
            concl_file = request.files['arquivo_conclusao']
            concl_filename = concl_file.filename
            
            conclusao_path: Path = os.path.join('relatorio_componentes', instrumento, 'conclusao')
            
            if not os.path.exists(conclusao_path):
                return jsonify({'error': 'Diretório não encontrado'}), 404
            
            arquivos: list = os.listdir(conclusao_path)
            
            full_path_concl = os.path.join(conclusao_path, concl_filename)
            
            if not arquivos:
                concl_file.save(full_path_concl)
                return jsonify({'message': 'Conclusão substituida com sucesso.'}), 200
            
            os.remove(os.path.join(conclusao_path, arquivos[0]))
            concl_file.save(full_path_concl)
            
            return jsonify({'message': 'Conclusão substituída com sucesso.'}), 200
        except Exception as e: 
            return jsonify({'error': f'Erro ao substituir arquivo: {e}'}), 400
        
        
    @app.route('/api/instrumento/etapas', methods=['POST'])
    def get_steps_instrument():
        '''
        Lista as etapas já finalizadas daquele instrumento de acordo com o usuário que o preenche.
        '''
        data = request.json
        database = data.get('instrumento')
        
        if not database:
            return {'error': 'Instrumento não fornecido'}, 400
        
        etapas = get_etapas(database, client)
        if not etapas:
            return {'error': 'Não foi possível encontrar etapas para o instrumento'}, 404
        
        etapas = converteObjectIDToStr(etapas)
        etapas = removeKeys(etapas, ['_id'])
        
        return jsonify({'etapas': etapas}), 200


    @app.route('/api/instrumento/etapa/atualizar', methods=['POST'])
    def update_step_instrument():
        '''
        Atualiza as etapas do instrumento escolhido.
        '''
        data = request.get_json()
        database = data.get('instrumento')
        etapaId = data.get('etapa')
        etapaValor = data.get('novoValor')
        
        resultado = atualiza_etapa(database, etapaId, etapaValor, client)
        
        if resultado == 'Sucesso':
            return {'message': 'Etapa atualizada com sucesso'}, 200
        
        return {'error': resultado}, 400
    
    
    def process_csv(filename, ano, modalidade):
        global processing
        try:
            with app.app_context():
                response = inserir_e_processar_csv(int(ano), filename, modalidade, client)
                print(f'Processamento concluido: {response}')
        except Exception as e:
            print(f'Erro no processamento: {e}')
        finally: 
            time.sleep(2)
            send_email_via_gmail_api('', 'sec-cpa@uem.br', 'Processamento de CSV concluído', f'O processamento do CSV {filename} foi concluído com sucesso. \nO instrumento estará disponível para ser gerado os relatórios markdowns \n\nSISTEMA CPA.')
            processing = False
            
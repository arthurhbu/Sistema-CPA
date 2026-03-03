import os
import csv
from app import import_state
from threading import Thread
from api.utils.error_handlers import *
from src.main_controller import inserir_e_processar_csv
import logging
import time
from api.gmail_api.gmail_api_controller import send_email_via_gmail_api
from api.gmail_api.error_email_builder import ErrorEmailBuilder
import shutil
from api.utils_api import converteObjectIDToStr, removeKeys, normalize_database_name
from src.main_controller import get_progresso_insercao


logger = logging.getLogger(__name__)

class CsvService: 
    
    def __init__(self):
        self.CSV_UPLOAD_FOLDER = 'src/csv/CSVs'

    
    def process_csv_import(self, csv_file, intro_file, concl_file, mongo_client):
        '''Insere o arquivo CSV e introdução e conclusão no sistema'''
        try:
            database_name: str = normalize_database_name(csv_file.filename)
            databases_existentes = mongo_client.list_database_names();
            
            if database_name in databases_existentes:
                return {
                    'error': 'Database already exists', 
                    'message': 'Instrumento já existe em nosso banco de dados, confira se o instrumento já foi importado, caso não tenha, apenas altere o nome do arquivo csv.'
                }
                
            csv_file_path = os.path.join(self.CSV_UPLOAD_FOLDER, csv_file.filename)
            csv_file.save(csv_file_path)
            
            self._setup_intro_concl_directories(csv_file.filename, intro_file, concl_file)
           
            try:
                with open(f'{csv_file_path}', newline='', encoding='utf-8') as csvFile:
                    reader = csv.reader(csvFile)
                    header = next(reader)
                
                return {'header': header, 'error': ''}
            except Exception as e:
                logger.exception('Erro na leitura de cabeçalho')
                return {'header': '', 'error': f'Erro na leitura do cabeçalho: {e}'}
        except Exception as e:
            logger.exception('Erro ao inserir arquivos')
            return {'header': '', 'error': f'Erro ao inserir arquivos: {e}'}
            
            
    def _setup_intro_concl_directories(self, csv_filename, intro_file, concl_file):
        """Configura os diretórios de introdução e conclusão."""
        
        intro_conclusao_foldername = normalize_database_name(csv_filename)
        
        intro_conclusao_diretorio = f'relatorio_componentes/{intro_conclusao_foldername}'
        
        arquivo_introducao_diretorio = f'{intro_conclusao_diretorio}/introducao'
        arquivo_conclusao_diretorio = f'{intro_conclusao_diretorio}/conclusao'
        
        os.makedirs(arquivo_introducao_diretorio, exist_ok=True)
        os.makedirs(arquivo_conclusao_diretorio, exist_ok=True)
        
        if intro_file and intro_file.filename != '':
            intro_file.save(os.path.join(arquivo_introducao_diretorio, intro_file.filename))
        
        if concl_file and concl_file.filename != '':
            concl_file.save(os.path.join(arquivo_conclusao_diretorio, concl_file.filename))
            
            
    def start_csv_processing(self, csv_filename, ano, modalidade, mongo_client):
        try:
            import_state.processing = True
            
            thread = Thread(target=self._process_csv_thread, args=(csv_filename, ano, modalidade, mongo_client))
            thread.start()
            
            return "Importação iniciada com sucesso!", True
        except Exception as e: 
            logger.exception('Ocorreu um erro ao tentar processar CSV')
            return error_response('Ocorreu um erro ao tentar processar CSV', 400, str(e)), False

        
    def _process_csv_thread(self, csv_filename, ano, modalidade, mongo_client):
        try:
            erro = inserir_e_processar_csv(int(ano), csv_filename, modalidade, mongo_client)
        except Exception as e:
            logger.exception("Errro no processamento")
        finally: 
            if erro == 'False':
                database_name = normalize_database_name(csv_filename)
                mongo_client.drop_database(database_name)
                import_state.processing = False
                logger.error(f'Erro ao processar CSV: {erro}')
                return
            time.sleep(2)
            # Usar o novo sistema de notificação estruturada
            email_data = ErrorEmailBuilder.build_success_notification(
                instrumento=csv_filename,
                operation='Processamento de CSV',
                context={'status': 'Disponivel para geracao de relatorios'}
            )
            send_email_via_gmail_api('', 'sec-cpa@uem.br', email_data['subject'], email_data['body'])
            import_state.processing = False
            
            
    def cancel_csv_importation(self, nome_instrumento):
        try:
            normalized_name = normalize_database_name(nome_instrumento)
            csv_file_name = f'{normalized_name}.csv'
            csv_file_path = os.path.join(self.CSV_UPLOAD_FOLDER, csv_file_name);
            
            if os.path.exists(csv_file_path):
                os.remove(csv_file_path)
            
            intro_conclusao_diretorio: str = f'relatorio_componentes/{normalized_name}'
            if os.path.exists(intro_conclusao_diretorio):
                shutil.rmtree(intro_conclusao_diretorio)
            
            return 'Importação cancelada com sucesso.', True
        except Exception as e: 
            logger.exception("Ocorreu um erro ao tentar cancelar importação")
            return f'Não foi possível cancelar importação: {e}', False
        
        
    def get_import_status(self, filename, processing, mongo_client):
        try: 
            progresso = {}
            if processing:
                progresso = get_progresso_insercao(filename, mongo_client)
                progresso = converteObjectIDToStr(progresso)  
                progresso = removeKeys(progresso, ['_id', 'instrumento'])
                
            return {'processing': processing, 'file': filename, 'progresso': progresso}, True
        except Exception as e:
            logger.exception('Ocorreu um erro ao tentar verificar status da importação')
            return f'Ocorreu um erro ao tentar verificar status da importação: {e}', False
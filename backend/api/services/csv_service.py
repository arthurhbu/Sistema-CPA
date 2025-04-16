import os
import csv
from app import import_state
from threading import Thread
from api.utils.error_handlers import *
from src.main_controller import inserir_e_processar_csv
import logging
import time
from api.gmail_api.gmail_api_controller import send_email_via_gmail_api
import shutil
from api.utils_api import converteObjectIDToStr, removeKeys
from src.main_controller import get_progresso_insercao


logger = logging.getLogger(__name__)

class CsvService: 
    
    def __init__(self):
        self.CSV_UPLOAD_FOLDER = 'src/csv/CSVs'

    
    def process_csv_import(self, csv_file, intro_file, concl_file, mongo_client):
        '''Insere o arquivo CSV e introdução e conclusão no sistema'''
        try:
            database_name: str = csv_file.filename.replace('.csv', '');
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
        
        intro_conclusao_foldername = csv_filename.replace('.csv', '')
        
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
            inserir_e_processar_csv(int(ano), csv_filename, modalidade, mongo_client)
        except Exception as e:
            logger.exception("Errro no processamento")
        finally: 
            time.sleep(2)
            send_email_via_gmail_api('', 'sec-cpa@uem.br', 'Processamento de CSV concluído', f'O processamento do CSV {csv_filename} foi concluído com sucesso. \nO instrumento estará disponível para ser gerado os relatórios markdowns \n\nSISTEMA CPA.')
            import_state.processing = False
            
            
    def cancel_csv_importation(self, nome_instrumento):
        try:
            csv_file_name = f'{nome_instrumento}.csv';
            csv_file_path = os.path.join(self.CSV_UPLOAD_FOLDER, csv_file_name);
            os.remove(csv_file_path);
            
            intro_conclusao_diretorio: str = f'relatorio_componentes/{nome_instrumento}';
            shutil.rmtree(intro_conclusao_diretorio);
            
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
                print(progresso)
                
            return {'processing': processing, 'file': filename, 'progresso': progresso}, True
        except Exception as e:
            logger.exception('Ocorreu um erro ao tentar verificar status da importação')
            return f'Ocorreu um erro ao tentar verificar status da importação: {e}', False
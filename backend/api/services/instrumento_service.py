import logging
import os 
from api.utils.error_handlers import *
from src.main_controller import get_etapas, atualiza_etapa
from api.utils_api import *

logger = logging.getLogger(__name__)

class InstrumentoService:
    
    def list_instrumentos(self, mongo_client):
        try:
            databases: list[str] = mongo_client.list_database_names()
            users_database: list[str] = [db for db in databases if db not in ['admin', 'config', 'local']] 
            
            return users_database, True
        except Exception as e:
            logger.exception('Erro ao tentar listar os databases disponíveis')
            return f'Erro ao tentar listar os databases disponíveis: {e}', False
        
    def download_introducao_instrumento(self, instrumento: str): 
        try:
            introducao_path = os.path.join('relatorio_componentes', instrumento, 'introducao')
            
            if not os.path.exists(introducao_path):
                return not_found_error('Diretório'), False
            
            arquivos: list = os.listdir(introducao_path)
            
            if not arquivos:
                return not_found_error('Arquivo'), False
            
            nome_arquivo = arquivos[0]
            full_path_intro = os.path.join(introducao_path, nome_arquivo)
            
            return {'full_path_intro': full_path_intro, 'nome_arquivo': nome_arquivo}, True
            
        except Exception as e: 
            logger.exception('Erro ao baixar arquivo')
            return error_response(f'Erro ao baixar arquivo',details=e), False
        
    def download_conclusao_instrumento(self, instrumento: str):
        try:
            conclusao_path = os.path.join('relatorio_componentes', instrumento, 'conclusao')
            
            if not os.path.exists(conclusao_path):
                return not_found_error('Diretório'), False
            
            arquivos: list = os.listdir(conclusao_path)
            
            if not arquivos:
                return not_found_error('Arquivo'), False
            
            nome_arquivo = arquivos[0]
            full_path_concl = os.path.join(conclusao_path, nome_arquivo)
            
            return {'full_path_concl': full_path_concl, 'nome_arquivo': nome_arquivo}, True
            
        except Exception as e: 
            logger.exception('Erro ao baixar arquivo')
            return error_response(f'Erro ao baixar arquivo',details=e), False
        
    def replace_introducao_instrumento(self, instrumento: str, intro_file):
        try: 
            intro_filename = intro_file.filename
            
            introducao_path = os.path.join('relatorio_componentes', instrumento, 'introducao')
            
            if not os.path.exists(introducao_path):
                return not_found_error('Diretório'), False
            
            arquivos: list = os.listdir(introducao_path)
            full_path_intro = os.path.join(introducao_path, intro_filename)
            
            if not arquivos:
                intro_file.save(full_path_intro)
                return 'Introdução substituida com sucesso.', True
            
            os.remove(os.path.join(introducao_path, arquivos[0]))
            intro_file.save(full_path_intro)
            
            return 'Introdução substituída com sucesso.', True
        except Exception as e: 
            logger.exception('Erro ao substituir arquivo')
            return error_response('Erro ao substituir arquivo',details=e), False
        
    def replace_conclusao_instrumento(self, instrumento: str, concl_file):
        try: 
            concl_filename = concl_file.filename
            
            conclusao_path = os.path.join('relatorio_componentes', instrumento, 'conclusao')
            
            if not os.path.exists(conclusao_path):
                return not_found_error('Diretório'), False
            
            arquivos: list = os.listdir(conclusao_path)
            full_path_concl = os.path.join(conclusao_path, concl_filename)
            
            if not arquivos:
                concl_file.save(full_path_concl)
                return 'Conclusão substituida com sucesso.', True
            
            os.remove(os.path.join(conclusao_path, arquivos[0]))
            concl_file.save(full_path_concl)
            
            return 'Conclusão substituída com sucesso.', True
        except Exception as e: 
            logger.exception('Erro ao substituir arquivo')
            return error_response('Erro ao substituir arquivo',details=e), False
        
    def get_steps_instrument(self, database: str, mongo_client):
        try:
            etapas = get_etapas(database, mongo_client)
            
            if not etapas:
                return not_found_error('Instrumento'), False
            
            etapas = converteObjectIDToStr(etapas)
            etapas = removeKeys(etapas, ['_id'])
            
            return {'etapas': etapas}, True
    
        except Exception as e:
            logger.exception('Ocorreu um erro ao tentar pegar as etapas do instrumento')
            return error_response('Ocorreu um erro ao tentar pegar as etapas',details=e), False
        
    def update_step_instrument(self, database: str, etapa_id: dict, novo_valor_etapa: bool, mongo_client):
        resultado = atualiza_etapa(database, etapa_id, novo_valor_etapa, mongo_client)
        
        if resultado == 'Sucesso':
            return 'Etapa atualizada com sucesso', True
        
        return resultado, False
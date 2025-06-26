import logging
import os 
from api.utils.error_handlers import *
from src.main_controller import get_etapas, atualiza_etapa
from api.utils_api import *
from src.data_generator.generator_controller import generate_graph_table_report

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
        
    def list_instrumentos_with_status(self, mongo_client):
        '''
            Informações que serão retornadas:
            - Data de criação do instrumento
            - Nome do instrumento
            - Total de documentos
            - Documentos processados
            - Documentos não processados
            - Percentual de documentos processados
            - Percentual de documentos não processados
        '''
        
        try:
            databases: list[str] = mongo_client.list_database_names()
            instrumentos: list[str] = [db for db in databases if db not in ['admin', 'config', 'local']] 
            result = {}
            
            for instrumento in instrumentos:
                collection_instrumento = mongo_client[instrumento]['instrumento']
                progresso = mongo_client[instrumento]['progresso_da_insercao']
                progresso_document = progresso.find_one({})
                importado = progresso_document['Importado']
                gerado = progresso_document['Gerado']
                total_documentos = collection_instrumento.count_documents({})
                documentos_processados = collection_instrumento.count_documents({'processado': True})
                documentos_nao_processados = total_documentos - documentos_processados
                percentual_processados = (documentos_processados / total_documentos) * 100 if total_documentos > 0 else 0
                percentual_nao_processados = (documentos_nao_processados / total_documentos) * 100 if total_documentos > 0 else 0
                primeiro_documento = collection_instrumento.find_one({}, sort=[('_id', 1)])
                data_criacao = primeiro_documento['_id'].generation_time if primeiro_documento else None
                
                status_info = {
                    'nome_instrumento': instrumento,
                    'data_criacao': data_criacao,
                    'importado': importado,
                    'gerado': gerado,
                    'total_documentos': total_documentos,
                    'documentos_processados': documentos_processados,
                    'documentos_nao_processados': documentos_nao_processados,
                    'percentual_processados': round(percentual_processados, 2),
                    'percentual_nao_processados': round(percentual_nao_processados, 2)
                }
                result[instrumento] = status_info
            
            return result, True
            
        except Exception as e:
            logger.exception('Erro ao listar status dos instrumentos')
            return error_response('Erro ao listar status dos instrumentos', details=e), False
        
        
    def continuar_geracao(self, nome_instrumento, mongo_client):
        try:
            logger.info(f'Iniciando continuação da geração do instrumento: {nome_instrumento}')
            
            if not nome_instrumento:
                return 'Nome do instrumento não fornecido', False
                
            database = mongo_client[nome_instrumento]
            instrumento_collection = database['instrumento']
            progresso_collection = database['progresso_da_insercao']
            
            logger.info('Chamando generate_graph_table_report')
            resultado = generate_graph_table_report(mongo_client, nome_instrumento, instrumento_collection)
            logger.info(f'Resultado do processamento: {resultado}')
            
            if resultado == 'Finalizado':
                logger.info('Processamento concluído com sucesso')
                progresso_collection.update_one({'Gerado': False}, {'$set': {'Gerado': True}})
                return 'Processamento concluído com sucesso', True
            else:
                logger.error(f'Erro no processamento: {resultado}')
                return str(resultado), False
                
        except Exception as e:
            logger.exception('Erro ao continuar a geração do instrumento')
            return f'Erro ao continuar a geração do instrumento: {str(e)}', False
        
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
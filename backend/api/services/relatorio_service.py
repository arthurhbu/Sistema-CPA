import os 
from flask import jsonify, send_file
from api.utils.error_handlers import *
import logging
from src.main_controller import setup_to_generate_reports
from api.gmail_api.gmail_api_controller import send_email_via_gmail_api

logger = logging.getLogger(__name__)

class RelatorioService:
    
    def upload_templates(self, arquivo_template):
        try:
            template_path = os.path.join('relatorio_componentes', 'templates_intro_e_concl.md')
            
            if not os.path.exists(template_path):
                return not_found_error('Template'), False
            
            arquivo_template.save(template_path)
            
            return {'message': 'Template atualizado com sucesso'}, True
        except Exception as e: 
            logger.exception('Erro ao tentar atualizar o arquivo template')
            return error_response('Erro ao tentar atualizar o arquivo template', details=f'Detalhes do erro: \n {e}'), False
    
    def download_templates_intro_concl(self,):
        try:
            template_path = os.path.join('relatorio_componentes', 'templates_intro_e_concl.md')
            
            if not os.path.exists(template_path):
                return not_found_error('Template'), False
            
            return {'template_path': template_path, 'download_name': 'templates_intro_e_concl.md'}, True
        except Exception as e: 
            logger.exception('Erro ao tentar baixar o arquivo template')
            return error_response('Erro ao tentar baixar o arquivo template', details=f'Detalhes do erro: \n {e}'), False
        
    def generate_reports(self, instrumento, mongo_client, ano, modalidade, id_instrumento):
        
        try:
            res: dict = setup_to_generate_reports(instrumento, mongo_client, ano, modalidade, id_instrumento)
            
            if res['Success'] == True:
                send_email_via_gmail_api('', 'sec-cpa@uem.br', 'Relatórios gerados', f'Os relatórios do instrumento {instrumento} foram gerados com sucesso.')
                                
                return jsonify({
                    'success': True, 
                    'id_instrumento': id_instrumento,
                    'download_url': f'/api/{id_instrumento}/download',
                })
            
            return error_response('Erro ao tentar gerar relatórios', details=res['error'])
        except Exception as e: 
            logger.exception('Ocorre um erro inesperado')
            return error_response('Ocorreu um erro inesperado', details=str(e))
        
    def download_file_zip(self, filename_zip):
        try: 
            result_filepath = os.path.join('relatorio', 'markdowns', 'zip_temp_files', filename_zip)
            
            if not os.path.exists(result_filepath):
                return not_found_error('Arquivo'), False
            
            return {'result_filepath': result_filepath, 'download_name': filename_zip}, True
        except Exception as e: 
            logger.exception('Erro ao baixar relatorios zip')
            return error_response('Erro ao baixar relatorios zip', details=f'Detalhes do erro: \n {e}'), False
        
        
    def delete_zip(self, filename_zip):
        try:
            result_filepath = os.path.join('relatorio', 'markdowns', 'zip_temp_files', filename_zip)
            
            if not os.path.exists(result_filepath):
                return not_found_error('Arquivo'), False
            
            os.remove(result_filepath)
            
            return 'Arquivo deletado com sucesso', True
        except Exception as e:
            logger.exception('Erro ao deletar relatorios zip')
            return error_response('Erro ao deletar relatorios zip', details=f'Detalhes do erro: \n {e}'), False
        
        
    def get_avaliable_zips(self,):
        try:
            zip_directory = os.path.join('relatorio', 'markdowns', 'zip_temp_files')
            
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
            return {'zips': zips}, True
        except Exception as e:
            logger.exception('Erro ao listar arquivos')
            return error_response('Erro ao listar arquivos', details=f'Detalhes do erro: \n {e}'), False
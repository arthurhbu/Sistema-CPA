import os 
from flask import jsonify
from api.utils.error_handlers import *
import logging
import requests
from api.gmail_api.gmail_api_controller import send_email_via_gmail_api
from api.gmail_api.error_email_builder import ErrorEmailBuilder
from threading import Thread

logger = logging.getLogger(__name__)

class PdfService:
    
    def delete_pdfs_zip(self, pdf_filename: str): 
        try:
            path = os.path.join('relatorio', 'pdfs', 'pdfs_zip_temp_files', pdf_filename)
            
            if not os.path.exists(path):
                return not_found_error('Diretório', path), False
            
            os.remove(path)
            
            return 'Arquivo deletado com sucesso', True
        
        except Exception as e:
            logger.exception('Erro ao tentar deletar pdfs')
            return error_response('Erro ao tentar deletar pdfs', details=f'Detalhes do erro: \n {e}'), False 
        
    def download_pdfs_zip(self, pdf_filename: str):
        try:
            path = os.path.join('relatorio', 'pdfs', 'pdfs_zip_temp_files', pdf_filename)
            
            if not os.path.exists(path): 
                return not_found_error('Diretório', path), False
            
            return {'path_pdf_zip': path, 'nome_zip': pdf_filename}, True
        
        except Exception as e: 
            logger.exception('Erro ao tentar baixar zip dos pdfs')
            return error_response('Erro ao tentar baixar pdfs', details=f'Detalhes do erro \n {e}'), False

        
    def list_pdfs(self):
        try:
            pdfs_directory_path = os.path.join('relatorio', 'pdfs', 'pdfs_zip_temp_files')
            
            if not os.path.exists(pdfs_directory_path):
                return not_found_error('Diretório', pdfs_directory_path), False

            pdfs = []
            
            for filename in os.listdir(pdfs_directory_path):
                filepath = os.path.join(pdfs_directory_path, filename)            
                file_stats = os.stat(filepath)
                
                pdfs.append({
                    'id': filename.replace('.zip', ''),
                    'filename': filename,
                    'size': file_stats.st_size,
                })
                
            return {'pdfs': pdfs}, True
        except Exception as e: 
            logger.exception('Erro ao listar PDFs')
            return error_response('Erro ao listar PDFs', status_code=500, details=f'Detalhes do erro: \n {e}'), False
    
    def generate_pdf(self, zip_file_md):
        
        temp_dir = 'temp_uploads'
        os.makedirs(temp_dir, exist_ok=True)
        
        temp_file_path = os.path.join(temp_dir, zip_file_md.filename)
        
        zip_file_md.save(temp_file_path)
        
        id_instrumento_pdf = f'{zip_file_md.filename.replace(".zip", "")}_pdf'
        
        thread = Thread(target=self._process_pdf_generation_thread, args=(temp_file_path, id_instrumento_pdf))     
        thread.start()
        
        return jsonify({
            'message': 'Processamento iniciado. Um email será enviado quando finalizar.',
            'id_instrumento_pdf': id_instrumento_pdf
        }), 200
        
    def _process_pdf_generation_thread(self, file_path, id_instrumento_pdf):
        try: 
            os.makedirs(os.path.join('relatorio', 'pdfs', 'pdfs_zip_temp_files'), exist_ok=True)
            url_api_pdf = os.getenv("URL_API_PDF")
            
            with open(file_path, 'rb') as zip_file_md:
                response = requests.post(url_api_pdf, files={'file': zip_file_md}, timeout=1800)
            
            if response.status_code == 200:
                
                path = os.path.join('relatorio', 'pdfs', 'pdfs_zip_temp_files', f'{id_instrumento_pdf}.zip')
                
                with open(path, 'wb') as f:
                    f.write(response.content)
       
                # Usar o novo sistema de notificação estruturada
                email_data = ErrorEmailBuilder.build_success_notification(
                    instrumento=id_instrumento_pdf.replace('_pdf', ''),
                    operation='Geracao de PDFs',
                    context={'status': 'Disponivel para download', 'arquivo': f'{id_instrumento_pdf}.zip'}
                )
                send_email_via_gmail_api('', 'sec-cpa@uem.br', email_data['subject'], email_data['body'])
                
            else:
                # Usar o novo sistema de emails estruturados
                email_data = ErrorEmailBuilder.build_pdf_generation_error(
                    instrumento=id_instrumento_pdf.replace('_pdf', ''),
                    error_details=f"Erro HTTP {response.status_code}: {response.text}",
                    context={'status_code': response.status_code}
                )
                send_email_via_gmail_api('', 'sec-cpa@uem.br', email_data['subject'], email_data['body'])
                
        except requests.exceptions.Timeout:
            # Usar o novo sistema de emails estruturados
            email_data = ErrorEmailBuilder.build_pdf_generation_error(
                instrumento=id_instrumento_pdf.replace('_pdf', ''),
                error_details="Timeout na requisicao - tempo limite excedido",
                context={'timeout': True}
            )
            send_email_via_gmail_api('', 'sec-cpa@uem.br', email_data['subject'], email_data['body'])          
            
        except requests.exceptions.RequestException as e:
            # Usar o novo sistema de emails estruturados
            email_data = ErrorEmailBuilder.build_pdf_generation_error(
                instrumento=id_instrumento_pdf.replace('_pdf', ''),
                error_details=f"Erro na requisicao: {str(e)}",
                context={'tipo_erro': 'RequestException'}
            )
            send_email_via_gmail_api('', 'sec-cpa@uem.br', email_data['subject'], email_data['body'])      
        finally: 
            if os.path.exists(file_path):
                os.remove(file_path)
        
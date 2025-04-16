import os 
from flask import jsonify
from api.utils.error_handlers import *
import logging
import requests
from api.gmail_api.gmail_api_controller import send_email_via_gmail_api
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
                
            return {'pdfs': pdfs}
        except Exception as e: 
            logger.exception('Erro ao listar PDFs')
            return error_response('Erro ao listar PDFs', status_code=500, details=f'Detalhes do erro: \n {e}')
    
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
        
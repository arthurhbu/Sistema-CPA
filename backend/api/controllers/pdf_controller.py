from api.services.pdf_service import PdfService
from flask import jsonify, send_file
import logging

logger = logging.getLogger(__name__)

class PdfController:
    def __init__(self):
        self.pdf_service = PdfService()
        
    def delete_pdfs_zip(self, pdf_filename: str):
        try:
            result, success = self.pdf_service.delete_pdfs_zip(pdf_filename)
            
            if success:
                return jsonify({'message': result})
            
            return result
        except Exception as e: 
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
    
    def download_pdfs_zip(self, pdf_filename: str):
        try:
            result, success = self.pdf_service.download_pdfs_zip(pdf_filename)
            
            if not success: 
                return result
            
            return send_file(result['path_pdf_zip'], as_attachment=True, download_name=result['nome_zip'], mimetype='text/markdown')
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
        
    def list_pdfs(self):
        try:
            result, success = self.pdf_service.list_pdfs()
            
            if not success: 
                return result
            
            return jsonify({'pdfs': result['pdfs']}), 200
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
    
    def generate_pdf(self, zip_file_md):
        try:
            result = self.pdf_service.generate_pdf(zip_file_md)
            return result
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
        
        
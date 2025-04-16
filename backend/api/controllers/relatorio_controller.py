from api.services.relatorio_service import RelatorioService
from flask import send_file
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

class RelatorioController:
    def __init__(self):
        self.relatorio_service = RelatorioService()    
        
    def download_templates_intro_concl(self,):
        try:
            result, success = self.relatorio_service.download_templates_intro_concl()
            
            if not success:
                return result
            
            return send_file(result['template_path'], as_attachment=True, download_name=result['download_name'], mimetype='text/markdown')
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
        
    def generate_reports(self, instrumento, mongo_client, ano, modalidade, id_instrumento):
        try:
            result = self.relatorio_service.generate_reports(instrumento, mongo_client, ano, modalidade, id_instrumento)
            
            return result
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
        
        
    def download_file_zip(self, filename_zip):
        try:
            result, success = self.relatorio_service.download_file_zip(filename_zip)
            
            if not success:
                return result
            
            return send_file(result['result_filepath'], as_attachment=True, download_name=result['download_name'], mimetype='text/markdown')
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
        
    def delete_zip(self, filename_zip):
        try:
            result, success = self.relatorio_service.delete_zip(filename_zip)
            
            if not success: 
                return result
            
            return jsonify({'message': result}), 200
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
        
        
    def get_avaliable_zips(self):
        try:
            print('jdisqJIDFSAJIOFSAJIodfjiosadfjioasdjiosakopdASOKPDkopjksopadjiopsaJPDOISApkodksaopDKOPSakodpsaKOP')
            result, success = self.relatorio_service.get_avaliable_zips()
            
            if not success:
                return result
            
            return jsonify({'zips': result['zips']}), 200
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
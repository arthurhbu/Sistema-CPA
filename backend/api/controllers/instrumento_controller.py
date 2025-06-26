from api.services.instrumento_service import InstrumentoService
from flask import jsonify
from flask import send_file
import logging

logger = logging.getLogger(__name__)

class InstrumentoController:
    def __init__(self):
        self.instrumento_service = InstrumentoService()
        
    def list_instrumentos(self, mongo_client):
        try:
            result, success = self.instrumento_service.list_instrumentos(mongo_client)
            
            if not success:
                return jsonify({'erro': result}), 400
            
            return jsonify(result)
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
    
    def list_instrumentos_with_status(self, mongo_client):
        try:
            result, success = self.instrumento_service.list_instrumentos_with_status(mongo_client)
            
            if not success:
                return jsonify({'erro': result}), 400
            
            return jsonify(result)
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
        
    def continuar_geracao(self, nome_instrumento, mongo_client):
        try:
            result, success = self.instrumento_service.continuar_geracao(nome_instrumento, mongo_client)
            
            if not success:
                return jsonify({'erro': result}), 400
            
            return jsonify(result)
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
        
    def download_introducao_instrumento(self, instrumento: str):
        try:
            result, success = self.instrumento_service.download_introducao_instrumento(instrumento)
            
            if not success:
                return result
            
            return send_file(result['full_path_intro'], as_attachment=True, download_name=result['nome_arquivo'], mimetype='text/markdown')
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
    
    def download_conclusao_instrumento(self, instrumento: str):
        try:
            result, success = self.instrumento_service.download_conclusao_instrumento(instrumento)
            
            if not success:
                return result
            
            return send_file(result['full_path_concl'], as_attachment=True, download_name=result['nome_arquivo'], mimetype='text/markdown')
        except Exception as e: 
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500

    
    def replace_introducao_instrumento(self, instrumento: str, intro_file):
        try:
            result, success = self.instrumento_service.replace_introducao_instrumento(instrumento, intro_file)
            
            if not success: 
                return result
            
            return jsonify({'message': result}), 200
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
    
    def replace_conclusao_instrumento(self, instrumento: str, concl_file):
        try:
            result, success = self.instrumento_service.replace_conclusao_instrumento(instrumento, concl_file)
            
            if not success: 
                return result
            
            return jsonify({'message': result}), 200
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
    
    def get_steps_instrument(self, database: str, mongo_client):
        try: 
            result, success = self.instrumento_service.get_steps_instrument(database, mongo_client)
            
            if not success:
                return result
            
            return jsonify({'etapas': result['etapas']}), 200
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
    
    def update_step_instrument(self, database: str, etapa_id: dict, novo_valor_etapa: bool, mongo_client):
        try:
            result, success = self.instrumento_service.update_step_instrument(database, etapa_id, novo_valor_etapa, mongo_client)
            
            if not success: 
                return result
            
            return jsonify({'message': result}), 200
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
        
        
        
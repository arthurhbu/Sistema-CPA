from api.services.csv_service import CsvService
from api.utils.error_handlers import *
from flask import jsonify
import logging

logger = logging.getLogger(__name__)

class CsvController: 
    def __init__(self):
        self.csv_service = CsvService()

    def import_csv(self, csv_file, intro_file, concl_file, mongo_client):
        '''
        Importa o instrumento para o backend onde é retornado o header desse instrumento para poder ser feito uma comparação do header correto com o desse instrumento.
        
        - Rota utilizada na tela de inserção, onde é feita a requisição.
        
        '''
        try:
            result = self.csv_service.process_csv_import(
                csv_file, 
                intro_file, 
                concl_file, 
                mongo_client
            )
            if result['error'] == '':
                return jsonify(result), 200
            
            return jsonify(result), 400
            
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'header': '', 'error': f'Erro interno do servidor: {e}'}), 500
              
                
    def confirm_csv_importation(self, csv_filename, ano, modalidade, mongo_client):
        '''
        Confirma a importação do instrumento com a requisição vinda do usuário após ter sido conferido o header.
        
        - Rota utilizada na tela de inserção.
        '''
        try:
            result, success = self.csv_service.start_csv_processing(
                csv_filename, 
                ano, 
                modalidade,
                mongo_client
            )
            
            if success:
                return jsonify({'message': result}), 200
            else:
                return result
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
        

    def cancel_csv_importation(self, nome_instrumento):
        try:
            result, success = self.csv_service.cancel_csv_importation(
                nome_instrumento
            )
            
            if not success:
                return jsonify({'error': result}), 400
            
            return jsonify({'message': result, 'error': ''}), 200
        
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500
        

    def get_status_csv_import(self, filename, processing, mongo_client):
        '''
        Confere o status do instrumento que está sendo processado.
        
        - Utilizada na tela de progresso do frontend, onde é feita a requisição nessa rota para poder ser visualizado o progresso do csv que está sendo inserido.
        '''
        
        try: 
            result, success = self.csv_service.get_import_status(filename=filename, processing=processing, mongo_client=mongo_client)

            if not success:
                return jsonify({'error': result}), 400
            
            return jsonify(result), 200
        except Exception as e:
            logger.exception('Erro interno do servidor')
            return jsonify({'error': f'Erro interno no servidor: {e}'}), 500


from flask import Blueprint, current_app, request, jsonify
from api.controllers.instrumento_controller import InstrumentoController
from api.utils.error_handlers import *

instrumento_bp = Blueprint('instrumento', __name__, url_prefix='/api/instrumento')
controller = InstrumentoController()

@instrumento_bp.route('/listar', methods=['GET'])
def list_instrumentos():
    mongo_client = current_app.config['MONGO_CLIENT']
    return controller.list_instrumentos(mongo_client)

@instrumento_bp.route('/listarComStatus', methods=['GET'])
def list_instrumentos_with_status():
    mongo_client = current_app.config['MONGO_CLIENT']
    return controller.list_instrumentos_with_status(mongo_client)

@instrumento_bp.route('/continuarGeracao', methods=['POST'])
def continuar_geracao():
        data = request.get_json()
        if not data or 'nome_instrumento' not in data:
            return jsonify({'error': 'Nome do instrumento não fornecido'}), 400
            
        nome_instrumento = data.get('nome_instrumento')
        mongo_client = current_app.config['MONGO_CLIENT']
        
        return controller.continuar_geracao(nome_instrumento, mongo_client)
        
@instrumento_bp.route('/<string:instrumento>/introducao/download', methods=['GET'])
def download_introducao_instrumento(instrumento):
    return controller.download_introducao_instrumento(instrumento)


@instrumento_bp.route('/<string:instrumento>/conclusao/download', methods=['GET'])
def download_conclusao_instrumento(instrumento):
    return controller.download_conclusao_instrumento(instrumento)
    
    
@instrumento_bp.route('/<string:instrumento>/introducao/substituir', methods=['POST'])
def replace_introducao_instrumento(instrumento):
    
    if 'arquivo_introducao' not in request.files:
        return validation_error(missing_fields='arquivo_introducao')
    
    intro_file = request.files['arquivo_introducao']
    
    return controller.replace_introducao_instrumento(instrumento, intro_file)
    
    
@instrumento_bp.route('/<string:instrumento>/conclusao/substituir', methods=['POST'])
def replace_conclusao_instrumento(instrumento):
    if 'arquivo_conclusao' not in request.files:
        return validation_error(missing_fields='arquivo_conclusao')
    
    concl_file = request.files['arquivo_conclusao']
    
    return controller.replace_conclusao_instrumento(instrumento, concl_file)


@instrumento_bp.route('/etapas', methods=['POST'])
def get_steps_instrument():
    data = request.json
    database: str = data.get('instrumento')
    
    if not database:
        validation_error('Database')
    
    mongo_client = current_app.config['MONGO_CLIENT']
    
    return controller.get_steps_instrument(database, mongo_client)


@instrumento_bp.route('/etapa/atualizar', methods=['PUT'])
def update_step_instrument():
    data = request.get_json()
    
    required_data = ['instrumento', 'etapa', 'novoValor']
    
    missing = [d for d in required_data if d not in data]
    
    database = data.get('instrumento')
    etapa_id = data.get('etapa')
    novo_valor_etapa = data.get('novoValor')
    
    if missing:
        return validation_error(missing_fields=missing)
    
    mongo_client = current_app.config['MONGO_CLIENT']
    return controller.update_step_instrument(database, etapa_id, novo_valor_etapa, mongo_client)
    

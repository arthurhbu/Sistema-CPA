from flask import Blueprint, request, current_app
from api.controllers.csv_controller import CsvController
from api.utils.error_handlers import *
from app import import_state

csv_bp = Blueprint('csv', __name__, url_prefix='/api/csv')
controller = CsvController()

@csv_bp.route('/importar', methods=['POST'])
def import_csv():
    
    required_files = ['file', 'arquivo_introducao', 'arquivo_conclusao']
    missing = [f for f in required_files if f not in request.files or not request.files[f].filename]
    
    if missing:
        return validation_error(missing_fields=missing)
    
    csv_file = request.files['file']
    import_state.filename = csv_file.filename
    intro_file = request.files['arquivo_introducao']
    concl_file = request.files['arquivo_conclusao']
    
    mongo_client = current_app.config['MONGO_CLIENT']
    
    return controller.import_csv(csv_file, intro_file, concl_file, mongo_client)


@csv_bp.route('/importar/confirmar', methods=['POST'])
def confirm_csv_importation():
    required_fields = ['ano', 'modalidade']
    data = request.get_json()
    
    missing = [f for f in required_fields if f not in data]
    
    if missing:
        return validation_error(missing_fields=missing)
    
    ano = data['ano']
    modalidade = data['modalidade']
    
    if import_state.processing == True:
        return error_response('Outro instrumento já está sendo processado.')
    
    mongo_client = current_app.config['MONGO_CLIENT']
    
    return controller.confirm_csv_importation(import_state.filename, ano, modalidade, mongo_client)


@csv_bp.route('/cancel/<string:nome_instrumento>', methods=['DELETE'])
def cancel_csv_importation(nome_instrumento):
    return controller.cancel_csv_importation(nome_instrumento)


@csv_bp.route('/importacao/progresso', methods=['GET'])
def get_status_csv_import():
    filename = import_state.filename
    processing = import_state.processing
    mongo_client = current_app.config['MONGO_CLIENT']
    
    return controller.get_status_csv_import(filename, processing, mongo_client)
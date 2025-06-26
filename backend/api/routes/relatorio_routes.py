from flask.blueprints import Blueprint
from api.controllers.relatorio_controller import RelatorioController
from flask import request, current_app
from api.utils.error_handlers import *

relatorio_bp = Blueprint('relatorio', __name__, url_prefix='/api/relatorios')
controller = RelatorioController()

@relatorio_bp.route('/templates/upload', methods=['POST'])
def upload_templates():
    required_files = ['arquivo_template']
    missing = [f for f in required_files if f not in request.files or not request.files[f].filename]
    
    if missing:
        return validation_error(missing_fields=missing)
    
    arquivo_template = request.files.get('arquivo_template')
    
    return controller.upload_templates(arquivo_template)

@relatorio_bp.route('/templates/download', methods=['GET'])
def download_templates_intro_concl():
    return controller.download_templates_intro_concl()
    
@relatorio_bp.route('/gerar', methods=['POST'])
def generate_reports():
    # Verificar se os dados vêm como JSON ou form data
    if request.is_json:
        data = request.get_json()
        required_fields = ['introConcl', 'ano', 'instrumento']
        missing = [f for f in required_fields if f not in data or not data[f]]
    else:
        required_fields = ['introConcl', 'ano', 'instrumento']
        missing = [f for f in required_fields if f not in request.form or not request.form[f]]
    
    if missing:
        return validation_error(missing_fields=missing)
    
    # Obter dados da requisição
    if request.is_json:
        data = request.get_json()
        ano = data.get('ano')
        introConcl = data.get('introConcl')
        instrumento = data.get('instrumento')
    else:
        ano = request.form.get('ano')
        introConcl = request.form.get('introConcl')
        instrumento = request.form.get('instrumento')
    
    # Validar se ano é um número válido
    try:
        ano = int(ano)
    except (ValueError, TypeError):
        return validation_error(missing_fields=['ano deve ser um número válido'])
    
    id_instrumento = f'{instrumento}_id'
    
    mongo_client = current_app.config['MONGO_CLIENT']
    
    return controller.generate_reports(instrumento, mongo_client, ano, introConcl, id_instrumento)
    
        
@relatorio_bp.route('/<string:id_instrumento>/download', methods=['GET'])
def download_file_zip(id_instrumento):
    filename_zip = f'{id_instrumento}.zip'
    return controller.download_file_zip(filename_zip)
    
@relatorio_bp.route('/<string:id_instrumento>/delete', methods=['DELETE'])
def delete_zip(id_instrumento):
    filename_zip = f'{id_instrumento}.zip'
    return controller.delete_zip(filename_zip)
    
@relatorio_bp.route('/zips', methods=['GET'])
def get_avaliable_zips():
    return controller.get_avaliable_zips()
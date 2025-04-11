from flask import Blueprint, request
from controllers.csv_controller import CsvController

csv_bp = Blueprint('csv', __name__, url_prefix='/api/csv')
controller = CsvController()

@csv_bp.route('/importar', methods=['POST'])
def import_csv():
    return controller.import_csv(request)

@csv_bp.route('/importar/confirmar', methods=['POST'])
def confirm_csv_importation():
    return controller.confirm_csv_importation(request)

@csv_bp.route('/cancel/<string:nome_instrumento>', methods=['DELETE'])
def cancel_csv_importation(nome_instrumento):
    return controller.cancel_csv_importation(nome_instrumento)

@csv_bp.route('importacao/progresso', methods=['GET'])
def get_status_csv_import():
    return controller.get_status_csv_import()
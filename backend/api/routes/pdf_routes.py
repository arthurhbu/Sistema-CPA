from flask.blueprints import Blueprint
from api.controllers.pdf_controller import PdfController
from flask import request
from api.utils.error_handlers import *

pdf_bp = Blueprint('pdf', __name__, url_prefix='/api/pdf')
controller = PdfController()

@pdf_bp.route('/<string:id_instrumento_pdf>/delete', methods=['DELETE'])
def delete_pdfs_zip(id_instrumento_pdf):
    
    pdf_filename: str = f'{id_instrumento_pdf}.zip'
    return controller.delete_pdfs_zip(pdf_filename)

@pdf_bp.route('/<string:id_instrumento_pdf>/download', methods=['GET'])
def download_pdfs_zip(id_instrumento_pdf):
    pdf_filename = f'{id_instrumento_pdf}.zip'
    return controller.download_pdfs_zip(pdf_filename)

@pdf_bp.route('/listar', methods=['GET'])
def list_pdfs():
    return controller.list_pdfs()

@pdf_bp.route('/gerar', methods=['POST'])
def generate_pdf():
    
    zip_file_md = request.files['compressArchive']
    return controller.generate_pdf(zip_file_md)
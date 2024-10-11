from flask import Flask, request, jsonify, render_template
from main import main
from general_controller import geraçãoDeRelatorio
import os   
from flask_cors import CORS
from flask_socketio import SocketIO
from pymongo import MongoClient
from general_controller import listDatabases
from database.pythonMongoConfig import readDBConfig
from database.connectionDB import connection


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

dbConfig: dict  = readDBConfig()
client: MongoClient = connection(dbConfig)

UPLOAD_FOLDER = 'src/csvManipulationFunctions/CSVs'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
filename: str = ''
processing: bool = False

@app.route('/api/importar', methods=["POST"])
def importar():
    global filename
    global processing
    print('receive request')
    file = request.files['file']
    print(f'filename: {file.filename}')
    ano = request.form.get('ano')
    print(f'ano: {ano}')
    if file and ano:
        filename = file.filename
        print(filename)
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        # main(ano, file.filename, '', 'inserir', client)
        processing = True
        
        socketio.start_background_task(target=processa_csv, filename=filename, ano=ano)
        return jsonify({'message': 'File successfully uploaded'}), 200
        
    return jsonify({'error': 'Missing file or ano'}), 400

def processa_csv(filename, ano):
    global processing
    try:
        main(ano, filename, '', 'inserir', client)
    finally: 
        processing = False

@app.route('/progresso', methods=['GET'])
def get_status():
    global filename
    global processing
    return {'processing': False, 'file': filename}

@app.route('/api/instrumentos', methods=['GET'])
def list_instrumentos():
    dbs = listDatabases(client)
    return jsonify(dbs)

@app.route('/api/gerarRelatorios', methods=['POST'])
def gerarRelatorios(): 
    ano = request.form.get('ano')
    introConcl = request.form.get('introConcl')
    instrumento = request.form.get('instrumento')
    print(ano)
    print(introConcl)
    print(instrumento)
    
    if ano and introConcl and instrumento:
        print('oi') 
        # Funcao para gerar relatorios
        # Criar um await e async para esperar confirmar que os relatorios foram gerados com sucesso
        return jsonify({'message': 'Relatórios gerados com sucesso!'}), 200

    return jsonify({'message': 'Não foi possível gerar os relatórios'}), 400
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
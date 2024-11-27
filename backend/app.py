from flask import Flask, request, jsonify, render_template
import os, csv
from flask_cors import CORS
from flask_socketio import SocketIO
from pymongo import MongoClient
from general_controller import listDatabases
from database.pythonMongoConfig import readDBConfig
from database.connectionDB import connection
from general_controller import applicationController, getProgressoInsercao, getEtapas, atualizaEtapa
from bson import ObjectId
from collections import OrderedDict

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

def converteObjectIDToStr(document):
    if document is None:
        return None
    return {key: (str(value) if isinstance(value, ObjectId) else value) for key, value in document.items()}

def removeKeys(document, keysToRemove):
    return {k: v for k,v in document.items() if k not in keysToRemove}
    

@app.route('/api/importar', methods=["POST"])
def importCsv():
    global filename
    
    file = request.files['file']
    ano = request.form.get('ano')
    
    if file and ano:
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        try:
            with open(f'{file_path}', newline='', encoding='utf-8') as csvFile:
                reader = csv.reader(csvFile)
                header = next(reader)
            
            return jsonify({'header': header, 'error': ''}), 200 
        except:
            return jsonify({'header': '', 'error': 'Ocorreu um erro na hora de realizar a leitura do cabeçalho.'}), 400
            
        
    return jsonify({'header': '', 'error': 'Não foi possível carregar o ano ou o arquivo CSV passado.'}), 400


def processCsv(filename, ano):
    global processing
    try:
        applicationController(int(ano), filename, '', 'inserir', client)
    finally: 
        processing = False


@app.route('/api/confirmarImportacao', methods=['POST'])
def confirmImportation():
    global processing, filename
    ano = request.json.get('ano')
    print(filename)
    print(ano)
    if filename and ano:
        processing = True
        socketio.start_background_task(target=processCsv, filename=filename, ano=ano)
        return jsonify({'response': 'Análise confirmada e importação iniciada!'}), 200
    
    return jsonify({'response':'Erro ao confirmar a analise'}), 400


@app.route('/progresso', methods=['GET'])
def getStatus():
    global filename
    global processing
    processing = True
    progresso = {}
    if processing == True:
        progresso = getProgressoInsercao(filename, client)
        progresso = converteObjectIDToStr(progresso)  
        
        progresso = removeKeys(progresso, ['_id', 'instrumento'])
        print(progresso)
    return {'processing': processing, 'file': filename, 'progresso': progresso}, 200


@app.route('/api/instrumentos', methods=['GET'])
def listInstrumentos():
    dbs = listDatabases(client)
    return jsonify(dbs)


@app.route('/api/gerarRelatorios', methods=['POST'])
def generateReports(): 
    ano = request.form.get('ano')
    introConcl = request.form.get('introConcl')
    instrumento = request.form.get('instrumento')
    print(ano)
    print(introConcl)
    print(instrumento)
    
    if ano and introConcl and instrumento:
        applicationController(int(ano), instrumento, introConcl, 'gerarRelatorio', client)
        # Criar um await e async para esperar confirmar que os relatorios foram gerados com sucesso
        return jsonify({'message': 'Relatórios gerados com sucesso!'}), 200
            
    return jsonify({'message': 'Não foi possível gerar os relatórios'}), 400


@app.route('/api/etapasInstrumento', methods=['POST'])
def getSteps():
    data = request.json
    database = data.get('instrumento')
    
    if not database:
        return {'error': 'Instrumento não fornecido'}, 400
    
    etapas = getEtapas(database, client)
    if not etapas:
        return {'error': 'Não foi possível encontrar etapas para o instrumento'}, 404
    
    etapas = converteObjectIDToStr(etapas)
    etapas = removeKeys(etapas, ['_id'])
    
    
    return jsonify({'etapas': etapas}), 200


@app.route('/api/atualizarEtapa', methods=['POST'])
def updateStep():
    data = request.get_json()
    database = data.get('instrumento')
    etapaId = data.get('etapa')
    etapaValor = data.get('novoValor')
    
    resultado = atualizaEtapa(database, etapaId, etapaValor, client)
    
    if resultado == 'Sucesso':
        return {'message': 'Etapa atualizada com sucesso'}, 200
    
    return {'error': resultado}, 400
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    

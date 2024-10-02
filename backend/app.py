from flask import Flask, request, jsonify, render_template
from main import main
from general_controller import geraçãoDeRelatorio
import os   
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

UPLOAD_FOLDER = 'src/csvManipulationFunctions/CSVs'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
filename = ''
processing = False

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
        
        # main(ano, file.filename, '', 'inserir')
        processing = True
        
        socketio.start_background_task(target=processa_csv, filename=filename, ano=ano)
        return jsonify({'message': 'File successfully uploaded'}), 200
        
    return jsonify({'error': 'Missing file or ano'}), 400

def processa_csv(filename, ano):
    global processing
    try:
        main(ano, filename, '', 'inserir')
    finally: 
        processing = False

@app.route('/progresso', methods=['GET'])
def get_status():
    global filename
    global processing
    return {'processing': False, 'file': filename}



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
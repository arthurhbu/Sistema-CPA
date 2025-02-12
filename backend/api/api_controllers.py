from flask import request, jsonify
from api.utils_api import converteObjectIDToStr, removeKeys
from src.main_controller import list_databases,get_etapas,atualiza_etapa,application_controller,get_progresso_insercao
import os, csv

filename: str = ''
processing: bool = False

UPLOAD_FOLDER = 'src/csv/CSVs'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def setup_routes(app, client, socketio): 
    
    @app.route('/api/importar', methods=["POST"])
    def importCsv():
        '''
        Importa o instrumento para o backend onde é retornado o header desse instrumento para poder ser feito uma comparação do header correto com o desse instrumento.
        
        - Rota utilizada na tela de inserção, onde é feita a requisição.
        
        '''
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

    
    
    @app.route('/api/confirmarImportacao', methods=['POST'])
    def confirmImportation():
        '''
        Confirma a importação do instrumento com a requisição vinda do usuário após ter sido conferido o header.
        
        - Rota utilizada na tela de inserção.
        '''
        global processing, filename
        ano = request.json.get('ano')
        modalidade = request.json.get('modalidade')
        print(ano, modalidade)
        if filename and ano and modalidade:
            try: 
                processing = True
                socketio.start_background_task(target=processCsv, filename=filename, ano=ano, modalidade=modalidade)
                return jsonify({'message': 'importacao iniciada com sucesso'}), 200
            except Exception as e: 
                return jsonify({'message': 'um erro ocorreu durante a importação'}), 400
        return jsonify({'message': 'faltando nome do arquivo ou ano ou modalidade'}), 400


    @app.route('/progresso', methods=['GET'])
    def getStatusCsvImport():
        '''
        Confere o status do instrumento que está sendo processado.
        
        - Utilizada na tela de progresso do frontend, onde é feita a requisição nessa rota para poder ser visualizado o progresso do csv que está sendo inserido.
        '''
        global filename
        global processing
        progresso = {}
        if processing == True:
            progresso = get_progresso_insercao(filename, client)
            progresso = converteObjectIDToStr(progresso)  
            progresso = removeKeys(progresso, ['_id', 'instrumento'])
        return {'processing': processing, 'file': filename, 'progresso': progresso}, 200


    @app.route('/api/instrumentos', methods=['GET'])
    def listInstrumentos():
        '''
        Lista os instrumentos disponíveis no banco MongoDB para o usuário.
        
        '''
        dbs = list_databases(client)
        return jsonify(dbs)


    @app.route('/api/gerarRelatorios', methods=['POST'])
    def generateReports(): 
        '''
        Gera os relatórios para certo instrumento com a requisição feita pelo usuário, sendo necessário informações como:
        
            - ano do instrumento
            - Introdução e Conclusão do modal do instrumento (EAD, DISCENTES, EGRESSOS, ETC)
            - Nome do instrumento que o liga ao banco de dados com as informações dele
            
        '''
        ano = request.form.get('ano')
        introConcl = request.form.get('introConcl')
        instrumento = request.form.get('instrumento')
        
        if ano and introConcl and instrumento:
            application_controller(int(ano), instrumento, introConcl, 'gerarRelatorio', client)
            return jsonify({'message': 'Relatórios gerados com sucesso!'}), 200
                
        return jsonify({'message': 'Não foi possível gerar os relatórios'}), 400


    @app.route('/api/etapasInstrumento', methods=['POST'])
    def getStepsInstrument():
        '''
        Lista as etapas já finalizadas daquele instrumento de acordo com o usuário que o preenche.
        '''
        data = request.json
        database = data.get('instrumento')
        
        if not database:
            return {'error': 'Instrumento não fornecido'}, 400
        
        etapas = get_etapas(database, client)
        if not etapas:
            return {'error': 'Não foi possível encontrar etapas para o instrumento'}, 404
        
        etapas = converteObjectIDToStr(etapas)
        etapas = removeKeys(etapas, ['_id'])
        
        return jsonify({'etapas': etapas}), 200


    @app.route('/api/atualizarEtapa', methods=['POST'])
    def updateStepInstrument():
        '''
        Atualiza as etapas do instrumento escolhido.
        '''
        data = request.get_json()
        database = data.get('instrumento')
        etapaId = data.get('etapa')
        etapaValor = data.get('novoValor')
        
        resultado = atualiza_etapa(database, etapaId, etapaValor, client)
        
        if resultado == 'Sucesso':
            return {'message': 'Etapa atualizada com sucesso'}, 200
        
        return {'error': resultado}, 400
    
    def processCsv(filename, ano, modalidade):
        global processing
        try:
            with app.app_context():
                response = application_controller(int(ano), filename, '', 'inserir', client, modalidade)
                socketio.emit('importacao_concluida', {'status':'sucesso', 'message': f'{response}'})
        except Exception as e:
            socketio.emit('importacao_concluida', {'status': 'erro', 'message': f'Ocorreu um erro na importação: {e}'})
        finally: 
            processing = False
from flask import Flask
from flask_cors import CORS
from database.pythonMongoConfig import readDBConfig
from database.connectionDB import connection
from pymongo import MongoClient
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("meu_app.log"),    
        logging.StreamHandler()              
    ]
)

class ImportState:
    def __init__(self):
        self.filename = ''
        self.processing = False
        
import_state = ImportState()

def create_app():

    load_dotenv()

    app: Flask = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    dbConfig: dict = readDBConfig()
    client: MongoClient = connection(dbConfig)

    app.config['MONGO_CLIENT'] = client

    from api.routes.csv_routes import csv_bp
    from api.routes.pdf_routes import pdf_bp
    from api.routes.relatorio_routes import relatorio_bp
    from api.routes.instrumento_routes import instrumento_bp
    
    app.register_blueprint(csv_bp)
    app.register_blueprint(pdf_bp)
    app.register_blueprint(relatorio_bp)
    app.register_blueprint(instrumento_bp)
    
    return app
    

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)

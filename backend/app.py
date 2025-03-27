from flask import Flask
from flask_cors import CORS
from database.pythonMongoConfig import readDBConfig
from database.connectionDB import connection
from api.api_controllers import setup_routes
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

dbConfig: dict = readDBConfig()
client: MongoClient = connection(dbConfig)

setup_routes(app, client)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

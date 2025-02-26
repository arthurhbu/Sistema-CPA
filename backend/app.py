import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from database.pythonMongoConfig import readDBConfig
from database.connectionDB import connection
from api.api_controllers import setup_routes
from pymongo import MongoClient

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")

dbConfig: dict = readDBConfig()
client: MongoClient = connection(dbConfig)

setup_routes(app, client, socketio)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)

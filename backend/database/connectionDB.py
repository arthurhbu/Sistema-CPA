from pymongo import (
    MongoClient,
    errors)
from database.pythonMongoConfig import readDBConfig

def connection(db_config):
    """
    Realiza a conexão com o banco de dados

    :param db_config: contém informações do host e usuário para realizar a conexão
    :type db_config: Dict
    :return: Retorna o MongoClient 
    :rtype: MongoClient
    """
    try:
        print("Connecting to mongoDB database...")
        Mclient = MongoClient(
            db_config['host'],
            username=db_config['username'],
            password=db_config['password'],
            serverSelectionTimeoutMS=5000
        )
    except errors.ConnectionError as err:
        print(f"Connection error: {err}")
        return None
    except errors.OperationFailure as err:
        print(f"Authentication error: {err}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None

    print("Connected successfully!")
    return Mclient

def connectToDatabase(database_name, client):
    print("Connection Established with MongoDB")
    filterDBName = database_name.replace(" ", "")
    filterDBName = filterDBName.replace(".csv", "")
    database = client[filterDBName]
    print(filterDBName)
    return filterDBName, database

def initialize_all_collections(database: str):
    """
    Inicializa todos as coleções pertencentes ao banco que foi escolhido.
    
    """

    dict_collections = {
        'instrumento': database['instrumento'],
        'cursos_e_centros': database['cursos_e_centros'], 
        'centros_e_diretores': database['centros_e_diretores'],
        'cursos_por_centro': database['cursos_por_centro'],
        'centro_por_ano': database['centro_por_ano'],
        'progresso': database['progresso_da_insercao'],
        'etapas': database['etapas'],
    }
    
    return dict_collections
    

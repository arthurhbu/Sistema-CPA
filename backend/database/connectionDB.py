from pymongo import (
    MongoClient,
    errors)
from pymongo.database import Database
from database.pythonMongoConfig import readDBConfig


def connection(db_config: dict) -> MongoClient:
    """
    Realiza a conexão com o client do MongoDB.

    Args:
        db_config (dict): Dict contendo informações para incializar conexão com o banco MongoDB.
    Returns:
        Mclient (MongoClient): Conexão/Cliente com o MongoDB.
    """
    try:
        print("Connecting to mongoDB database...")
        Mclient = MongoClient(
            db_config['host'],
            username=db_config['username'],
            password=db_config['password'],
            serverSelectionTimeoutMS=5000,
            maxPoolSize=50,  
            minPoolSize=10,  
            maxIdleTimeMS=30000,  
            waitQueueTimeoutMS=10000,  
            connectTimeoutMS=20000,  
            socketTimeoutMS=20000, 
            retryWrites=True,  
            retryReads=True,  
            heartbeatFrequencyMS=10000  
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

def connectToDatabase(database_name: str, client: MongoClient) -> tuple[str, Database]:
    """
    Realiza os passos para a conexão ser estabelecida com o banco.
    
    Args:
        database_name (str): Nome do database/instrumento que será utilizado.
        client (MongoClient): Client que se conecta com o MongoDB.
    Returns:
        filterDBName, database (tuple[str, Database]): Retorna nome do database e a Entidade de conexão com esse database.
    Raises:
        None:
    """
    print("Connection Established with MongoDB")
    filterDBName = database_name.replace(" ", "")
    filterDBName = filterDBName.replace(".csv", "")
    database = client[filterDBName]
    print(filterDBName)
    return filterDBName, database

def initialize_all_collections(database: str) -> dict:
    """
    Inicializa todos as coleções pertencentes ao banco que foi escolhido.

    Args:
        database (str): Conexão estabelecida com o database/instrumento selecionado.
    Returns:
        dict_collections (dict): Retorna um dict contendo todas as conexões estabelecidas com as Collections daquele database.
    Raises:
        None:
    
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
    

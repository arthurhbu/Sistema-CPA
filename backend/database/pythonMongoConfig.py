from configparser import ConfigParser
import os

def readDBConfig(filename: str='config.ini', section: str='Mongodb') -> dict:
    """ 
    Captura o arquivo contendo as configurações iniciais para conexão com o mongoDB.
    
    Args: 
        filename (str): Nome do arquivo .ini que contém a conexão.
        section (str): Seção do arquivo .ini que contém informações de conexão do mongoDB.
    Returns:
        db_config (dict): Dict contendo as informações para conexão.
    Raises:
        None:
    """

    thisfolder = os.path.dirname(os.path.abspath(__file__))
    initfile = os.path.join(thisfolder, 'config.ini')

    parser = ConfigParser()
    parser.read(initfile)

    db_config = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db_config[item[0]] = item[1]
    else:
        raise Exception(
            '{0} not found in the {1} file.'.format(section, filename)
        )
        
    return db_config
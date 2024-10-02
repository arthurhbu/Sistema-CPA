from configparser import ConfigParser
import os

def readDBConfig(filename='config.ini', section='Mongodb'):
    """ Read database configuration file and return a dictionary object
    :param filenae: name of the configuration file
    :param section: section of database configuration

    :return: a dictionary of database parameters
    """

    #Finding the path to the config.ini archive
    thisfolder = os.path.dirname(os.path.abspath(__file__))
    initfile = os.path.join(thisfolder, 'config.ini')

    #Reading the filename and creating the parser
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
from pymongo import errors
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import MongoClient
from database.connectionDB import connectToDatabase, initialize_all_collections
from src.csv.csv_controller import *
from src.data_generator.generator_controller import *
from src.relatorio.relatorio_controller import gerar_todos_relatorios
from database.databaseQuerys import df_centro_por_ano,df_cursos_por_centro
from database.databaseQuerys import update_progresso
from src.utils.compact_and_send_zip import zip_markdown_files, send_email_zip

'''
Controller principal onde funciona como um controlador de um repositório de funções que é usada pela api.

'''

def initalize_database_inserts(database_name: Database, csv_filename: str, client: MongoClient, modalidade: str, collection_instrumento: Collection, collection_centro_e_curso: Collection, collection_diretor_e_centro: Collection,  progresso: Collection, etapas: Collection, ) -> None:
    """
    Função que junta os primeiros passos da execução do programa que seria as inserções e os realiza de uma vez.
    """

    progresso.insert_one(
        {
            'instrumento': f'{database_name}',
            'Insercao_Main_CSV': 'Pendente',
            'Insercao_Curso_Centro_Database': 'Pendente',
            'Insercao_Centro_Diretor_Database': 'Pendente',
            'Geracao_de_Dados': 'Pendente',
            'Criacao_Cursos_por_Centro_Database': 'Pendente',
            'Criacao_Centro_por_Ano_Database': 'Pendente',
        }
    )
    
    etapas.insert_one(
        {
            'Inserção/Análise do instrumento': False,
            'Geração de Relatórios': False,
            'Revisão de Relatórios': False,
            'Correção de possíveis erros': False,
            'Geração de PDFs': False,
            'Entrega dos Relatórios': False,
            'Finalizado': False
        }
    )
    
    progresso_etapa1 = CSVManagment.insert_main_csv_to_database(collection_instrumento, csv_filename, modalidade)
    update_progresso(progresso, 'Insercao_Main_CSV', progresso_etapa1)
    
    progresso_etapa2 = CSVManagment.insert_curso_e_centro_csv_to_database(collection_centro_e_curso) 
    update_progresso(progresso, 'Insercao_Curso_Centro_Database', progresso_etapa2)
    
    progresso_etapa3 = CSVManagment.insert_centro_diretor_csv_database(collection_diretor_e_centro)  
    update_progresso(progresso, 'Insercao_Centro_Diretor_Database', progresso_etapa3)
    
    progresso_etapa4 = generate_graph_table_report(client, database_name, collection_instrumento)
    if progresso_etapa4 != 'Finalizado':
        raise Exception('Erro na geração de dados: ', progresso_etapa4)
    update_progresso(progresso, 'Geracao_de_Dados', progresso_etapa4)
    


def prepare_side_dataframes(database: Database, ano: int, modal: str, collection_instrumento: Collection, collection_cursos_e_centros: Collection, progresso: Database) -> None:
    """
    Realiza a criação dos dataframes intermediários que são utilizados para a criação de da introdução e conclusão. E os insere em uma collection no banco de dados.

    :param database: Conexão com o banco de dados.
    :type database: Database
    :param ano: Contém o ano que é uma condition para escolhida que tem relação com o ano do arquivo csv
    será feito a leitra.
    :type ano: Integer
    :param collectionCurso: Nome da collection que contém as informações do csv principal.
    :type collectionCurso: Collection (MongoDB)    
    """

    try: 
        centros = collection_instrumento.distinct('centro_de_ensino')

        document_to_insert = []

        for centro in centros:
            document_to_insert.extend(df_cursos_por_centro(collection_cursos_e_centros, ano, centro))
            
        database['cursos_por_centro'].insert_many(document_to_insert)   
        progresso_etapa5 = 'Finalizado'
    except:
        progresso_etapa5 = 'Ocorreu um erro na criaçao do dataframe cursos por centro'
    
    update_progresso(progresso,'Criacao_Cursos_por_Centro_Database',progresso_etapa5)

    progresso_etapa6 = df_centro_por_ano(collection_instrumento, database, ano, modal)
    update_progresso(progresso, 'Criacao_Centro_por_Ano_Database', progresso_etapa6)


def generate_reports(collection_instrumento: Collection, collection_centro_por_ano: Collection, collection_cursos_por_centro: Collection, ano: int, database_name: str, modal: str, id_instrumento: str) -> None:
    """
    Realiza a criação de relatórios, podendo ser possível escolher se será gerado um único relatório,
    por centro ou todos os relatórios.

    :param collectionCurso: Nome da collection que contém as informações do csv principal.
    :type collectionCurso: Collection (MongoDB)     
    :param collectionCentroPorAno: Nome da collection que contém as informações sobre os centros.
    :type: Collection (MongoDB)
    :param CollectionCursosPorCentro: Nome da collection que contém informações sobre os cursos de um centro.
    :type: Collection (MongoDB)
    :param ano: Contém o ano que é uma condition para escolhida que tem relação com o ano do arquivo csv será feito a leitra.
    :type ano: Integer
    :param dbName: Nome do banco de dados que está sendo manipulado
    :type dbName: str
    """
    modal = modal.lower()
    arquivo_intro_esc = f'introducao_{modal}.md'
    arquivo_conclusao_esc = f'conclusao_{modal}.md'
    
    gerar_todos_relatorios(collection_instrumento, collection_centro_por_ano, collection_cursos_por_centro, arquivo_intro_esc, arquivo_conclusao_esc, ano, database_name, modal)
    zip_markdown_files(database_name, f'{id_instrumento}.zip')
    # send_email_zip(f'./relatorio/markdowns/{database_name}/{database_name}.zip', 'ra129406@uem.br', 'sec-cpa@uem.br', 'senha')
    

def inserir_e_processar_csv(ano: int, csv_Filename: str, modalidade: str, client: MongoClient,) -> None:
    """
    Args:
        ano (int): Ano de referência para a operação.
        csv_Filename (str): Caminho para o arquivo CSV que contém os dados.
        modal (str): Modalidade de operação.
        modo (str): Modo de operação, pode ser 'inserir' ou 'gerarRelatorio'.
        client (MongoClient): Cliente MongoDB para conexão com o banco de dados.
    Returns:
        None: A função não retorna nenhum valor, mas pode retornar mensagens de sucesso ou erro.
    Raises:
        Exception: Lança uma exceção se ocorrer algum erro durante a execução.
    """
    
    dbName, database = connectToDatabase(csv_Filename, client)
    collections = initialize_all_collections(database)
    
    try:
        initalize_database_inserts(
            dbName, 
            csv_Filename, 
            client, 
            modalidade,
            collections['instrumento'], 
            collections['cursos_e_centros'],
            collections['centros_e_diretores'], 
            collections['progresso'], 
            collections['etapas'], 
            )
        
        prepare_side_dataframes(
            database, 
            ano, 
            modalidade, 
            collections['instrumento'], 
            collections['cursos_e_centros'], 
            collections['progresso']
            )
        
        return 'Inserção finalizada com sucesso'

    except Exception as e: 
        return f'Ocorreu um erro: {e}'
    
def gerar_relatorios(csv_filename: str, client: MongoClient, ano: int, modal: str, id_instrumento: str) -> str:
    dbName, database = connectToDatabase(csv_filename, client)
    collections = initialize_all_collections(database)
    
    try:
        generate_reports(collections['instrumento'], collections['centro_por_ano'], collections['cursos_por_centro'], ano, dbName, modal, id_instrumento)
        return 'Relatórios gerados com sucesso'
    except Exception as e:
        return f'Ocorreu um erro: {e}'

def list_databases(client): 
    dbs = client.list_database_names()
    usersDatabases = [db for db in dbs if db not in ['admin', 'config', 'local']]
    return usersDatabases


def get_progresso_insercao(instrumento: str, client: MongoClient):
    dbName, database = connectToDatabase(instrumento, client)
    progresso = database['progresso_da_insercao']
    progressoDocument = progresso.find_one()
    return progressoDocument
    
    
def get_etapas(instrumento: str, client: MongoClient):
    dbName, database = connectToDatabase(instrumento, client)
    etapas = database['etapas']
    etapasDocument = etapas.find_one()
    return etapasDocument


def atualiza_etapa(instrumento: str, etapa: str, novoValor: bool, client: MongoClient):
    dbName, database = connectToDatabase(instrumento, client)
    etapas = database['etapas']
    try:
        etapas.update_one({}, 
            {'$set':
                {
                    f'{etapa}': f'{novoValor}'        
                }}
        )
        return 'Sucesso'
    except (DuplicateKeyError, OperationFailure) as db_error:
        return f'Erro no banco de dados: {db_error}'
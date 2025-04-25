from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import MongoClient
from pymongo import ReturnDocument
from database.connectionDB import connectToDatabase, initialize_all_collections
from src.csv.csv_controller import *
from src.data_generator.generator_controller import *
from src.relatorio.relatorio_controller import gerar_todos_relatorios
from database.databaseQuerys import *
from src.utils.compact_and_send_zip import zip_markdown_files
from api.gmail_api.gmail_api_controller import send_email_via_gmail_api
from api.utils.error_handlers import *

'''
Controller principal onde funciona como um controlador de um repositório de funções que é usada pela api.

'''

def initalize_database_inserts(database_name: Database, csv_filename: str, client: MongoClient, modalidade: str, collection_instrumento: Collection, collection_centro_e_curso: Collection, collection_diretor_e_centro: Collection,  progresso: Collection, etapas: Collection, ) -> dict:
    """
    Função para inicializar as Collections em nosso banco e inserir o arquivo CSV no banco e por último gerar os textos e figuras utilizando uma LLM.
        
    Args:
        database_name (Database): Nome do banco/Collection que estaremos utilizando.
        csv_filename (str): Nome do arquivo CSV do instrumento.
        client (MongoClient): client do MongoDB.
        modalidade (str): Tipo do instrumento (EAD, EGRESSO, DISC, etc) para inserção personalizada.
        collection_instrumento (Collection): Collection principal.
        collection_centro_e_curso (Collection): Collection contendo CSV de centros e cursos.
        collection_diretor_e_centro (Collection): Collection contendo CSV dos diretores e centros.
        progresso (Collection): Collection utilizada para atualizar o progresso da inserção.
        etapas (Collection): Collection utilizada para o usuário atualizar as etapas de processo do instrumento.
    Returns:
        dict: Retorna um dicionário contendo status da importação.
    Raises:
        Raise: A função não levanta nenhuma exceção, apenas repassa as exceções que ocorreram antes.
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
    
    progresso_etapa1: str = CSVManagment.insert_main_csv_to_database(collection_instrumento, csv_filename, modalidade)
    if progresso_etapa1 != 'Finalizado':
        return {'Success': False, 'Error': progresso_etapa1, 'Message': 'Ocorreu um erro ao tentar inserir CSV principal'}
    update_progresso(progresso, 'Insercao_Main_CSV', progresso_etapa1)
    
    progresso_etapa2: str = CSVManagment.insert_curso_e_centro_csv_to_database(collection_centro_e_curso) 
    if progresso_etapa2 != 'Finalizado':
        return {'Success': False, 'Error': progresso_etapa2, 'Message': 'Ocorreu um erro ao tentar inserir CSV centro_e_curso'}
    update_progresso(progresso, 'Insercao_Curso_Centro_Database', progresso_etapa2)
    
    progresso_etapa3: str = CSVManagment.insert_centro_diretor_csv_database(collection_diretor_e_centro)  
    if progresso_etapa3 != 'Finalizado':
        return {'Success': False, 'Error': progresso_etapa3, 'Message': 'Ocorreu um erro ao tentar inserir CSV centro_diretor'}
    update_progresso(progresso, 'Insercao_Centro_Diretor_Database', progresso_etapa3)
    
    progresso_etapa4: str = generate_graph_table_report(client, database_name, collection_instrumento)
    if progresso_etapa4 != 'Finalizado':
        return {'Success': False, 'Error': progresso_etapa4, 'Message': 'Ocorreu um erro ao tentar gerar grafico, tabela e legenda'}
    update_progresso(progresso, 'Geracao_de_Dados', progresso_etapa4)
    
    return {'Success': True, 'Error': '', 'Message': 'Inserção e geração de dados finalizada com sucesso'}


def prepare_side_dataframes(database: Database, ano: int, modal: str, collection_instrumento: Collection, collection_cursos_e_centros: Collection, progresso: Database) -> dict:
    """
    Realiza a criação dos dataframes intermediários que são utilizados para a criação de da introdução e conclusão. E os insere em uma collection no banco de dados.
    
    Args:
        database (Database): Conexão com o banco de dados.
        ano (int): Contém o ano que é uma condition para escolhida que tem relação com o ano do arquivo csv será feito a leitra.
        collection_instrumento (Collection): Collection que contém as informações do csv principal.
        collection_cursos_e_centros (Collection): Collection que contém informações do csv cursos_e_centros.
        progresso (Collection): Collection que contém o progresso da inserção e geração de dados.
    Returns:
        dict: A função retorna um dict contendo se a etapa foi bem sucedida, caso não tenha sido, ele retorna a Exception gerada.
    Raises:
        Raise: A função não levanta nenhuma exceção, apenas repassa as exceções que ocorreram antes.
    """

    centros = collection_instrumento.distinct('centro_de_ensino')

    document_to_insert = []

    for centro in centros:
        resultado_cursos_por_centro: dict = df_cursos_por_centro(collection_cursos_e_centros, ano, centro)
        if resultado_cursos_por_centro['Success'] == False:
            return {'Success': False, 'Error': f"{resultado_cursos_por_centro['error']}"}
        document_to_insert.extend(resultado_cursos_por_centro['resultado'])
        
    database['cursos_por_centro'].insert_many(document_to_insert)   
    progresso_etapa5 = 'Finalizado'
    update_progresso(progresso,'Criacao_Cursos_por_Centro_Database',progresso_etapa5)

    resultado_df_centro_por_ano: dict  = df_centro_por_ano(collection_instrumento, database, ano)

    if resultado_df_centro_por_ano['Success'] == False: 
        progresso_etapa6 = resultado_df_centro_por_ano['error']
        update_progresso(progresso, 'Criacao_Centro_por_Ano_Database', progresso_etapa6)
        return {'Success': False, 'Error': f"{resultado_df_centro_por_ano['error']}"}
    
    progresso_etapa6 = resultado_df_centro_por_ano['message']
    update_progresso(progresso, 'Criacao_Centro_por_Ano_Database', progresso_etapa6)
    
    return {'Success': True, 'Message': 'Etapa finalizada com sucesso'}


def generate_reports(collection_instrumento: Collection, collection_centro_por_ano: Collection, collection_cursos_por_centro: Collection, ano: int, database_name: str, modal: str, id_instrumento: str, nome_instrumento: str) -> dict:
    """
    Realiza a geração dos relatórios markdowns.

    Args:
        collection_instrumento (Collection): Collection do CSV principal.
        collection_centro_por_ano (Collection): Collection criada centro_por_ano.
        collection_cursos_por_centro (Collection): Collection criada cursos_por_centro.
        ano (int): Indica o ano do relatório que será gerado.
        database_name (str): Contém o nome do banco de dados/instrumento que será usado.
        modal (str): Modalidade/tipo do instrumento que será gerado.
        id_instrumento (str): Id criado para nomear o arquivo ZIP que será criado.
    Returns:
        dict: A função retorna um dict contendo se a etapa foi bem sucedida, caso não tenha sido, ele retorna a Exception gerada.
    Raises:
        Raise: A função não levanta nenhuma exceção, apenas repassa as exceções que ocorreram antes.
    """
    
    res_gerar_todos_relatorios: dict = gerar_todos_relatorios(collection_instrumento, collection_centro_por_ano, collection_cursos_por_centro, ano, database_name, modal, nome_instrumento)
    
    if res_gerar_todos_relatorios['Success'] == False:
        send_email_via_gmail_api('', 'sec-cpa@uem.br', 'Ocorreu um erro ao tentar gerar os relatórios', f"Uma exceção inesperada ocorreu durante a geração de relatórios, confira a seguir: \n\n {res_gerar_todos_relatorios['Error']} ")
        return {'Success': False, 'error': res_gerar_todos_relatorios['Error']}
    
    res_zip_files: dict = zip_markdown_files(database_name, f'{id_instrumento}.zip')
    
    if res_zip_files['Success'] == False: 
        send_email_via_gmail_api('', 'sec-cpa@uem.br', 'Um erro ocorreu ao tentar compactar relatorios', f"Uma exceção inesperada ocorreu durante a compactação de arquivos, confira a seguir: \n\n {res_zip_files['Error']} ")
        return {'Success': False, 'error': res_zip_files['Error']}
        
    return {'Success': True}
    

def inserir_e_processar_csv(ano: int, csv_Filename: str, modalidade: str, client: MongoClient,) -> None:
    """
    Args:
        ano (int): Ano de referência para a operação.
        csv_Filename (str): Caminho para o arquivo CSV que contém os dados.
        modalidade (str): Tipo do instrumento que será processado.
        client (MongoClient): Cliente MongoDB para conexão com o banco de dados.
    Returns:
        None: A função não retorna nenhum valor, mas pode retornar mensagens de sucesso ou erro.
    Raises:
        Exception: Lança uma exceção se ocorrer algum erro durante a execução.
    """
    
    dbName, database = connectToDatabase(csv_Filename, client)
    collections = initialize_all_collections(database)
    
    try:
        response_initalize_database_inserts: dict = initalize_database_inserts(
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
        
        if response_initalize_database_inserts['Success'] == False: 
            send_email_via_gmail_api('', 'sec-cpa@uem.br', f"{response_initalize_database_inserts['Message']}", f"{response_initalize_database_inserts['Error']}")
            return
        
        response_prepare_side_dataframes: dict = prepare_side_dataframes(
            database, 
            ano, 
            modalidade, 
            collections['instrumento'], 
            collections['cursos_e_centros'], 
            collections['progresso']
            )
        
        if response_prepare_side_dataframes['Success'] == False:
            send_email_via_gmail_api('', 'sec-cpa@uem.br', 'Ocorreu um erro ao tentar gerar as collections de apoio', f"{response_prepare_side_dataframes['Error']}")
            return
        
        return 'Inserção finalizada com sucesso'

    except Exception as e: 
        return f'Ocorreu um erro: {e}'
  
    
def setup_to_generate_reports(nome_instrumento: str, client: MongoClient, ano: int, modal: str, id_instrumento: str) -> dict:
    """
    Realiza a geração dos relatórios markdowns.

    Args:
        csv_filename (str): Nome do arquivo csv que foi importado.
        client (MongoClient): Client proveniente do mongo.
        ano (int): Ano do instrumento que será gerado.
        modal (str): Modalidade/tipo do instrumento.
        id_instrumento (str): Id para reconhecimento do arquivo Zip gerado.
    Returns:
        dict: A função retorna um dict contendo se a etapa foi bem sucedida, caso não tenha sido, ele retorna a Exception gerada.
    Raises:
        Raise: A função não levanta nenhuma exceção, apenas repassa as exceções que ocorreram antes.
    """
    dbName, database = connectToDatabase(nome_instrumento, client)
    collections = initialize_all_collections(database)
    
    res: dict = generate_reports(collections['instrumento'], collections['centro_por_ano'], collections['cursos_por_centro'], ano, dbName, modal, id_instrumento, nome_instrumento)
    return res


def list_databases(client: MongoClient) -> list[str]: 
    """
    Lista todos os databases/instrumentos disponíveis
    
    Args:
        client (MongoClient): client proveniente do mongo.
    Returns:
        user_databases: Retorna uma lista contendo o nome de todos os databases/instrumentos disponíveis.
    """
    dbs: list[str] = client.list_database_names()
    users_database: list[str] = [db for db in dbs if db not in ['admin', 'config', 'local']]
    return users_database


def get_progresso_insercao(instrumento: str, client: MongoClient) -> ReturnDocument:
    """
    Pega a Collection Progresso de inserção do instrumento selecionado.
    
    Args:
        instrumento (str): Nome do instrumento/database que será pego a Collection.
        client (MongoClient): client proveniente do mongo.
    Returns:
        progressoDocument: Retorna o document que contém as informações do progresso da inserção.
    """

    dbName, database = connectToDatabase(instrumento, client)
    progresso: Database = database['progresso_da_insercao']
    progressoDocument: ReturnDocument = progresso.find_one()
    return progressoDocument
    
    
def get_etapas(instrumento: str, client: MongoClient) -> ReturnDocument:
    """
    Pega a Collection que contém as etapas do instrumento selecionado.
    
    Args:
        instrumento (str): Nome do instrumento/database que será pego a Collection.
        client (MongoClient): client proveniente do mongo.
    Returns:
        etapasDocument: Retorna um documento contendo as etapas do instrumento. 
    """
    
    dbName, database = connectToDatabase(instrumento, client)
    etapas: Database = database['etapas']
    etapasDocument: ReturnDocument = etapas.find_one()
    return etapasDocument


def atualiza_etapa(instrumento: str, etapa: str, novoValor: bool, client: MongoClient) -> str:
    """
    Atualiza o valor de uma etapa na Collection Etapas.
    
    Args:
        instrumento (str): Nome do instrumento/database que será pego a Collection.
        etapa (str): Nome da etapa que será alterada.
        novoValor (bool): Contém o novo valor booleano da etapa.
        client (MongoClient): client proveniente do mongo.
    Returns:
        String: Retorna uma str como uma response.
    """
    dbName, database = connectToDatabase(instrumento, client)
    etapas: Database = database['etapas']
    try:
        etapas.update_one({}, 
            {'$set':
                {
                    f'{etapa}': f'{novoValor}'        
                }}
        )
        return 'Sucesso'
    except (DuplicateKeyError, OperationFailure) as db_error:
        return error_response('Erro ao atualizar etapa', details=db_error)
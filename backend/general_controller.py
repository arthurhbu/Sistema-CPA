from pymongo import errors
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import MongoClient
from database.connectionDB import connectToDatabase 
from src.csvManipulationFunctions.CSVManager import *
from src.generationFunctions.mainGenerator import *
from src.generationFunctions.relatório.gerarRelatorio import gerarRelatorioPorCurso
from database.databaseQuerys import dfCursosPorCentro,dfCentroPorAno
from database.pythonMongoConfig import readDBConfig
from database.databaseQuerys import update_progresso


# def initializeBD(databaseName):
#     #Inicializando conexão com o banco de dados
#     dbName, database = connectToDatabase(databaseName)
#     return dbName, database
#     #Criando as collections que serão usadas (OBS: REALIZAR MUDANÇA BASEADA NO ANO, EX: centro_e_curso_{ano})


def initalizeDatabaseInserts(databaseName: Database, collectionCurso: Collection, collectionCentroeCurso: Collection, collectionDiretoreCentro: Collection, csvFileName: str, client: MongoClient, progresso: Database, etapas: Database) -> None:
    """
    Função que junta os primeiros passos da execução do programa que seria as inserções e os realiza de uma vez.
    """

    #Inserir CSVs no banco de dados
    progresso.insert_one(
        {
            'instrumento': f'{databaseName}',
            'Insercao_Main_CSV': 'Pendente',
            'Insercao_Curso_Centro_Database': 'Pendente',
            'Insercao_Centro_Diretor_Database': 'Pendente',
            'Geracao_de_Dados': 'Pendente',
            'Criacao_Cursos_por_Centro_Database': 'Pendente',
            'Criacao_Centro_por_Ano_Database': 'Pendente'
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
    
    progressoEtapa1 = CSVManagment.insertMainCSVtoDatabase(collectionCurso, csvFileName)
    update_progresso(progresso, 'Insercao_Main_CSV', progressoEtapa1)
    
    progressoEtapa2 = CSVManagment.insertCursoeCentroCSVtoDatabase(collectionCentroeCurso) 
    update_progresso(progresso, 'Insercao_Curso_Centro_Database', progressoEtapa2)
    
    progressoEtapa3 = CSVManagment.insertCentroDiretorCSVDatabase(collectionDiretoreCentro)  
    update_progresso(progresso, 'Insercao_Centro_Diretor_Database', progressoEtapa3)

    #Gerar Gráfico, Tabela e Relatório
    progressoEtapa4 = gerarGrafTabRelatorioGPT(client, databaseName, collectionCurso)
    update_progresso(progresso, 'Geracao_de_Dados', progressoEtapa4)
    


def prepareDataframesForReports(database: Database, collectionCursoseCentros: Collection, ano: int, collectionCurso: Collection, modal: str) -> None:
    """
    Realiza a criação dos dataframes intermediários que são utilizados para a criação de da introdução e 
    conclusão. E os insere em uma collection no banco de dados.

    :param database: Conexão com o banco de dados.
    :type database: Database
    :param ano: Contém o ano que é uma condition para escolhida que tem relação com o ano do arquivo csv
    será feito a leitra.
    :type ano: Integer
    :param collectionCurso: Nome da collection que contém as informações do csv principal.
    :type collectionCurso: Collection (MongoDB)    
    """

    #Preprocessamento
    centros = collectionCurso.distinct('centro_de_ensino')
    print(centros)

    document_to_insert = []

    for centro in centros:
        document_to_insert.extend(dfCursosPorCentro(collectionCursoseCentros, ano, centro))
    database['cursos_por_centro'].insert_many(document_to_insert)   

    dfCentroPorAno(collectionCurso, database, ano, modal)

def generateReports(collectionCurso: Collection, collectionCentroPorAno: Collection, collectionCursosPorCentro: Collection, ano: int, dbName: str, modal: str) -> None:
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
     # opcoes = [1,2,3]

    # # escolha = int(input('Escolha quantos relatorios você quer gerar com base nas opções: \n 1- Gerar relatórios por centro \n 2- Gerar relatório único \n 3- Gerar todos relatórios\n Escolha: '))
    # escolha = 3
    # if escolha not in opcoes:
    #     print('Digite uma opção válida!')

    # if escolha == 1:
    #     centro = str(input('Digite o nome do centro que gostaria de criar os relatórios: '))    
    #     gerarRelatoriosPorCentro(collectionCurso, collectionCentroPorAno, collectionCursosPorCentro, 'introducao.md', 'conclusao.md', ano, centro, dbName)
    # if escolha == 2:
    #     # curso = str(input('Digite o nome do curso que gostaria de gerar relatório: '))
    #     curso = 'Administração'
    #     gerarUmRelatorio(collectionCurso, collectionCentroPorAno, collectionCursosPorCentro, 'introducao.md', 'conclusao.md', ano, curso, dbName)
    # if escolha == 3:
    if modal == 'EAD':
        arquivo_intro_esc = 'introducao_ead.md'
        arquivo_conclusao_esc = 'conclusao_ead.md'
    elif modal == 'DISC':
        arquivo_intro_esc = 'introducao.md'
        arquivo_conclusao_esc = 'conclusao.md'
    else: 
        return print('O modal escolhido não existe, por favor, escolha entre EAD ou DISC por enquanto...')
    gerarTodosRelatorios(collectionCurso, collectionCentroPorAno, collectionCursosPorCentro, arquivo_intro_esc, arquivo_conclusao_esc, ano, dbName)

def applicationController(ano: int, csvFileName: str, modal: str, modo: str, client: MongoClient) -> None:
    """
    Junta todos os passos das funções acima e os realiza em ordem.
    """
    
    dbName, database = connectToDatabase(csvFileName, client)
    curso = database['curso']
    cursos_e_centros = database['cursos_e_centros']
    centros_e_diretores = database['centros_e_diretores']
    cursos_por_centro = database['cursos_por_centro']
    centro_por_ano = database['centro_por_ano'] 
    progresso = database['progresso_da_insercao']
    etapas = database['etapas']
    
    if modo == 'inserir':
        initalizeDatabaseInserts(dbName, curso, cursos_e_centros, centros_e_diretores, csvFileName, client, progresso, etapas)
        prepareDataframesForReports(database, cursos_e_centros, ano, curso, modal)
    if modo == 'gerarRelatorio':
        generateReports(curso, centro_por_ano, cursos_por_centro, ano, dbName, modal)

def listDatabases(client): 
    dbs = client.list_database_names()
    usersDatabases = [db for db in dbs if db not in ['admin', 'config', 'local']]
    return usersDatabases

def getProgressoInsercao(instrumento: str, client: MongoClient):
    dbName, database = connectToDatabase(instrumento, client)
    progresso = database['progresso']
    progressoDocument = progresso.find_one()
    return progressoDocument
    
def getEtapas(instrumento: str, client: MongoClient):
    dbName, database = connectToDatabase(instrumento, client)
    etapas = database['etapas']
    etapasDocument = etapas.find_one()
    return etapasDocument

def atualizaEtapa(instrumento: str, etapa: str, novoValor: bool, client: MongoClient):
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
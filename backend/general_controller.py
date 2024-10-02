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


# def initializeBD(databaseName):
#     #Inicializando conexão com o banco de dados
#     dbName, database = connectToDatabase(databaseName)
#     return dbName, database
#     #Criando as collections que serão usadas (OBS: REALIZAR MUDANÇA BASEADA NO ANO, EX: centro_e_curso_{ano})


def firstStepApplication(databaseName: Database, collectionCurso: Collection, collectionCentroeCurso: Collection, collectionDiretoreCentro: Collection, csvFileName: str, client: MongoClient) -> None:
    """
    Função que junta os primeiros passos da execução do programa que seria as inserções e os realiza de uma vez.
    """

    #Inserir CSVs no banco de dados
    
    CSVManagment.insertMainCSVtoDatabase(collectionCurso, csvFileName)
    CSVManagment.insertCursoeCentroCSVtoDatabase(collectionCentroeCurso) 
    CSVManagment.insertCentroDiretorCSVDatabase(collectionDiretoreCentro)  

    #Gerar Gráfico, Tabela e Relatório
    gerarGrafTabRelatorioGPT(client, databaseName, collectionCurso)
    


def preprocessing(database: Database, collectionCursoseCentros: Collection, ano: int, collectionCurso: Collection, modal: str) -> None:
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

def geraçãoDeRelatorio(collectionCurso: Collection, collectionCentroPorAno: Collection, collectionCursosPorCentro: Collection, ano: int, dbName: str, modal: str) -> None:
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
    opcoes = [1,2,3]

    # escolha = int(input('Escolha quantos relatorios você quer gerar com base nas opções: \n 1- Gerar relatórios por centro \n 2- Gerar relatório único \n 3- Gerar todos relatórios\n Escolha: '))
    escolha = 3
    if escolha not in opcoes:
        print('Digite uma opção válida!')

    if escolha == 1:
        centro = str(input('Digite o nome do centro que gostaria de criar os relatórios: '))    
        gerarRelatoriosPorCentro(collectionCurso, collectionCentroPorAno, collectionCursosPorCentro, 'introducao.md', 'conclusao.md', ano, centro, dbName)
    if escolha == 2:
        # curso = str(input('Digite o nome do curso que gostaria de gerar relatório: '))
        curso = 'Administração'
        gerarUmRelatorio(collectionCurso, collectionCentroPorAno, collectionCursosPorCentro, 'introducao.md', 'conclusao.md', ano, curso, dbName)
    if escolha == 3:
        if modal == 'EAD':
            arquivo_intro_esc = 'introducao_ead.md'
            arquivo_conclusao_esc = 'conclusao_ead.md'
        elif modal == 'DISC':
            arquivo_intro_esc = 'introducao.md'
            arquivo_conclusao_esc = 'conclusao.md'
        else: 
            return print('O modal escolhido não existe, por favor, escolha entre EAD ou DISC por enquanto...')
        gerarTodosRelatorios(collectionCurso, collectionCentroPorAno, collectionCursosPorCentro, arquivo_intro_esc, arquivo_conclusao_esc, ano, dbName)

def runAplication(ano: int, csvFileName: str, modal: str, modo: str) -> None:
    """
    Junta todos os passos das funções acima e os realiza em ordem.
    """
    db_config = readDBConfig()
    client = connection(db_config)
    dbName, database = connectToDatabase(csvFileName, client)
    curso = database['curso']
    cursos_e_centros = database['cursos_e_centros']
    centros_e_diretores = database['centros_e_diretores']
    cursos_por_centro = database['cursos_por_centro']
    centro_por_ano = database['centro_por_ano'] 
    
    # count = 0
    # count2  = 0
    # count3 = 0
    # for document in curso.find({'path': {'$regex': '^`'}}):
    #     count += 1
    # #2549
    # print('Contagem para saber se o número de figuras geradas bate com o numero de paths',count)

    # for document in curso.find({'relatorioGraficoAI': '-' }):
    #     count2 += 1
    # print('Contagem para saber quantos documentos não possuem relatorioGraficoAI', count2)
    
    # for document in curso.find({'nm_disciplina': '-' }):
    #     count3 += 1
    # print('Contagem para saber quantos documentos possuem nm_disciplina igual a -', count3)
    
    if modo == 'inserir':
        firstStepApplication(dbName, curso, cursos_e_centros, centros_e_diretores, csvFileName, client)
        preprocessing(database, cursos_e_centros, ano, curso, modal)
    # else:
    # geraçãoDeRelatorio(curso, centro_por_ano, cursos_por_centro, ano, dbName, modal)


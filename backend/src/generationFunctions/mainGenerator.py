from src.supportFunctions.dictToTwoLists import dictToList
from src.generationFunctions.graph.graphGenerator import controllerGraphGenerator
from src.generationFunctions.text.textFunctions import composeTable
from src.gemma2.generationFunctions import createReport
from src.generationFunctions.relatório.comporPartesRelatorio import *
from src.generationFunctions.relatório.gerarRelatorio import gerarRelatorioPorCurso
from src.supportFunctions.ordenarOpcoes import ordenarOpcoesDict
from datetime import datetime, timedelta
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from database.connectionDB import connection
import random as rand
import sys
sys.stdout.reconfigure(encoding="utf-8")



def gerarGrafTabRelatorioGPT(client: MongoClient, databaseName: Database, collectionName: Collection) -> None:
    """ 
    Função controller que chama as outras funções para gerar o gráfico, a tabela e as legendas e reports para o relatório

    :param CollectionName: Paramêtro que chama a collection na qual estamos trabalhando
    :type CollectionName: Collection
    """
    # with client.start_session() as session:
    #     session_id = session.session_id

    #     cursor = collectionName.find({'tabela': {'$exists': False}}, no_cursor_timeout = True, session=session).batch_size(10)
        
    #     refresh_timeStamp = datetime.now()
    #     try:
    #         for document in cursor:
    #             if (datetime.now() - refresh_timeStamp).total_seconds() > 300:
    #                 client.admin.command({'refreshSessions': [session_id]})
    #                 refresh_timeStamp = datetime.now()

    #             pergunta_formatada = re.sub(r"^\d+\.\d+-\s*",'',document["nm_pergunta"])
    #             sorted_pctOptDict = dict(sorted(document["pct_por_opcao"].items(), key=lambda x: x[1], reverse=True))
    #             opcoes, pct = dictToList(sorted_pctOptDict)
    #             table = composeTable(pergunta_formatada, sorted_pctOptDict, document['total_do_curso'])
    #             path = '-'
    #             captionGraph = '-'
    #             reportGraph = '-'

    #             if document['nm_disciplina'] == '-':
    #                 path = controllerGraphGenerator(databaseName, collectionName, opcoes, pct, document["cd_curso"], document["cd_subgrupo"], document["cd_pergunta"], pergunta_formatada)
    #                 reportGraph = createReport(pergunta_formatada, sorted_pctOptDict) 
                    
    #                 collectionName.update_one(
    #                     {
    #                         "cd_curso": document["cd_curso"],
    #                         "cd_subgrupo": document['cd_subgrupo'],
    #                         "cd_pergunta": document["cd_pergunta"]
    #                     },
    #                     {
    #                         '$set': {
    #                             'path': path,
    #                             'tabela': table,
    #                             'relatorioGraficoAI': reportGraph,
    #                             'tituloGraficoAI': captionGraph
    #                         }
    #                     }   
    #                 )
    #                 continue
                
    #             collectionName.update_one(
    #                 {
    #                     'cd_curso': document['cd_curso'],
    #                     'cd_pergunta': document['cd_pergunta'],
    #                     'cd_disciplina': document['cd_disciplina']
    #                 },
    #                 {
    #                     '$set': {
    #                         'path': path,
    #                         'tabela': table,
    #                         'relatorioGraficoAI': reportGraph,
    #                         'tituloGraficoAI': captionGraph
    #                     }
    #                 }
    #             )
    #     finally:
    #         cursor.close()


    #PARA MEXER NA TABELA E RELATORIOAI(ALTERAR O FINAL DO RELATORIO ADICIONANDO NOVA FRASE)
    # for document in collectionName.find({}):
    #     pergunta_formatada = re.sub(r"^\d+\.\d+-\s*",'',document["nm_pergunta"])
    #     sorted_pctOptDict = dict(sorted(document["pct_por_opcao"].items(), key=lambda x: x[1], reverse=True))
    #     table = composeTable(pergunta_formatada, document['pct_por_opcao'], document['total_do_curso'])
    #     if document['nm_disciplina'] == '-':
    #         referencia_figura = rand.choice(['A figura index_ demonstra a prevalência das respostas.', 'A figura index_ mostra a tendência dominante das respostas.', 'A figura index_ representa a maior frequência das respostas.', 'A figura index_ exibe o padrão predominante nas respostas.','A figura index_ destaca a maior concentração de respostas.', 'A figura index_ evidencia a principal tendência nas respostas.', 'A figura index_ revela o comportamento predominante das respostas.', 'A figura index_ exibe a distribuição dos respondentes.', 'A figura index_ demonstra o padrão de distribuição dos respondentes.', 'A figura index_ representa a distribuição dos respondentes.'])

    #         relatorio_mudanca = document['relatorioGraficoAI']
    #         relatorio_mudanca = f'{relatorio_mudanca}{referencia_figura}'
    #     collectionName.update_one(
    #         {
    #             "cd_curso": document["cd_curso"],
    #             "cd_subgrupo": document['cd_subgrupo'],
    #             "cd_pergunta": document["cd_pergunta"]
    #         },
    #         {
    #             '$set': {
    #                 'tabela': table,
    #                 'relatorioGraficoAI': relatorio_mudanca
    #             }
    #         }   
    #     )



    #PARA APENAS SUBSTITUIR TABELAS
    for document in collectionName.find({}):
        pergunta_formatada = re.sub(r"^\d+\.\d+-\s*",'',document["nm_pergunta"])
        sorted_pctOptDict = dict(sorted(document["pct_por_opcao"].items(), key=lambda x: x[1], reverse=True))
        table = composeTable(pergunta_formatada, document['pct_por_opcao'], document['total_do_curso'])
        collectionName.update_one(
            {
                "cd_curso": document["cd_curso"],
                "cd_subgrupo": document['cd_subgrupo'],
                "cd_pergunta": document["cd_pergunta"]
            },
            {
                '$set': {
                    'tabela': table
                }
            }   
        )



    #PARA SUBSTITUIR PATHS E GRÁFICOS
    # for document in collectionName.find({}):
    #     pergunta_formatada = re.sub(r"^\d+\.\d+-\s*",'',document["nm_pergunta"])
    #     sorted_pctOptDict = dict(sorted(document["pct_por_opcao"].items(), key=lambda x: x[1], reverse=True))
    #     opcoes, pct = dictToList(sorted_pctOptDict)
    #     path = '-'
    #     captionGraph = '-'
    #     reportGraph = '-'

    #     if document['nm_disciplina'] == '-':
    #         path = controllerGraphGenerator(databaseName, collectionName, opcoes, pct, document["cd_curso"], document["cd_subgrupo"], document["cd_pergunta"], pergunta_formatada)
            
    #         collectionName.update_one(
    #             {
    #                 "cd_curso": document["cd_curso"],
    #                 "cd_subgrupo": document['cd_subgrupo'],
    #                 "cd_pergunta": document["cd_pergunta"]
    #             },
    #             {
    #                 '$set': {
    #                     'path': path
    #                 }
    #             }   
    #         )
    #         continue

    # ATUALIZAR DICTS FORA DE ORDEM
    # for document in collectionName.find({}):
    #     lista = ['Excelente','Ótimo', 'Bom', 'Regular', 'Ruim', 'Péssimo','Não sei informar']
    #     dictOrd = ordenarOpcoesDict(document['pct_por_opcao'], lista)
    #     collectionName.update_one(
    #         {
    #             "cd_curso": document["cd_curso"],
    #             "cd_subgrupo": document['cd_subgrupo'],
    #             "cd_pergunta": document["cd_pergunta"]
    #         },
    #         {
    #             '$set': {
    #                 'pct_por_opcao': dictOrd
    #             }
    #         }  
    #     )        



def gerarTodosRelatorios(collectionCurso: Collection, collectionCentroPorAno: Collection, collectionCursosPorCentro: Collection, arquivo_intro: str, arquivo_conclusao: str, ano: int, dbName: str) -> None:
    """
    Gera relatório de todos os cursos.

    :param collectionCurso: Nome da collection que contém as informações do csv principal.
    :type collectionCurso: Collection (MongoDB)     
    :param collectionCentroPorAno: Nome da collection que contém as informações sobre os centros.
    :type: Collection (MongoDB)
    :param CollectionCursosPorCentro: Nome da collection que contém informações sobre os cursos de um centro.
    :type: Collection (MongoDB)
    :param arquivo_intro: Nome do arquivo que contém o template da introdução do relatório
    :type: String
    :param arquivo_conclusao: Nome do arquivo que contém o template de conclusão do relatório 
    :type arquivo_conclusao: String
    :param ano: O ano de que será feito o relatório.
    :type ano: Integer
    :param dbName: Nome do banco de dados que está sendo manipulado
    :type dbName: str
    """
    centros = collectionCurso.distinct('centro_de_ensino')
    for centro in centros:
        gerarRelatoriosPorCentro(collectionCurso, collectionCentroPorAno, collectionCursosPorCentro, arquivo_intro, arquivo_conclusao, ano, centro, dbName)

        


def gerarRelatoriosPorCentro(collectionCurso: Collection, collectionCentroPorAno: Collection, collectionCursosPorCentro: Collection, arquivo_intro: str, arquivo_conclusao: str, ano: int, centro_de_ensino: str, dbName: str) -> None:
    """
    Gera relatórios dos cursos pertencentes a um centro.

    :param collectionCurso: Nome da collection que contém as informações do csv principal.
    :type collectionCurso: Collection (MongoDB)     
    :param collectionCentroPorAno: Nome da collection que contém as informações sobre os centros.
    :param CollectionCursosPorCentro: Nome da collection que contém informações sobre os cursos de um centro.
    :type: Collection (MongoDB)
    :param arquivo_intro: Nome do arquivo que contém o template da introdução do relatório
    :type: String
    :param arquivo_conclusao: Nome do arquivo que contém o template de conclusão do relatório 
    :type arquivo_conclusao: String
    :param ano: O ano de que será feito o relatório.
    :type ano: Integer
    :param centro_de_ensino: Centro de ensino escolhido para gerar os relatórios dos cursos pertencentes ao mesmo
    :type centro_de_ensino: String
    :param dbName: Nome do banco de dados que está sendo manipulado
    :type dbName: str
    """
    comporIntroducao(collectionCentroPorAno, collectionCursosPorCentro, arquivo_intro, ano, centro_de_ensino)
    comporConclusao(collectionCursosPorCentro, arquivo_conclusao, ano)

    cursos = collectionCurso.distinct('nm_curso', {'centro_de_ensino': centro_de_ensino})
    print(cursos)
    for curso in cursos:
        gerarRelatorioPorCurso(curso, collectionCurso, collectionCursosPorCentro, dbName)
        cursoArquivo = f'{curso}.md'
        substituirIdentificadores(cursoArquivo, dbName)



def gerarUmRelatorio(collectionCurso: Collection, collectionCentroPorAno: Collection, collectionCursosPorCentro: Collection, arquivo_intro: str, arquivo_conclusao: str, ano: int, curso: str, dbName: str): # type: ignore

    print(curso)
    document = collectionCurso.find_one(
        {'nm_curso': curso},
    )
    print(document['centro_de_ensino'])

    comporIntroducao(collectionCentroPorAno, collectionCursosPorCentro, arquivo_intro, ano, document['centro_de_ensino'])
    comporConclusao(collectionCursosPorCentro, arquivo_conclusao, ano)
    gerarRelatorioPorCurso(curso, collectionCurso, collectionCursosPorCentro, dbName)
    cursoArquivo = f'{curso}.md'
    substituirIdentificadores(cursoArquivo, dbName)

    

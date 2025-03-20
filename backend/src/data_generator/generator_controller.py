from src.utils.dict_to_two_lists import dict_to_list
from src.data_generator.graph.graph_generator import controller_graph_generator
from src.data_generator.text.text_functions import compose_table
from src.ollama.ollama import create_report
from datetime import datetime
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from pymongo.errors import OperationFailure, CursorNotFound, ConnectionFailure, InvalidOperation, DuplicateKeyError
import random as rand
import sys
import re
sys.stdout.reconfigure(encoding="utf-8")



def generate_graph_table_report(client: MongoClient, database_name: Database, collection_name: Collection) -> None:
    """ 
    Função controller que chama as outras funções para gerar o gráfico, a tabela e as legendas e reports para o relatório

    :param CollectionName: Paramêtro que chama a collection na qual estamos trabalhando
    :type CollectionName: Collection
    """
    try:
        with client.start_session() as session:
            session_id = session.session_id

            cursor = collection_name.find({'tabela': {'$exists': False}}, no_cursor_timeout = True, session=session).batch_size(10)
            
            
            refresh_timeStamp = datetime.now()
            
            try:
                for document in cursor:
                    if (datetime.now() - refresh_timeStamp).total_seconds() > 300:
                        client.admin.command({'refreshSessions': [session_id]})
                        refresh_timeStamp = datetime.now()
                    pergunta_formatada = re.sub(r"^\d+\.\d+-\s*",'',document["nm_pergunta"])
                    try:
                        sorted_pctOptDict = dict(sorted(document["pct_por_opcao"].items(), key=lambda x: x[1], reverse=True))
                        opcoes, pct = dict_to_list(sorted_pctOptDict)
                        table = compose_table(pergunta_formatada, document['pct_por_opcao'], document['total_do_curso'])
                    except KeyError as key_error:
                        return f'Erro de chave: {key_error}'
                    
                    path = '-'
                    caption_graph = '-'
                    report_graph = '-'

                    if document['nm_disciplina'] == '-':
                        try:
                            path = controller_graph_generator(database_name, collection_name, opcoes, pct, document["cd_curso"], document["cd_subgrupo"], document["cd_pergunta"], pergunta_formatada)
                            report_graph = create_report(pergunta_formatada, sorted_pctOptDict) 
                        except (ValueError, RuntimeError, OSError) as graph_error:
                            return f'Erro ao gerar ou gravar gráfico: {graph_error}'
                        
                        try: 
                            collection_name.update_one(
                                {
                                    "cd_curso": document["cd_curso"],
                                    "cd_subgrupo": document['cd_subgrupo'],
                                    "cd_pergunta": document["cd_pergunta"]
                                },
                                {
                                    '$set': {
                                        'path': path,
                                        'tabela': table,
                                        'relatorioGraficoAI': report_graph,
                                        'tituloGraficoAI': caption_graph
                                    }
                                }   
                            )
                        except (DuplicateKeyError, OperationFailure) as db_error:
                            return f'Erro no banco de dados: {db_error}'
                        continue
                    
                    try:
                        collection_name.update_one(
                            {
                                'cd_curso': document['cd_curso'],
                                'cd_pergunta': document['cd_pergunta'],
                                'cd_disciplina': document['cd_disciplina']
                            },
                            {
                                '$set': {
                                    'path': path,
                                    'tabela': table,
                                    'relatorioGraficoAI': report_graph,
                                    'tituloGraficoAI': caption_graph
                                }
                            }
                        )
                    except (DuplicateKeyError, OperationFailure) as db_error:
                        return f'Erro no banco de dados: {db_error}'
                    
                return 'Finalizado'
            except Exception as e:
                print(f'Erro: {e}')
            finally:
                cursor.close()
                
    except (ConnectionFailure, InvalidOperation, CursorNotFound) as mongo_error:
        return f'Erro de conexão ou operação com MongoDB: {mongo_error}'


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
    # for document in collectionName.find({}):
    #     pergunta_formatada = re.sub(r"^\d+\.\d+-\s*",'',document["nm_pergunta"])
    #     sorted_pctOptDict = dict(sorted(document["pct_por_opcao"].items(), key=lambda x: x[1], reverse=True))
    #     table = composeTable(pergunta_formatada, document['pct_por_opcao'], document['total_do_curso'])
    #     collectionName.update_one(
    #         {
    #             "cd_curso": document["cd_curso"],
    #             "cd_subgrupo": document['cd_subgrupo'],
    #             "cd_pergunta": document["cd_pergunta"]
    #         },
    #         {
    #             '$set': {
    #                 'tabela': table
    #             }
    #         }   
    #     )



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


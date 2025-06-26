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
from pymongo import CursorType
from typing import Union
import sys
import re
sys.stdout.reconfigure(encoding="utf-8")
import logging

logger = logging.getLogger(__name__)

def generate_graph_table_report(mongo_client, database_name: str, collection: Collection) -> str:
    """
    Gera relatórios de gráficos e tabelas para documentos não processados.
    
    Args:
        mongo_client: Cliente MongoDB
        database_name: Nome do banco de dados
        collection: Collection do MongoDB contendo os dados
        
    Returns:
        str: Mensagem indicando o resultado do processamento
    """
    try:
        # Busca documentos não processados
        documentos = collection.find({'processado': False})
        total_docs = collection.count_documents({'processado': False})
        
        if total_docs == 0:
            logger.info("Nenhum documento não processado encontrado")
            return 'Finalizado'
            
        logger.info(f"Encontrados {total_docs} documentos não processados")
        
        # Processa cada documento
        for doc in documentos:
            try:
                # Extrai dados do documento
                cd_curso = doc.get('cd_curso')
                cd_subgrupo = doc.get('cd_subgrupo')
                cd_pergunta = doc.get('cd_pergunta')
                nm_pergunta = doc.get('nm_pergunta')
                pct_por_opcao = doc.get('pct_por_opcao', {})
                
                if not all([cd_curso, cd_subgrupo, cd_pergunta, nm_pergunta, pct_por_opcao]):
                    logger.warning(f"Documento {doc.get('_id')} está incompleto, pulando...")
                    continue
                
                # Prepara dados para o gráfico
                opcoes = list(pct_por_opcao.keys())
                porcentagens = list(pct_por_opcao.values())
                
                # Gera o gráfico
                logger.info(f"Gerando gráfico para pergunta {cd_pergunta}")
                path_figura = controller_graph_generator(
                    database_name,  # Passando o nome do banco de dados
                    collection,
                    opcoes,
                    porcentagens,
                    cd_curso,
                    cd_subgrupo,
                    cd_pergunta,
                    nm_pergunta
                )
                
                # Marca o documento como processado
                result = collection.update_one(
                    {'_id': doc['_id']},
                    {'$set': {'processado': True}}
                )
                
                if result.modified_count == 0:
                    logger.error(f"Falha ao marcar documento {doc['_id']} como processado")
                    return f"Erro ao atualizar status do documento {doc['_id']}"
                    
                logger.info(f"Documento {doc['_id']} processado com sucesso")
                
            except Exception as e:
                logger.error(f"Erro ao processar documento {doc.get('_id')}: {str(e)}")
                return f"Erro ao processar documento: {str(e)}"
                
        return 'Finalizado'
        
    except Exception as e:
        logger.error(f"Erro ao gerar relatórios: {str(e)}")
        return f"Erro ao gerar relatórios: {str(e)}"


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


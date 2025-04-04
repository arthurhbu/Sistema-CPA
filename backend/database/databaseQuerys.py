from pymongo.database import Database
from pymongo.collection import Collection

def df_cursos_por_centro(collection_cursos_e_centros: Collection, ano: int, centro_de_ensino: str) -> dict:
    """
    Realiza uma Query no padrão do mongoDB para criar o database cursos_por_centro que possui informações em relação aos cursos e seus centros.
    
    Args:
        collection_cursos_e_centros (Collection): Collection que possui informações que serão usadas para gerar esse novo database.
        ano (int): Ano do instrumento que está sendo gerado.
        centro_de_ensino (str): Nome do Centro de Ensino da UEM que gerará as informações.
    Returns:
        dict: A função retorna um dict contendo se a etapa foi bem sucedida, caso não tenha sido, ele retorna a Exception gerada.
    Raises:
        Raise: A função não levanta nenhuma exceção, apenas repassa as exceções que ocorreram antes.
    """
    try:
        results = list(collection_cursos_e_centros.aggregate([
        {
            "$lookup": {
                "from": "instrumento",
                "localField": "cd_curso",
                "foreignField": "cd_curso",
                "as": "curso"
            }
        },
        {
            "$unwind": "$curso"
        },
        {
            "$match": {
                "ano_referencia": ano,
                "centro_de_ensino": centro_de_ensino
            }
        },
        {
            "$group": {
                "_id": "$cd_curso",
                "nm_curso": {"$first": "$nm_curso"},
                "centro_de_ensino": {"$first": "$centro_de_ensino"},
                "matriculados": {"$first": "$matriculados"},
                "total_do_curso": {"$max": "$curso.total_do_curso"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "nm_curso": 1,
                "centro_de_ensino": 1,
                "respondentes": "$total_do_curso",
                "matriculados": 1,
                "porcentagem": {
                    "$cond": {
                        "if": {"$eq": ["$matriculados", 0]},
                        "then": 0,
                        "else": {
                            "$round": [
                                {
                                    "$multiply": [
                                        {"$divide": ["$total_do_curso", "$matriculados"]},
                                        100
                                    ]
                                },
                                2
                            ]
                        }
                    }
                }
            }
        },
        {
            "$sort": {"nm_curso": 1}
        }
        ]))
        return {'Success': True, 'resultado': results}
    except Exception as e:
        return {'Success': False, 'error': f'Ocorreu um erro ao tentar criar Collection cursos_por_centro. Erro: {e}'}


def df_centro_por_ano(collection_instrumento: Collection, database: Database, ano: int):
    """
    Realiza uma Query no padrão do mongoDB para criar o database centro_por_ano que possui informações em relação ao centro e o ano do instrumento.
    
    Args:
        collection_instrumento (Collection): Collection principal do instrumento.
        database (Database): Conexão do database/instrumento que está sendo utilizado.
        ano (int): Ano do instrumento que está sendo gerado.
    Returns:
        dict: A função retorna um dict contendo se a etapa foi bem sucedida, caso não tenha sido, ele retorna a Exception gerada.
    Raises:
        Raise: A função não levanta nenhuma exceção, apenas repassa as exceções que ocorreram antes.
    """    

    centro_por_ano_temp = database['centro_por_ano_temp']

    try:
        collection_instrumento.aggregate([
            {   
                "$lookup": {
                "from": "cursos_e_centros",
                "localField": "cd_curso",
                "foreignField": "cd_curso",
                "as": "cursos_e_centros"
                }
            },
            {
                "$unwind": "$cursos_e_centros"
            },
            {
                "$match": {
                    "cursos_e_centros.ano_referencia": ano 
                }
            },
            {
                "$group": {
                    "_id": "$nm_curso",
                    "respondentes": {"$max": "$total_do_curso"},
                    "centro_de_ensino": {'$first': '$cursos_e_centros.centro_de_ensino'},
                    "matriculados": {'$first': "$cursos_e_centros.matriculados"},
                }
            },
            {
                '$addFields': {
                    'centro_de_ensino': '$centro_de_ensino'
                }
            },
            {
                '$project': {
                    '_id': 1,
                    'centro_de_ensino': 1,
                    'respondentes': 1,
                    'matriculados': 1,
                }
            },
            {
                '$out':'centro_por_ano_temp'
            }
        ])
        

        centro_por_ano_temp.aggregate(
            [
                {
                    '$lookup':{
                        "from": "centros_e_diretores",
                        "localField": "centro_de_ensino",
                        "foreignField": "centro_de_ensino",
                        "as": "centros_e_diretores"
                    }
                },
                {
                    "$unwind": "$centros_e_diretores"
                },
                {
                    "$group": {
                        "_id": "$centro_de_ensino",
                        "centro_descricao": {"$first": "$centros_e_diretores.centro_descricao"},
                        "respondentes": {"$sum": "$respondentes"},
                        "matriculados": {"$sum": "$matriculados"},
                    }
                },
                {
                    "$addFields": {
                        "porcentagem": {
                            "$cond": {
                                "if": {"$or": [{"$eq": ["$matriculados", 0]}, {"$eq": ["$respondentes", 0]}]},
                                "then": 0,
                                "else": {
                                    "$round": [
                                        {
                                            "$multiply": [
                                                {"$divide": ["$respondentes", "$matriculados"]},
                                                100
                                            ]
                                        },
                                        2
                                    ]
                                }
                            }
                        }
                    }
                },
                {
                    '$project': {
                        '_id': 0,
                        'centro_de_ensino':'$_id',
                        'centro_descricao':1,
                        'respondentes': 1,
                        'matriculados':1,
                        'porcentagem': {'$round': ['$porcentagem', 2]}
                    }

                },
                {
                    "$sort": {"_id": 1}
                },
                {
                    '$out': f'centro_por_ano'
                }
                
            ]
        )
        centro_por_ano_temp.drop()
        return {'Success': True, 'message': 'Finalizado'}
    except Exception as e: 
        return {'Success': False, 'error': f'Ocorreu um erro ao tentar criar Collection centro_por_ano: {e}'}
    
def update_progresso(progresso: Database, etapa: str, resposta: str):
    if resposta == 'Finalizado':
        progresso.update_one(
            {
                f'{etapa}': 'Pendente'
            },
            {
                '$set': {
                    f'{etapa}': 'Finalizado'
                }
            }
        )
    else: 
            progresso.update_one(
            {
                f'{etapa}': 'Pendente'
            },
            {
                '$set': {
                    f'{etapa}': resposta
                }
            }
        )
from pymongo.collection import Collection
from typing import Union

def percentage_calculator(respostas: dict, total: int) -> dict:
    """
    Calcula o porcentagem com base na quantidade de respostas e o total.

    Args:
        respostas (dict): Dict contendo as opções e suas respectivas respostas.
        total (int): Valor total de respondentes.
    Returns:
        opcao_e_porcentagem (dict): Retorna um Dict contendo as opções e as porcentagens das respostas.
    Raises:
        None:
    """
    opcao_e_porcentagem = {}    
    for key, value in respostas.items():
        percentage = round((value*100)/total,2)
        opcao_e_porcentagem.update({key: percentage})
    
    return opcao_e_porcentagem

def insert_percentage_dict_into_database(collection_name: Collection, dict_name: str, option_percentage: dict, condition1: str, condition1_value: Union[str, int], condition2: str, condition2_value: Union[str, int]) -> None:
    """
    Insere um novo dict(dicionário) que contém a opção/porcentagem em cada documento da respectiva collection.

    Args:
        collection_name (Collection): Collection onde será inserido os dicts.
        dict_name (str): Nome que será dado para o dict.
        condition1 (str): Um valor condicional do documento para podermos realizar o update no mesmo.
        condition1_value (Union[str,int]): Valor respectivo da condition1.
        condition2 (str): Um segundo valor condicional do documento para podermos realizar o update no mesmo.
        condition2_value (Union[str,int]): Valor respectivo da condition2.
    Returns:
        None:
    Raises:
        None:
    """
    collection_name.update_one(
        {
            condition1: condition1_value,
            condition2: condition2_value 
        },
        {
            '$set': {dict_name: option_percentage}
        }
    )

def insert_dict_disciplina(collection_name: Collection, dict_name: str, option_percentage: dict, condition1: str, condition1_value: Union[str, int],    condition2: str, condition2_value: Union[str, int], condition3: str, condition3_value: Union[str, int]) -> None:

    collection_name.update_one(
        {
            condition1: condition1_value,
            condition2: condition2_value, 
            condition3: condition3_value
        },
        {
            '$set': {dict_name: option_percentage}
        }
    )


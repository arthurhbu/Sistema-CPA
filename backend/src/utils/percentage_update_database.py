from pymongo.collection import Collection
from typing import Union

def percentage_calculator(respostas: dict, total: int) -> dict:
    """
    Calcula o porcentagem com base na quantidade de respostas e o total

    :param repostas: Opção da reposta e sua respectiva quantidade de respostas
    :type respostas: Dict
    :param total: Quantidade total de respostas dadas 
    :type total: Int
    :return: Opções de resposta e as porcentagens calculadas
    :rtype: Dict
    """
    opcao_e_porcentagem = {}    
    for key, value in respostas.items():
        percentage = round((value*100)/total,2)
        opcao_e_porcentagem.update({key: percentage})
    
    return opcao_e_porcentagem

def insert_percentage_dict_into_database(collection_name: Collection, dict_name: str, option_percentage: dict, condition1: str, condition1_value: Union[str, int], condition2: str, condition2_value: Union[str, int]) -> None:
    """
    Insere um novo dict(dicionário) que contém a opção/porcentagem em cada documento da respectiva collection 

    :param collectionName: Coleção que contém os documentos que iremos realizar a inserção
    :type collectionName: Collection
    :param optPercentage: Contém as opções/Porcentagem de cada resposta
    :type optPercentage: Dict
    :param condition1 or condition2: Um valor condicional do documento para podermos realizar o update
    :type condition1 or condition2: String
    :param condition1Value or condition2Value: Valor respectivo do condition1
    :type Condition1Value or Condition2Value: String or Int
    :return: None
    :rtype: None
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

def insert_dict_disciplina(collection_name: Collection, dict_name: str, option_percentage: dict, condition1: str, condition1_value: Union[str, int], condition2: str, condition2_value: Union[str, int], condition3: str, condition3_value: Union[str, int]) -> None:

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


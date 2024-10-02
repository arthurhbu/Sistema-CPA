from pymongo.collection import Collection
from typing import Union

def percentageCalculator(respostas: dict, total: int) -> dict:
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

def insertPercentageDictIntoDB(collectionName: Collection, dictName: str, optPercentage: dict, condition1: str, condition1Value: Union[str, int], condition2: str, condition2Value: Union[str, int]) -> None:
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
    collectionName.update_one(
        {
            condition1: condition1Value,
            condition2: condition2Value
        },
        {
            '$set': {dictName: optPercentage}
        }
    )

def insertDictDisciplina(collectionName: Collection, dictName: str, optPercentage: dict, condition1: str, condition1Value: Union[str, int], condition2: str, condition2Value: Union[str, int], condition3: str, condition3Value: Union[str, int]) -> None:

    collectionName.update_one(
        {
            condition1: condition1Value,
            condition2: condition2Value, 
            condition3: condition3Value
        },
        {
            '$set': {dictName: optPercentage}
        }
    )

#FUNCAO SEM USO POR ENQUANTO
# def percentageDictGenerator(collectionName):
#     #Sem uso atualmente
    
#     """
#     Função que para documento gera um novo dict com a função percentageCalulcator e insere com a insertPercentageDictIntoDB

#     :param collectionName: Coleção que contém os documentos que realizamos a seleção de dados
#     :type collectionName: Collection
#     ;return: None
#     :rtype: None
#     """
#     cursor = collectionName.find({}, {'cd_curso': 1, 'cd_pergunta': 1, 'opcao_e_qtdResposta': 1, 'TotalResp_do_Curso': 24})
#     print('Atualizando dicionário de porcentagem no banco de dados...')
#     i = 0
#     for value in cursor:
#         print(f"Atualizando: {round((i*100)/collectionName.count_documents({}), 0)}%")
#         optPercentage = {'opcao_e_porcentagem': percentageCalculator(value['opcao_e_qtdResposta'], value['TotalResp_do_Curso'])}
#         insertPercentageDictIntoDB(collectionName, optPercentage, 'Codigo_Curso', value['Codigo_Curso'], 'nu_pergunta', value['nu_pergunta'])
#         i += 1 
#     print("Atualização da Collection finalizada ✅")

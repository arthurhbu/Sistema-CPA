
def dict_to_list(dictionary: dict) -> tuple[list[str], list[int]]:
    """
    Função que transforma um dict em uma list

    Args:
        dictionary (str): Um dict do python.
    Returns:
        keyList, valueList (tuple[list[str], list[int]]): Retorna duas lists que contém as chaves e seus respectivos valores no dict.
    Raises:
        None: 
    """
    keyList = []
    valueList = []
    for key,value in dictionary.items():
        keyList.append(key)
        valueList.append(value)
    return keyList, valueList

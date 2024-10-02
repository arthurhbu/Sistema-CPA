
def dictToList(dictionary) -> tuple[str, int]:
    """
    Função que transforma um dict em uma list

    :param dictionary: um dict
    :type dictionary: Dict
    return: Duas listas, uma contendo a key e outra contendo o valor
    """
    keyList = []
    valueList = []
    for key,value in dictionary.items():
        keyList.append(key)
        valueList.append(value)
    return keyList, valueList

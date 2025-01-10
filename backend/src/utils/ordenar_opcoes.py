def ordenar_opcoes_dict(dict_original: dict, lista_referencia: list) -> dict:
    """
    Função criada para corrigir exceções de erro de ordem nas opções do csv, ou seja, quando as opções vem fora da ordem requerida. 
    A função corrige apenas uma exceção por vez.

    :type dictOriginal: dict.
    :param dictOriginal: dicionário original do banco de dados.
    :type listaReferencia: list
    :param listaReferencia: lista contendo a ordem correta das opceos que deveria ter no dicionário.
    :type return: dict
    :param return: dicionário atualizado.x'

    """

    chaves_em_comum = [key for key in lista_referencia if key in dict_original]
    
    dict_ordenado = {key: dict_original[key] for key in chaves_em_comum}
    
    chaves_extras = {key: dict_original[key] for key in dict_original if key not in chaves_em_comum}
    
    dict_ordenado.update(chaves_extras)
    
    return dict_ordenado
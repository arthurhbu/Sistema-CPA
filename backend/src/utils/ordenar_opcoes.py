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

    # Filtra apenas as chaves que estão tanto no dict quanto na lista de referência
    chaves_em_comum = [key for key in lista_referencia if key in dict_original]
    
    # Ordena o dict conforme a ordem da lista de referência, sem perder chaves extras
    dict_ordenado = {key: dict_original[key] for key in chaves_em_comum}
    
    # Adiciona as chaves que não estão na lista de referência, mas estão no dicionário
    chaves_extras = {key: dict_original[key] for key in dict_original if key not in chaves_em_comum}
    
    # Combina as duas partes: ordenado e as chaves extras (sem ordem definida)
    dict_ordenado.update(chaves_extras)
    
    return dict_ordenado
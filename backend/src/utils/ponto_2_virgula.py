from typing import Union

def ponto_2_virgula(valor: Union[str, int]) -> str:
    '''
    Apenas dá replace em um valor, trocando '.'  por uma ',', muito utilizado para valores de porcentagem, pela diferença existente no brasil e outros países na hora de representar casas decimais.
    
    Args:
        valor (Union[str, int]): Valor que será feito a substituição.
    Retrurns:
        str: Retorna a string modficiada.
    Raises:
        None:
    '''
    return str(valor).replace(".",",")
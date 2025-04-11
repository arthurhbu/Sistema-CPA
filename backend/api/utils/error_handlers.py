'''
Handle para cuidar dos erros que serão gerados.
'''

def error_response(message:str , status_code:int=400, details:any=None):
    """
    Cria mensagem de erro padronizada.

    Args:
        message (str): Mensagem do erro que será gerada.
        status_code (int): Código do status do erro.
        details (any | str): Contém os detalhes do erro.
    Returns:
        tuple: (resposta JSON, status_code)
    """
    ...


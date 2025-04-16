from flask import jsonify

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
    response = {'error': message}
    if details: 
        response['details'] = details
    
    return jsonify(response), status_code


def validation_error(missing_fields=None):
    """
    Cria uma resposta de erro para validação de dados.
    
    Args:
        missing_fields (list): Campos que estão faltando na requisição.
    Returns:
        tuple: (Resposta JSON, status_code)
    """
    
    message = 'Erro de validação, verifique os dados enviados'
    details = {'missing_fields': missing_fields} if missing_fields else {}
    return error_response(message, 400, details)

def not_found_error(resource_type, resource_id=None):
    """
    Cria mensagem de erro para quando recursos não encontrados.
    
    Args: 
        resource_type (str): Tipo de recurso (ex: 'Instrumento', 'Arquivo')
        resource_id (str, optional): Identificador do recurso
    
    Returns:
        tuple: (resposta JSON, status_code)
    """
    message = f"{resource_type} não encotrado"
    if resource_id:
        message += f": {resource_id}"
    return error_response(message, 404)

def server_error(exception=None):
    """
    Cria uma resposta para erros internos do servidor.
    
    Args:
        exception (Exception, optional): A exceção que causou o erro
        
    Returns:
        tuple (reposta JSON, status_code)
    """
    message = 'Erro interno do servidor'
    details = str(exception) if exception else None
    return error_response(message, 500, details)

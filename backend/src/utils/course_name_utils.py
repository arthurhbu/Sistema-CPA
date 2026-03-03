"""
Utilitários para manipulação de nomes de cursos
"""

def generate_course_display_name(nm_curso: str, centro_de_ensino: str) -> str:
    """
    Gera nome do curso com tag identificadora para diferenciar modalidades
    
    Args:
        nm_curso (str): Nome original do curso
        centro_de_ensino (str): Centro/modalidade do curso
        
    Returns:
        str: Nome do curso com tag identificadora
    """
    # Mapear centros para tags identificadoras
    tags_modalidade = {
        'EAD': '[EAD]',
        'PARFOR': '[PARFOR]',
        'CCH': '[Presencial]',
        'CCA': '[Presencial]', 
        'CSA': '[Presencial]',
        'CTC': '[Presencial]',
        'CCE': '[Presencial]',
        'CCB': '[Presencial]',
        'CCS': '[Presencial]'
    }
    
    # Obter tag apropriada (padrão para presencial se não encontrar)
    tag = tags_modalidade.get(centro_de_ensino, '[Presencial]')
    
    # Limpar nome do curso (remover espaços extras)
    nome_limpo = nm_curso.strip()
    
    return f"{nome_limpo} {tag}"


def sanitize_filename(filename: str) -> str:
    """
    Sanitiza nome do arquivo removendo caracteres problemáticos
    
    Args:
        filename (str): Nome do arquivo original
        
    Returns:
        str: Nome do arquivo sanitizado
    """
    # Remover ou substituir caracteres problemáticos para nomes de arquivo
    import re
    # Substituir caracteres especiais por underscores
    sanitized = re.sub(r'[<>:"/\\|?*\[\]]', '_', filename)
    # Remover espaços extras e substituir por underscores
    sanitized = re.sub(r'\s+', '_', sanitized.strip())
    return sanitized
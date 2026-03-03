from bson import ObjectId

def converteObjectIDToStr(document):
    if document is None:
        return None
    return {key: (str(value) if isinstance(value, ObjectId) else value) for key, value in document.items()}

def removeKeys(document, keysToRemove):
    return {k: v for k,v in document.items() if k not in keysToRemove}

def normalize_database_name(name: str) -> str:
    """
    Normaliza o nome do banco de dados/instrumento removendo espaços e extensão .csv.
    Esta função garante consistência entre o nome usado no banco de dados e nos diretórios.
    
    Args:
        name (str): Nome do arquivo ou instrumento a ser normalizado.
    Returns:
        str: Nome normalizado sem espaços e sem extensão .csv.
    """
    normalized = name.replace(" ", "")
    normalized = normalized.replace(".csv", "")
    return normalized
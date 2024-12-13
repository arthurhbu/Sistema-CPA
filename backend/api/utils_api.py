from bson import ObjectId

def converteObjectIDToStr(document):
    if document is None:
        return None
    return {key: (str(value) if isinstance(value, ObjectId) else value) for key, value in document.items()}

def removeKeys(document, keysToRemove):
    return {k: v for k,v in document.items() if k not in keysToRemove}
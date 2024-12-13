from typing import Union

def ponto_2_virgula(valor: Union[str, int]) -> str:
    return str(valor).replace(".",",")
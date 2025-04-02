import re
import sys
sys.stdout.reconfigure(encoding="utf-8")


def table_interpretation_text_generator(pergunta: str, option_and_percentage: dict) -> str:
    """
    Função que cria um texto que facilite o prompt para a LLM, fazendo assim com que a resposta dela seja mais precisa.

    Args:
        pergunta (str): Uma das perguntas do instrumento.
        option_and_percentage (dict): É um dict que conté as opções e porcentagens dessa pergunta.
    Returns:
        text (str): Retorna uma String contendo o prompt que será consumido pela LLM.
    Raises: 
        None: Não há raises na função.
    """

    pergunta_formatada = re.sub("^\d+\.\d+\s*-\s*",'',pergunta)
    text = f'{pergunta_formatada} \n'
    for options in option_and_percentage.items():
        pct = str(options[1]).replace(".", ",")
        text = f'{text} - {pct}% responderam {options[0]}\n'  
    
    return text


def compose_table(pergunta: str, option_and_percentage: dict, respondentes: int) -> str:
    """
    Função que realiza a composição da tabela contendo as opções, porcentagens e respondentes.

    Args:
        pergunta (str): Uma pergunta do instrumento.
        option_and_percentage (dict): Dict contendo as opções e porcentagens da pergunta.
        respondentes (int): A quantidade de pessoas que responderam à pergunta.
    Responses:
        table (str): Uma tabela markdown em uma String.
    Raises:
        None: Não há raises.
    """
    pergunta_formatada = re.sub("^\d+\.\d+\s*-\s*",'',pergunta)
    table = "| Indicador |"
    for tuple in option_and_percentage.items():
        table = f'{table} {tuple[0].capitalize()} |'

    table = f"{table} Respondentes |"
    table = f'{table} \n|---|'
    for tuple in option_and_percentage.items():
        table =  f'{table}---|'
    table = f'{table}---|'

    table = f'{table} \n| {pergunta_formatada} |'
    for tuple in option_and_percentage.items():
        pct = str(tuple[1]).replace('.', ',')
        table = f'{table} {pct}% | '         
    table = f'{table}{respondentes} | '
    return table


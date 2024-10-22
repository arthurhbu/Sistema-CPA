import re
import sys
sys.stdout.reconfigure(encoding="utf-8")


def tableInterpretationTextGenerator(pergunta: str, optAndPercentage: dict) -> str:
    """
    Função que cria um texto contendo uma pergunta, as opções e as porentagens

    :param pergunta: Será utilizado como título para o texto formado
    :type pergunta: String
    :param optAndPercentage: Contém as opções e suas respectivas porcentagens em um dicionário
    :type optAndPercentage: Dict
    :return: Texto que contendo tudo de maneira formatada para que uma IA possa interpretar de maneira correta
    :rtype: String
    """

    pergunta_formatada = re.sub("^\d+\.\d+\s*-\s*",'',pergunta)
    text = f'{pergunta_formatada} \n'
    for options in optAndPercentage.items():
        pct = str(options[1]).replace(".", ",")
        text = f'{text} - {pct}% responderam {options[0]}\n'  
    
    return text


def composeTable(pergunta: str, optAndPercentage: dict, respondentes: int) -> str:
    """
    Função que realiza a composição de uma tabela contendo as opções e porcentagens

    :param pergunta: Utilizado para identificação da tabela que foi criada
    :type pergunta: String
    :param optAndPercentage: Contém as opções e suas respectivas porcentagens em um dicionário
    :type optAndPercentage: Dict
    :return: Uma tabela formada em markdown
    :rtype: String
    """
    pergunta_formatada = re.sub("^\d+\.\d+\s*-\s*",'',pergunta)
    s = "| Indicador |"
    for tuple in optAndPercentage.items():
        s = f'{s} {tuple[0].capitalize()} |'

    s = f"{s} Respondentes |"
    s = f'{s} \n|---|'
    for tuple in optAndPercentage.items():
        s =  f'{s}---|'
    s = f'{s}---|'

    s = f'{s} \n| {pergunta_formatada} |'
    for tuple in optAndPercentage.items():
        pct = str(tuple[1]).replace('.', ',')
        s = f'{s} {pct}% | '         
    s = f'{s}{respondentes} | '
    return s


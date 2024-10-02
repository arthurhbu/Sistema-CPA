from src.generationFunctions.text.textFunctions import tableInterpretationTextGenerator
import random as rand
import ollama
import requests
import json

url = 'http://servidor-ai:11434/api/generate'

headers = {'Content-Type': 'application/json'}


def createReport(pergunta, dictOptPct):
    """
    Função que gera o relatório para a pergunta que está sendo analisada, com base nas opções e porcentagens

    :param pergunta: Pergunta na qual está sendo feito o relatório
    :type pergunta: String
    :param dictOPtPct: Dicionário contendo as opções e respostas da pergunta
    :type dictOptPct: Dict
    :return: Retorna o relatório feito pelo chatGPT como resposta
    :rtype: String
    """
    inicio_textual = rand.choice([f"Considerando a Tabela index_, ", f"De acordo com a Tabela index_, ", f"Pela Tabela index_, ", f"Constatou-se pela Tabela index_ que ", f"Percebe-se pela Tabela index_ que "])
    temp_message = tableInterpretationTextGenerator(pergunta, dictOptPct)

    data = {
        'model': 'gemma2',
        'prompt': f"Reescreva na forma de um parágrafo sucinto iniciando com a frase {inicio_textual} o seguinte texto: \n {temp_message} ",
        'stream': False
    }

    for attempt in range(10):
        # try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_text = response.text
            data = json.loads(response_text)
            actual_response = data['response']
            return actual_response
        else:
            return print('ERROR: ', response.status_code, response.text)
        # except: 
        #     print('Aconteceu um erro com o Ollama!!!')
        #     continue
        # else: 
        #     break



    # response = ollama.chat(model="gemma2", messages=[{'role': 'user', 'content':f"Reescreva na forma de um parágrafo sucinto iniciando com a frase {inicio_textual} o seguinte texto: \n {temp_message} "}])

    # return response
    
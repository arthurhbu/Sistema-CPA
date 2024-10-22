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

    referencia_figura = rand.choice(['A figura index_ demonstra a prevalência das respostas.', 'A figura index_ mostra a tendência dominante das respostas.', 'A figura index_ representa a maior frequência das respostas.', 'A figura index_ exibe o padrão predominante nas respostas.','A figura index_ destaca a maior concentração de respostas.', 'A figura index_ evidencia a principal tendência nas respostas.', 'A figura index_ revela o comportamento predominante das respostas.', 'A figura index_ exibe a distribuição dos respondentes.', 'A figura index_ demonstra o padrão de distribuição dos respondentes.', 'A figura index_ representa a distribuição dos respondentes.'])

    temp_message = tableInterpretationTextGenerator(pergunta, dictOptPct)

    data = {
        'model': 'gemma2',
        'prompt': f"Reescreva na forma de um parágrafo sucinto iniciando com a frase {inicio_textual} o seguinte texto: \n {temp_message} ",
        'stream': False
    }

    for attempt in range(10):
        # try:
        response: dict = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            response_text: str = response.text
            data: str = json.loads(response_text)
            actual_response: str = data['response']
            clean_actual_response = actual_response.replace("\n", "")
            clean_actual_response = f'{clean_actual_response} {referencia_figura}'
            return actual_response
        else:
            return print('ERROR: ', response.status_code, response.text)




    # response = ollama.chat(model="gemma2", messages=[{'role': 'user', 'content':f"Reescreva na forma de um parágrafo sucinto iniciando com a frase {inicio_textual} o seguinte texto: \n {temp_message} "}])

    # return response
    
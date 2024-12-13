# from src.openAI.environment_variables import getKey
# from openai import OpenAI
# import re
# import random as rand
# from src.generationFunctions.text.textFunctions import tableInterpretationTextGenerator

# key = getKey()
# clientAI = OpenAI(api_key=key)

# def createCaption(pergunta):
#     """
#     Função que gera o título com base na pergunta, que é gerada utilizando a IA

#     :Param pegunta: Pergunta que será transformada em titulo pelo chatGPT
#     :type pergunta: String
#     :return: título gerado pelo chatGPT
#     :rtype: String
#     """
#     try:
#         completion = clientAI.chat.completions.create(
#             model="gpt-4-turbo",
#             messages=[
#                 {"role": "system", "content": "Você é um profissional que trabalha com relatórios"},
#                 {"role": "user", "content": f"Transforme a pergunta {pergunta} na forma de um título sucinto e que não seja indagação"}
#             ]
#         )
#         print(completion.usage.total_tokens)
#         return completion.choices[0].message.content
#     except OpenAI.error.Timeout as e:
#         #Handle timeout error, e.g. retry or log
#         print(f"OpenAI API request timed out: {e}")
#         pass
#     except OpenAI.error.APIError as e:
#         #Handle API error, e.g. retry or log
#         print(f"OpenAI API returned an API Error: {e}")
#         pass
#     except OpenAI.error.APIConnectionError as e:
#         #Handle connection error, e.g. check network or log
#         print(f"OpenAI API request failed to connect: {e}")
#         pass
#     except OpenAI.error.InvalidRequestError as e:
#         #Handle invalid request error, e.g. validate parameters or log
#         print(f"OpenAI API request was invalid: {e}")
#         pass
#     except OpenAI.error.AuthenticationError as e:
#         #Handle authentication error, e.g. check credentials or log
#         print(f"OpenAI API request was not authorized: {e}")
#         pass
#     except OpenAI.error.PermissionError as e:
#         #Handle permission error, e.g. check scope or log
#         print(f"OpenAI API request was not permitted: {e}")
#         pass
#     except OpenAI.error.RateLimitError as e:
#         #Handle rate limit error, e.g. wait or log
#         print(f"OpenAI API request exceeded rate limit: {e}")
#         pass

# def createReport(pergunta, dictOptPct):
#     """
#     Função que gera o relatório para a pergunta que está sendo analisada, com base nas opções e porcentagens

#     :param pergunta: Pergunta na qual está sendo feito o relatório
#     :type pergunta: String
#     :param dictOPtPct: Dicionário contendo as opções e respostas da pergunta
#     :type dictOptPct: Dict
#     :return: Retorna o relatório feito pelo chatGPT como resposta
#     :rtype: String
#     """
#     inicio_textual = rand.choice([f"Considerando a Tabela index_, ", f"De acordo com a Tabela index_, ", f"Pela Tabela index_", f"Constatou-se pela Tabela index_ que ", f"Percebe-se pela Tabela index_ que "])
#     temp_message = tableInterpretationTextGenerator(pergunta, dictOptPct)

#     try:
#         completion = clientAI.chat.completions.create(
#             model="gpt-4-turbo",
#             messages=[
#                 {"role": "system", "content": "Você é especialista em gramática e em produzir relatórios formais e profissionais."},
#                 {"role": "user", "content": f"Reescreva na forma de um parágrafo sucinto iniciando com a frase {inicio_textual} o seguinte texto: \n {temp_message} "}
#             ]
#         )
#         print(completion.usage.total_tokens)
#         return completion.choices[0].message.content
#     except OpenAI.error.Timeout as e:
#         #Handle timeout error, e.g. retry or log
#         print(f"OpenAI API request timed out: {e}")
#         pass
#     except OpenAI.error.APIError as e:
#         #Handle API error, e.g. retry or log
#         print(f"OpenAI API returned an API Error: {e}")
#         pass
#     except OpenAI.error.APIConnectionError as e:
#         #Handle connection error, e.g. check network or log
#         print(f"OpenAI API request failed to connect: {e}")
#         pass
#     except OpenAI.error.InvalidRequestError as e:
#         #Handle invalid request error, e.g. validate parameters or log
#         print(f"OpenAI API request was invalid: {e}")
#         pass
#     except OpenAI.error.AuthenticationError as e:
#         #Handle authentication error, e.g. check credentials or log
#         print(f"OpenAI API request was not authorized: {e}")
#         pass
#     except OpenAI.error.PermissionError as e:
#         #Handle permission error, e.g. check scope or log
#         print(f"OpenAI API request was not permitted: {e}")
#         pass
#     except OpenAI.error.RateLimitError as e:
#         #Handle rate limit error, e.g. wait or log
#         print(f"OpenAI API request exceeded rate limit: {e}")
#         pass
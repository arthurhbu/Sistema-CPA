import pystache
import re
from src.utils.ponto_2_virgula import ponto_2_virgula 
import sys
from pathlib import Path
from pymongo.collection import Collection
sys.stdout.reconfigure(encoding="utf-8")


def compor_introducao(collection_centro_por_ano: Collection,collection_cursos_por_centro: Collection, arquivo_intro: str, ano: int, centro_de_ensino: str, modal: str) -> None:
    """
    Gera um arquivo markdown contendo as informações da introdução do relatório baseado no tipo de instrumento, levando em conta que cada template possui suas próprias informações a serem passadas.

    :param collectionCentroPorAno: Nome da collection que contém as informações sobre os centros.
    :type: Collection (MongoDB)
    :param CollectionCursosPorCentro: Nome da collection que contém informações sobre os cursos de um centro.
    :type: Collection (MongoDB)
    :param arquivo_intro: Nome do arquivo que contém o template da introdução do relatório
    :type: String
    :param ano: O ano de que será feito o relatório.
    :type ano: Integer
    :param centro_de_ensino: Nome do centro de ensino escolhido para a geração da tabela contendo os seus cursos
    :type centro_de_ensino: String

    """
    
    #FALTA MEXER PARA TER O PARTICIPACAO_CURSO TAMBEM
    
    if modal == 'discente':	
        with open(f'relatorioComponentes/{arquivo_intro}','r',encoding='utf-8') as f:
            template = f.read()
        renderer = pystache.Renderer()
        respondentes_total = 0
        matriculas_totais = 0
        
        tabela_centros = "| Sigla | Centro   | Matr. | Resp.   |  %   |\n |------|:----:|:-----:|:---:|:---:| \n"
        for document in collection_centro_por_ano.find():
            respondentes_total += document['respondentes']  
            matriculas_totais += document['matriculados']
            tabela_centros += f'| {document["centro_de_ensino"]}'
            tabela_centros += f'| {document["centro_descricao"]}'    
            tabela_centros += f'| {document["matriculados"]}'
            tabela_centros += f'| {document["respondentes"]}'    
            tabela_centros += f'| {document["porcentagem"]}'    
            tabela_centros += '| \n'    
            
        participacao_uem = round(100 * (respondentes_total/matriculas_totais), 2)
        
        tabela_cursos = df_2_tabela_cursos = "| Curso |  Resp. |Matr.|   %   | \n |------|:-----:|:-----:|:---:| \n "
        for document in collection_cursos_por_centro.find({'centro_de_ensino': centro_de_ensino}):
            tabela_cursos += f'| {document["nm_curso"]}'
            tabela_cursos += f'| {document["respondentes"]}'
            tabela_cursos += f'| {document["matriculados"]}'
            tabela_cursos += f'| {document["porcentagem"]}'
            tabela_cursos += '| \n'

        intro = renderer.render(template, {'tabela_centros': tabela_centros, 'tabela_cursos_por_centro': tabela_cursos, 'ano': ano, 'curso': '{{curso}}', 'participacao_uem': ponto_2_virgula(participacao_uem), 'participacao_curso': '{{participacao_curso}}'})
        
        with open("relatorio/info_introducao.md", "w", encoding='utf-8') as arquivo:
            arquivo.write(f'{intro} \n')
    elif modal == 'ead':
        with open(f'relatorioComponentes/{arquivo_intro}','r',encoding='utf-8') as f:
            template = f.read()
        renderer = pystache.Renderer()
        respondentes_total = 0
        matriculas_totais = 0
        
        for document in collection_centro_por_ano.find():
            respondentes_total += document['respondentes']
            matriculas_totais += document['matriculados']
        
        #Implementar o participacao_curso
        
        intro = renderer.render(template, {'ano': ano, 'curso': '{{curso}}', 'participacao_curso': '{{participacao_curso}}'})
        
        with open("relatorio/info_introducao.md", "w", encoding='utf-8') as arquivo:
            arquivo.write(f'{intro} \n')
    elif modal == 'egresso':
        with open(f'relatorioComponentes/{arquivo_intro}','r',encoding='utf-8') as f:
            template = f.read()
        renderer = pystache.Renderer()
        
        intro = renderer.render(template, {'ano': ano, 'curso': '{{curso}}'})
        
        with open("relatorio/info_introducao.md", "w", encoding='utf-8') as arquivo:
            arquivo.write(f'{intro} \n')
    else:
        with open(f'relatorioComponentes/{arquivo_intro}','r',encoding='utf-8') as f:
            template = f.read()
        renderer = pystache.Renderer()
        
        intro = renderer.render(template)
        
        with open("relatorio/info_introducao.md", "w", encoding='utf-8') as arquivo:
            arquivo.write(f'{intro} \n')
    

def compor_conclusao(collection_name_cursos_por_centro: Collection, arquivo_conclusao: str, ano: int, curso: str, modal: str) -> None:
    """
    Compõe o arquivo de conclusão do relatório, baseado no tipo de instrumento que está sendo passado, sendo classificados em: Egresso, EAD, Discente, Docente e Tecnico. Cada um deles tem um template de conclusão diferente por isso o uso de um "Switch case" para escolher o template correto.

    :param CollectionCursosPorCentro: Nome da collection que contém informações sobre os cursos de um centro.
    :type: Collection (MongoDB)
    :param arquivo_conclusao: Nome do arquivo que contém o template de conclusão do relatório 
    :type arquivo_conclusao: String
    :param ano: O ano de que será feito o relatório.
    :type ano: Integer
    """
    
    if modal == 'discente':
        with open(f'relatorioComponentes/{arquivo_conclusao}', 'r', encoding='utf-8') as f:
            template = f.read()
        renderer = pystache.Renderer()
        for document in collection_name_cursos_por_centro.find():
            respondentes_total = document['respondentes']
            matriculas_totais = document['matriculados']

        participacao_curso = collection_name_cursos_por_centro.find_one({'nm_curso': curso})['porcentagem']
        
        participacao_uem = round(100 * (respondentes_total/matriculas_totais), 2)
        conclusao = renderer.render(template, {'ano': ano, 'curso': '{{curso}}', 'participacao_uem': ponto_2_virgula(participacao_uem), 'participacao_curso': ponto_2_virgula(participacao_curso)})
        with open("relatorio/info_conclusao.md","w", encoding='utf-8') as arquivo:
            arquivo.write(f'{conclusao} \n')
            
    elif modal == 'ead':
        with open(f'relatorioComponentes/{arquivo_conclusao}', 'r', encoding='utf-8') as f:
            template = f.read()
        renderer = pystache.Renderer()
        for document in collection_name_cursos_por_centro.find():
            respondentes_total = document['respondentes']
            matriculas_totais = document['matriculados']

        participacao_uem = round(100 * (respondentes_total/matriculas_totais), 2)
        
        conclusao = renderer.render(template, {'ano': ano, 'participacao_uem': ponto_2_virgula(participacao_uem)})
        with open("relatorio/info_conclusao.md","w", encoding='utf-8') as arquivo:
            arquivo.write(f'{conclusao} \n')
            
    elif modal == 'egresso':
        with open(f'relatorioComponentes/{arquivo_conclusao}', 'r', encoding='utf-8') as f:
            template = f.read()
        renderer = pystache.Renderer()
        for document in collection_name_cursos_por_centro.find():
            respondentes_total = document['respondentes']
            matriculas_totais = document['matriculados']

        participacao_uem = round(100 * (respondentes_total/matriculas_totais), 2)
        
        conclusao = renderer.render(template, {'ano': ano, 'participacao_uem': ponto_2_virgula(participacao_uem)})
        with open("relatorio/info_conclusao.md","w", encoding='utf-8') as arquivo:
            arquivo.write(f'{conclusao} \n')
    else: 
        with open(f'relatorioComponentes/{arquivo_conclusao}', 'r', encoding='utf-8') as f:
            template = f.read()
        renderer = pystache.Renderer()
        
        conclusao = renderer.render(template)
        with open("relatorio/info_conclusao.md","w", encoding='utf-8') as arquivo:
            arquivo.write(f'{conclusao} \n')
    

def substituirIdentificadores(filename: str, dbName: str):
    directory = Path('relatorio')
    file = f'{directory}/{filename}'

    with open(f'./relatorio/markdowns/{dbName}/{filename}', 'r', encoding='utf-8') as file:
        content = file.read()

    index = 0
    index_disciplina = 0
    contador = 0

    def replace_custom(match):
        nonlocal contador, index, index_disciplina
        iden = match.group(1)
        
        if iden == 'index_':
            if (contador % 4) == 0:
                index += 1
            replacement = f'{index}'
            contador += 1

        elif iden == 'indexDisciplina':
            index += 1
            replacement = f'{index}'
            
        return replacement

    defaultContent = re.sub(r'Index_', 'index_', content)
    new_content = re.sub(r'(index_|indexDisciplina)', replace_custom, defaultContent)
    
    with open(f'./relatorio/markdowns/{dbName}/{filename}', 'w', encoding='utf-8') as file:
        file.write(new_content)



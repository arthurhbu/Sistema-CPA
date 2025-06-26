import pystache
import re
from src.utils.ponto_2_virgula import ponto_2_virgula 
import sys
from pathlib import Path
from pymongo.collection import Collection
sys.stdout.reconfigure(encoding="utf-8")
import os 


def compor_introducao(collection_centro_por_ano: Collection,collection_cursos_por_centro: Collection, ano: int, centro_de_ensino: str, modal: str, nome_instrumento: str) -> dict:
    """
    Gera um arquivo markdown contendo as informações da introdução do relatório baseado no tipo de instrumento, levando em conta que cada template possui suas próprias informações a serem passadas.

    Args:
        collection_centro_por_ano (Collection): Collection contendo informações do dataset criado centro_por_ano. 
        collection_cursos_por_centro (Collection): Collection contendo informações do dataset centro_por_curso.
        arquivo_intro (str): Nome do arquivo de introdução que foi escolhido.
        centro_de_ensino (str): Nome do centro de ensino da UEM.
        modal (str): Modalidade/Tipo do instrumento que será gerado a introdução.
    Returns:
        dict: Retorna um dict informando a falha e o erro ou sucesso.
    Raises:
        None: Não possui Raises, Exceptions passadas via return.
    """
    try:
        path_intro = os.path.join('relatorio_componentes', nome_instrumento, 'introducao')
        arquivos_intro = os.listdir(path_intro)
        arq_intro = arquivos_intro[0]
        arquivo_path = os.path.join(path_intro, arq_intro)
        if modal == 'discente':	
            with open(arquivo_path,'r',encoding='utf-8') as f:
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
            with open(arquivo_path,'r',encoding='utf-8') as f:
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
            with open(arquivo_path,'r',encoding='utf-8') as f:
                template = f.read()
            renderer = pystache.Renderer()
            
            intro = renderer.render(template, {'ano': ano, 'curso': '{{curso}}'})
            
            with open("relatorio/info_introducao.md", "w", encoding='utf-8') as arquivo:
                arquivo.write(f'{intro} \n')
                
        else:
            with open(arquivo_path,'r',encoding='utf-8') as f:
                template = f.read()
            renderer = pystache.Renderer()
            
            intro = renderer.render(template)
            
            with open("relatorio/info_introducao.md", "w", encoding='utf-8') as arquivo:
                arquivo.write(f'{intro} \n')
        
        return {'Success': True}
    except Exception as e:
        return {'Success': False, 'Error': f'Ocorreu um erro ao tentar compor introdução: {e}'}
        

def compor_conclusao(collection_name_cursos_por_centro: Collection, ano: int, curso: str, modal: str, nome_instrumento: str) -> None:
    """
    Compõe o arquivo de conclusão do relatório, baseado no tipo de instrumento que está sendo passado, sendo classificados em: Egresso, EAD, Discente, Docente e Tecnico. Cada um deles tem um template de conclusão diferente por isso o uso de um "Switch case" para escolher o template correto.

    Args:
        collection_name_cursos_por_centro (Collection): Collection que contém as informações do dataset cursos_por_centro.
        arquivo_conclusao (str): Nome do arquivo markdown de conclusão selecionado.
        ano (int): Inteiro contendo o ano do relatório.
        curso (str): Nome do curso que está sendo gerado a conclusão.
        modal (str): Modalidade/Tipo do instrumento que será gerado a introdução.
    Returns:
        dict: Retorna um dict informando a falha e o erro ou sucesso.
    Raises:
        None: Não possui Raises, Exceptions passadas via return.
    """
    
    try:
        path_concl = os.path.join('relatorio_componentes', nome_instrumento, 'conclusao')
        arquivos_concl = os.listdir(path_concl)
        arq_concl = arquivos_concl[0]
        arquivo_path = os.path.join(path_concl, arq_concl)
        if modal == 'discente':
            with open(arquivo_path, 'r', encoding='utf-8') as f:
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
            with open(arquivo_path, 'r', encoding='utf-8') as f:
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
            with open(arquivo_path, 'r', encoding='utf-8') as f:
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
            with open(arquivo_path, 'r', encoding='utf-8') as f:
                template = f.read()
            renderer = pystache.Renderer()
            
            conclusao = renderer.render(template)
            with open("relatorio/info_conclusao.md","w", encoding='utf-8') as arquivo:
                arquivo.write(f'{conclusao} \n')
        return {'Success': True}
        
    except Exception as e:
        return {'Success': False, 'Error': f'Ocorreu um erro ao tentar compor conclusão: {e}'}

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
        
def replace_reference_in_caption(caption_from_ai: str, index: int) -> str:
    """
    Substitui a referência index_ da legenda gerada pela AI por um valor que será usada na geração de PDF utilizando o pandoc.
    
    Args:
        caption_from_ai (str): Texto que foi gerado pela LLM e que agora será modificada com as referências necessárias.
        index (int): Índice da pergunta que possui tal texto.
    Returns:
        formated_caption (str): Retorna o texto modificado.
    Raises:
        None: Não possui Raises, Exceptions passadas via return.
    """

    substitions = { 
        "_index_": "index_",
        "Index_": "index_",
        "tabela": "Tabela",
        "Figura": "figura"
    }

    substitions_to_pandoc_format = {
        "Tabela index_": f'[@tbl:tabela{index}]',
        "figura index_": f'[@fig:figura{index}]',
    }

    pattern = re.compile("|".join(map(re.escape, substitions.keys())))
    pattern_to_sub = re.compile("|".join(map(re.escape, substitions_to_pandoc_format.keys())))

    default_caption = pattern.sub(lambda match: substitions[match.group(0)], caption_from_ai)
    formated_caption = pattern_to_sub.sub(lambda match: substitions_to_pandoc_format[match.group(0)], default_caption)

    return formated_caption
import pystache
import re
import sys
from src.utils.ponto_2_virgula import ponto_2_virgula
from pathlib import Path
from src.relatorio.compor_partes_relatorio import replace_reference_in_caption

sys.stdout.reconfigure(encoding="utf-8")

def gerarRelatorioPorCurso(curso_escolhido, collectionCurso, collectionCursosPorCentro, dbName: str):
    """
    Gerar um relatório de apenas um curso.

    :param curso_escolhido: Nome do curso que você quer gerar o relatório md
    :type curso_escolhido: String
    :param collectionCurso: Nome da collection que tem as informações do csv principal
    :type collectionCurso: Collection
    :param collectionCursosPorCentro: Nome da collection que tem as informações para gerar a 
    introdução do relatório.
    :type collectionCursosPorCentro: Collection
    :param dbName: Nome do banco de dados que está sendo manipulado
    :type dbName: str
    """


    
    directory = Path(f'relatorio/markdowns/{dbName}')
    directory.mkdir(parents=True, exist_ok=True)
    file = f'{directory}/{curso_escolhido}.md'

    dir_pdfs = Path(f'relatorio/pdfs/{dbName}')
    dir_pdfs.mkdir(parents=True, exist_ok=True)

    with open(file, 'w', buffering=-1,encoding='utf-8') as arquivo:

        arquivo.write("---\n")
        arquivo.write("title: \"Relatório do Curso de {}\"\n".format(curso_escolhido))
        arquivo.write("---\n\n")

        with open("relatorio/info_introducao.md",'r', encoding='utf-8') as f:
            template_introducao = f.read()
        renderer = pystache.Renderer()
        participacao_curso = 0.0
        for document in collectionCursosPorCentro.find({'nm_curso': curso_escolhido}):
            participacao_curso = document['porcentagem']
        intro = renderer.render(template_introducao, {'curso': curso_escolhido, 'participacao_curso': participacao_curso})
        arquivo.write(f'{intro} \n')

        codGrupo: list = []
        codSubgrupo: list = []
        codDisciplina: list = []

        contador: int = 0
        print(curso_escolhido)

        for document in collectionCurso.find({'nm_curso': curso_escolhido}).sort({'cd_grupo': 1, 'cd_subgrupo': 1}):
            

            captionToPandoc = replace_reference_in_caption(document['relatorioGraficoAI'], contador)

            if document['cd_grupo'] not in codGrupo:
                print('\n',file=arquivo)
                arquivo.write(f"## {document['nm_grupo']}")
                print('\n', file=arquivo)
                codGrupo.append(document['cd_grupo'])
                codSubgrupo = []
            if document['cd_subgrupo'] not in codSubgrupo:
                print('\n',file=arquivo)
                arquivo.write(f"### {document['nm_subgrupo']}")
                print('\n',file=arquivo)
                codSubgrupo.append(document['cd_subgrupo'])

            if document['nm_disciplina'] == '-':
                pergunta_formatada: str = re.sub(r"^\d+\.\d+-\s*",'',document["nm_pergunta"])
                print(f'#### **Pergunta: {pergunta_formatada}**\n', file=arquivo)
                arquivo.write(f"![{document['nm_pergunta']}:]({document['path']}.png) {{#fig:figura{contador}}}")
                print('\n', file=arquivo)
                print(f': Tabela com dados referentes à pergunta apresentada. {{#tbl:tabela{contador}}} \n', file=arquivo)
                arquivo.write(document['tabela'])
                arquivo.write('\n')
                print(' ', file=arquivo)
                print(captionToPandoc, file=arquivo)
                arquivo.write('\n')
                arquivo.write('\n')
                contador += 1
                continue
            
            if document['cd_disciplina'] not in codDisciplina:
                print('\n', file=arquivo)
                arquivo.write(f"Considerando a disciplina **{document['nm_disciplina']}**, temos os seguintes resultados expressos por tabelas.")
                print('\n', file=arquivo)
                codDisciplina.append(document['cd_disciplina'])

            print('\n', file=arquivo)
            print(f"{{#tbl:tabela{contador}}} - Resultado do item: {document['nm_pergunta']} \n", file=arquivo)
            arquivo.write(document['tabela'])
            print('\n', file=arquivo)

            contador += 1 
            print('contador: ', contador)

        with open("relatorio/info_conclusao.md",'r',encoding='utf-8') as f:
            template_conclusao = f.read()
        rendererConclusao = pystache.Renderer()
        conclusao = rendererConclusao.render(template_conclusao, {'curso': curso_escolhido, 'participacao_curso': ponto_2_virgula(participacao_curso)})
        arquivo.write(f'{conclusao} \n')
    arquivo.close()

    
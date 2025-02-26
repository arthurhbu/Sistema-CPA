import pystache
import re
import sys
from src.utils.ponto_2_virgula import ponto_2_virgula
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

def gerar_relatorio_por_curso(curso_escolhido, collection_instrumento, collection_cursos_por_centro, dbName: str):
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


    #Talvez separar parte inicial para virar uma função compor capa
    
    directory = Path(f'relatorio/markdowns/{dbName}')
    directory.mkdir(parents=True, exist_ok=True)
    file = f'{directory}/{curso_escolhido}.md'

    dir_pdfs = Path(f'relatorio/pdfs/{dbName}')
    dir_pdfs.mkdir(parents=True, exist_ok=True)

    with open(file, 'w', buffering=-1,encoding='utf-8') as arquivo:

        arquivo.write("---\n")
        arquivo.write("title: \"Relatório do Curso de {}\"\n".format(curso_escolhido))
        arquivo.write("titlepage: true\n")
        arquivo.write("titlepage-background: \"capa\"\n")
        arquivo.write("titlepage-rule-color: \"B3B3B3\"\n")
        arquivo.write("page-background: \"interna02\"\n")
        arquivo.write("page-background-opacity: '1.0'\n")
        arquivo.write("author: [CPA-Comissão Própria de Avaliação]\n")
        arquivo.write("lang: \"pt-BR\"\n")
        arquivo.write("---\n\n")

        #Precisa criar a função que compõe a introdução
        with open("relatorio/info_introducao.md",'r', encoding='utf-8') as f:
            template_introducao = f.read()
        renderer = pystache.Renderer()
        participacao_curso = 0.0
        for document in collection_cursos_por_centro.find({'nm_curso': curso_escolhido}):
            participacao_curso = document['porcentagem']
        intro = renderer.render(template_introducao, {'curso': curso_escolhido, 'participacao_curso': participacao_curso})
        arquivo.write(f'{intro} \n')

        codGrupo = []
        codSubgrupo = []

        for document in collection_instrumento.find({'nm_curso': curso_escolhido}).sort({'cd_grupo': 1, 'cd_subgrpo': 1}):
            
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
                pergunta_formatada = re.sub(r"^\d+\.\d+-\s*",'',document["nm_pergunta"])
                print(f'**Pergunta: {pergunta_formatada}**\n', file=arquivo)
                arquivo.write(f"![{document['nm_pergunta']}]({document['path']}.png)")
                print(f'<p style="text-align: center; color: #E2E1E1;"> Figura index_ - {document['nm_pergunta']} </p>', file=arquivo)
                print('\n', file=arquivo)
                print(f"Tabela index_ \n", file=arquivo)
                arquivo.write(document['tabela'])
                arquivo.write('\n')
                print(' ', file=arquivo)
                print(document['relatorioGraficoAI'], file=arquivo)
                arquivo.write('\n')
                arquivo.write('\n')
                # print(f"Edição da pergunta {document['cd_pergunta']} do subgrupo {document['cd_subgrupo']} do curso {document['nm_curso']} concluida com sucesso!")
                continue
            
            print('\n', file=arquivo)
            print(f"Tabela indexDisciplina - Resultado do item: {document['nm_pergunta']} \n", file=arquivo)
            arquivo.write(document['tabela'])
            print('\n', file=arquivo)

        with open("relatorio/info_conclusao.md",'r',encoding='utf-8') as f:
            template_conclusao = f.read()
        rendererConclusao = pystache.Renderer()
        conclusao = rendererConclusao.render(template_conclusao, {'curso': curso_escolhido, 'participacao_curso': ponto_2_virgula(participacao_curso)})
        arquivo.write(f'{conclusao} \n')
    arquivo.close()

    
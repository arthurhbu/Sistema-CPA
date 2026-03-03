from pymongo.collection import Collection
import pystache
import re
import sys
from src.utils.ponto_2_virgula import ponto_2_virgula
from pathlib import Path
from src.relatorio.compor_partes_relatorio import replace_reference_in_caption

sys.stdout.reconfigure(encoding="utf-8")

def gerar_relatorio_por_curso(nome_arquivo: str, cd_curso: int, collection_curso: Collection, collection_cursos_por_centro: Collection, db_name: str):
    """
    Gera o relatório completo de somente um curso. Função reutilizada para assim gerar todos os relatórios do instrumento.

    Args:
        nome_arquivo: Nome do arquivo que será gerado (com tags identificadoras)
        cd_curso: Código do curso para consultas no banco de dados
        collection_curso: Nome da collection que tem as informações do csv principal
        collection_cursos_por_centro: Nome da collection que tem as informações para gerar a 
        introdução do relatório.
        db_name: Nome do banco de dados que está sendo manipulado
    Returns:
        dict: Retorna um dict informando a falha e o erro ou sucesso.
    Raises:
        None: Não possui Raises, Exceptions passadas via return.
    """
    
    try:
        directory = Path(f'relatorio/markdowns/{db_name}')
        directory.mkdir(parents=True, exist_ok=True)
        file = f'{directory}/{nome_arquivo}.md'

        dir_pdfs = Path(f'relatorio/pdfs/{db_name}')
        dir_pdfs.mkdir(parents=True, exist_ok=True)

        # Buscar informações do curso pelo código
        curso_info = collection_curso.find_one({'cd_curso': cd_curso})
        if not curso_info:
            return {'Success': False, 'Error': f'Curso com código {cd_curso} não encontrado'}
        
        nome_curso_display = nome_arquivo.replace('_', ' ')  # Converter underscores de volta para espaços no título

        with open(file, 'w', buffering=-1,encoding='utf-8') as arquivo:

            arquivo.write("---\n")
            arquivo.write("title: \"Relatório do Curso de {}\"\n".format(nome_curso_display))
            arquivo.write("---\n\n")

            with open("relatorio/info_introducao.md",'r', encoding='utf-8') as f:
                template_introducao = f.read()
                
            renderer = pystache.Renderer()
            participacao_curso = 0.0
            
            # MUDANÇA: Usar cd_curso em vez de nm_curso para buscar dados
            for document in collection_cursos_por_centro.find({'cd_curso': cd_curso}):
                participacao_curso = document['porcentagem']
                
            intro = renderer.render(template_introducao, {'curso': nome_curso_display, 'participacao_curso': participacao_curso})
            arquivo.write(f'{intro} \n')

            codGrupo: list = []
            codSubgrupo: list = []
            codDisciplina: list = []

            contador: int = 0
            print(f'Curso que está sendo gerado o relatório: {nome_curso_display} (Código: {cd_curso})')

            for document in collection_curso.find({'cd_curso': cd_curso}).sort([('cd_grupo', 1), ('cd_subgrupo', 1), ('cd_disciplina', 1), ('ordem_pergunta', 1)]):

                    captionToPandoc = replace_reference_in_caption(document['relatorioGraficoAI'], contador)
                    
                    if document['cd_grupo'] not in codGrupo:
                        print('\n',file=arquivo)
                        arquivo.write(f"## {document['nm_grupo']}")
                        print('\n', file=arquivo)
                        codGrupo.append(document['cd_grupo'])
                        codSubgrupo = []
                        codDisciplina = []  # Limpar disciplinas ao mudar de grupo
                    if document['cd_subgrupo'] not in codSubgrupo:
                        print('\n',file=arquivo)
                        arquivo.write(f"### {document['nm_subgrupo']}")
                        print('\n',file=arquivo)
                        codSubgrupo.append(document['cd_subgrupo'])
                        codDisciplina = []  # Limpar disciplinas ao mudar de subgrupo

                    if document['nm_disciplina'] == '-':
                        pergunta_formatada: str = re.sub(r"^\s*\d+\.\d+\s*-\s*",'',document["nm_pergunta"]).strip()
                        print(f'#### **Pergunta: {pergunta_formatada}**\n', file=arquivo)
                        arquivo.write(f"![{document['nm_pergunta']}:]({document['path']}.png){{#fig:figura{contador}}}")
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
                        arquivo.write(f"#### **Disciplina: {document['nm_disciplina'].strip()}**")
                        print('\n', file=arquivo)
                        arquivo.write(f"Considerando a disciplina **{document['nm_disciplina'].strip()}**, temos os seguintes resultados expressos por tabelas.")
                        print('\n', file=arquivo)
                        codDisciplina.append(document['cd_disciplina'])

                    print('\n', file=arquivo)
                    print(f"{{#tbl:tabela{contador}}} - Resultado do item: {document['nm_pergunta']} \n", file=arquivo)
                    arquivo.write(document['tabela'])
                    print('\n', file=arquivo)

                    contador += 1 

            with open("relatorio/info_conclusao.md",'r',encoding='utf-8') as f:
                template_conclusao = f.read()
            rendererConclusao = pystache.Renderer()
            conclusao = rendererConclusao.render(template_conclusao, {'curso': nome_curso_display, 'participacao_curso': ponto_2_virgula(participacao_curso)})
            arquivo.write(f'{conclusao} \n')
        arquivo.close()
        return {'Success': True}
        
    except Exception as e :
        return {'Success': False, 'Error': f'Ocorreu um erro ao tentar gerar os relatórios: {e}'}
    

    
from pymongo.collection import Collection
from pymongo.database import Database
from src.relatorio.compor_partes_relatorio import compor_introducao, compor_conclusao, substituirIdentificadores
from src.relatorio.gerar_relatorio import gerar_relatorio_por_curso
from src.utils.course_name_utils import generate_course_display_name, sanitize_filename


def gerar_todos_relatorios(collection_instrumento: Collection, collection_centro_por_ano: Collection, collection_cursos_por_centro: Collection, ano: int, database_name: str, modal: str, nome_instrumento: str) -> None:
    """
    Gera relatório de todos os cursos.
    
    Args:
        collection_instrumento (Collection): Collection que contém as informações do csv principal.
        collection_centro_por_ano (Collection): Collection que contém as informações sobre os centros.
        collection_cursos_por_centro (Collection): Collection que contém informações sobre os cursos de um centro.
        arquivo_intro (str): Nome do arquivo que contém o template da introdução do relatório.
        arquivo_conclusao (str): Nome do arquivo que contém o template de conclusão do relatório .
        ano (int): O ano de que será feito o relatório.
        database_name (str): Nome do banco de dados que está sendo manipulado.
        modal (str): Modalidade/Tipo do instrumento que será gerado.
    Returns:
        dict: Retorna um dict informando a falha e o erro ou sucesso.
    Raises:
        None: Não possui Raises, Exceptions passadas via return.
    """
    centros = collection_instrumento.distinct('centro_de_ensino')
    for centro in centros:
        if centro == 'nan':
            print('Centro nan não existe, por favor, confira o CSV ou alguma das etapas anteriores')
        res: dict = gerar_relatorios_por_centro(collection_instrumento, collection_centro_por_ano, collection_cursos_por_centro, ano, centro, database_name, modal, nome_instrumento)
        if res['Success'] == False:
            return {'Success': False, 'Error': res['Error']}
    return {'Success': True}
        

def gerar_relatorios_por_centro(collection_instrumento: Collection, collection_centro_por_ano: Collection, collection_cursos_por_centro: Collection, ano: int, centro_de_ensino: str, database_name: str, modal: str, nome_instrumento: str) -> None:
    """
    Gera os relatórios de um mesmo centro de ensino da UEM.
    Args:
        collection_instrumento (Collection): Collection que contém as informações do csv principal.
        collection_centro_por_ano (Collection): Collection que contém as informações sobre os centros.
        collection_cursos_por_centro (Collection): Collection que contém informações sobre os cursos de um centro.
        arquivo_intro (str): Nome do arquivo que contém o template da introdução do relatório
        arquivo_conclusao (str): Nome do arquivo que contém o template de conclusão do relatório 
        ano (int): O ano de que será feito o relatório.
        centro_de_ensino (str): Nome de um centro de ensino da UEM.
        database_name (str): Nome do banco de dados que está sendo manipulado.
        modal (str): Modalidade/Tipo do instrumento que será gerado.
    Returns:
        dict: Retorna um dict informando a falha e o erro ou sucesso.
    Raises:
        None: Não possui Raises, Exceptions passadas via return.
    """

    # MUDANÇA: Usar cd_curso em vez de nm_curso para evitar duplicatas
    codigos_cursos = collection_instrumento.distinct('cd_curso', {'centro_de_ensino': centro_de_ensino})
    
    for cd_curso in codigos_cursos:
        # Buscar informações completas do curso pelo código
        curso_info = collection_instrumento.find_one({'cd_curso': cd_curso, 'centro_de_ensino': centro_de_ensino})
        if not curso_info:
            print(f'Erro: Não foi possível encontrar informações para o curso com código {cd_curso}')
            continue
            
        nm_curso_original = curso_info['nm_curso']
        
        # Gerar nome para exibição com tag identificadora
        nome_para_exibicao = generate_course_display_name(nm_curso_original, centro_de_ensino)
        nome_arquivo = sanitize_filename(nome_para_exibicao)
        
        print(f'Gerando relatório para: {nome_para_exibicao} (Código: {cd_curso})')
        
        res_compor_intro: dict = compor_introducao(collection_centro_por_ano, collection_cursos_por_centro, ano, centro_de_ensino, modal, nome_instrumento)
        if res_compor_intro['Success'] == False: 
            return {'Success': False, 'Error': res_compor_intro['Error']}
        
        res_compor_conclusao: dict = compor_conclusao(collection_cursos_por_centro, ano, cd_curso, modal, nome_instrumento)
        if res_compor_conclusao['Success'] == False:
            return {'Success': False, 'Error': res_compor_conclusao['Error']} 
        
        res_gerar_relatorios: dict = gerar_relatorio_por_curso(nome_arquivo, cd_curso, collection_instrumento, collection_cursos_por_centro, database_name)
        if res_gerar_relatorios['Success'] == False:
            return {'Success': False, 'Error': res_gerar_relatorios['Error']} 
        
    return {'Success': True}

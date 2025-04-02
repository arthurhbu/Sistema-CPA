from pymongo.collection import Collection
from pymongo.database import Database
from src.relatorio.compor_partes_relatorio import compor_introducao, compor_conclusao, substituirIdentificadores
from src.relatorio.gerar_relatorio import gerar_relatorio_por_curso


def gerar_todos_relatorios(collection_instrumento: Collection, collection_centro_por_ano: Collection, collection_cursos_por_centro: Collection, arquivo_intro: str, arquivo_conclusao: str, ano: int, database_name: str, modal: str) -> None:
    """
    Gera relatório de todos os cursos.

    :param collectionCurso: Nome da collection que contém as informações do csv principal.
    :type collectionCurso: Collection (MongoDB)     
    :param collectionCentroPorAno: Nome da collection que contém as informações sobre os centros.
    :type: Collection (MongoDB)
    :param CollectionCursosPorCentro: Nome da collection que contém informações sobre os cursos de um centro.
    :type: Collection (MongoDB)
    :param arquivo_intro: Nome do arquivo que contém o template da introdução do relatório
    :type: String
    :param arquivo_conclusao: Nome do arquivo que contém o template de conclusão do relatório 
    :type arquivo_conclusao: String
    :param ano: O ano de que será feito o relatório.
    :type ano: Integer
    :param dbName: Nome do banco de dados que está sendo manipulado
    :type dbName: str
    """
    centros = collection_instrumento.distinct('centro_de_ensino')
    for centro in centros:
        if centro == 'nan':
            print('Centro nan não existe, por favor, confira o CSV ou alguma das etapas anteriores')
        res: dict = gerar_relatorios_por_centro(collection_instrumento, collection_centro_por_ano, collection_cursos_por_centro, arquivo_intro, arquivo_conclusao, ano, centro, database_name, modal)
        if res['Success'] == False:
            return {'Success': False, 'Error': res['Error']}
    return {'Success': True}
        

def gerar_relatorios_por_centro(collection_instrumento: Collection, collectionCentroPorAno: Collection, collectionCursosPorCentro: Collection, arquivo_intro: str, arquivo_conclusao: str, ano: int, centro_de_ensino: str, database_name: str, modal: str) -> None:
    """
    Gera relatórios dos cursos pertencentes a um centro.

    :param collectionCurso: Nome da collection que contém as informações do csv principal.
    :type collectionCurso: Collection (MongoDB)     
    :param collectionCentroPorAno: Nome da collection que contém as informações sobre os centros.
    :param CollectionCursosPorCentro: Nome da collection que contém informações sobre os cursos de um centro.
    :type: Collection (MongoDB)
    :param arquivo_intro: Nome do arquivo que contém o template da introdução do relatório
    :type: String
    :param arquivo_conclusao: Nome do arquivo que contém o template de conclusão do relatório 
    :type arquivo_conclusao: String
    :param ano: O ano de que será feito o relatório.
    :type ano: Integer
    :param centro_de_ensino: Centro de ensino escolhido para gerar os relatórios dos cursos pertencentes ao mesmo
    :type centro_de_ensino: String
    :param dbName: Nome do banco de dados que está sendo manipulado
    :type dbName: str
    """

    cursos = collection_instrumento.distinct('nm_curso', {'centro_de_ensino': centro_de_ensino})
    for curso in cursos:
        
        res_compor_intro: dict = compor_introducao(collectionCentroPorAno, collectionCursosPorCentro, arquivo_intro, ano, centro_de_ensino, modal)
        if res_compor_intro['Success'] == False: 
            return {'Success': False, 'Error': res_compor_intro['Error']}
        
        res_compor_conclusao: dict = compor_conclusao(collectionCursosPorCentro, arquivo_conclusao, ano, curso, modal)
        if res_compor_conclusao['Success'] == False:
            return {'Success': False, 'Error': res_compor_conclusao['Error']} 
        
        res_gerar_relatorios: dict = gerar_relatorio_por_curso(curso, collection_instrumento, collectionCursosPorCentro, database_name)
        if res_gerar_relatorios['Success'] == False:
            return {'Success': False, 'Error': res_gerar_relatorios['Error']} 
        
        return {'Success': True}

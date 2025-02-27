import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from src.utils.dict_to_two_lists import dict_to_list
import os
from PIL import Image
from pymongo.collection import Collection
from pymongo.database import Database


def percentage_plot(pct: int, all_values: list[float]) -> list[float]:
    """
    Função para plotar a porcentagem no gráfico de forma visual

    :param pct: Valor usado para realizar o calculo absoluto da porcentagem
    :type pct: Int
    :param allvalues: List contendo as porcentagens
    :type allvalues: List
    :return: retorna as porcentagnes para serem plotadas no gráfico
    :rtype: Int
    """
    absolute = int(pct / 100.*np.sum(all_values))
    return "{:.2f}%".format(pct, absolute) if pct > 0 else ''

def graph_plot(sub_dir_name: str, dir_saida_fig: Path, cod_curso: int, cod_subgrupo: int, options: list[str], percentage: list[float], num_pergunta: int, pergunta: str) -> Path:
    """
    Função que cria a figura do gráfico

    :param dirSaidaFig: Contém o path para o diretório onde será salvado as figuras.
    :type dirSaidaFig: Path
    :param cod_curso: Contém o codigo do curso que será utilizado para formar o nome da figura
    :type cod_curso: String
    :param cod_subgrupo: Contém o código do sub grupo que será utilizado para formar o nome da figura
    :type cod_subgrupo: String
    :param options: List que contém as opções de respostas que poderiam ser escolhidas
    :type options: List
    :param percentage: List que contém as porcentagens de cada opção que foi escolhida
    :type percentage: List
    :param num_pergunta: Contém o número da pergunta que será utilizado para formar o nome da figura
    :type num_pergnta: String
    :param pergunta: É a pergunta que dará título para a figura que contém o gráfico
    :type pergunta: String
    """

    figGraph_name = f'fig_{cod_curso}_{cod_subgrupo}_{num_pergunta}'
    print(figGraph_name)

    labelLegend = [f'{l}, {s}%' for l, s in zip(options, percentage)]

    wp = {'linewidth': 1, 'edgecolor': "black"}

    fig, ax = plt.subplots(figsize=(13, 7))

    wedges, texts, autotexts = ax.pie(percentage,
                                    autopct=lambda pct: percentage_plot(pct, percentage),
                                    labels=options,
                                    shadow=True,
                                    startangle=90,
                                    wedgeprops=wp,
                                    textprops=dict(color="white"))

    ax.legend(
            title="Opções",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            labels = labelLegend
            )

    plt.setp(autotexts, size=8, weight="bold")
    ax.set_title(f"{pergunta}") 
    fig.savefig(os.path.join(dir_saida_fig, figGraph_name))
    plt.close(fig)

    path = f'{sub_dir_name}/{figGraph_name}'
    return path


def controller_graph_generator(database_name: Database,collection_name: Collection, opcoes: list[str], porcentagem: list[float], cod_curso: int, cd_subgrupo: int, nu_pergunta: int, pergunta:str) -> Path:
    """
    Função que realiza a chamada da função que gera os gráficos para cada documento que estiver no banco de dados.

    :param collectionName: Coleção que contém os documentos que iremos realizar a inserção
    :type collectionName: Collection 
    """

    #Realizando a busca pelo caminho para o diretório em que serão salvos as figuras
    dirFigName = f'figurasGraficos_{database_name}'
    diretorio_trabalho = Path(f'relatorio/markdowns/{database_name}/figurasGrafico/')
    diretorio_trabalho.mkdir(parents=True, exist_ok=True)
    subdiretorio_trabalho = f'./figurasGrafico'

    finalPath = graph_plot(subdiretorio_trabalho, diretorio_trabalho, cod_curso, cd_subgrupo, opcoes, porcentagem, nu_pergunta, pergunta)
    
    return finalPath

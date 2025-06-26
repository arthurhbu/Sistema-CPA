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

    Args:
        pct (int): Um valor em porcentagem do pct_opt.
        all_values (list[float]): Um vetor contendo todos os valores do dict pct_opt.
    Returns:
        list[float]: Retorna uma lista com os valores atualizados.
    Raises:
        None: Não há raise de nenhuma Exception.
    """
    absolute: int = int(pct / 100.*np.sum(all_values))
    return "{:.2f}%".format(pct, absolute) if pct > 0 else ''

def graph_plot(sub_dir_name: str, dir_saida_fig: Path, cod_curso: int, cod_subgrupo: int, options: list[str], percentage: list[float], num_pergunta: int, pergunta: str) -> str:
    """
    Função que cria a figura do gráfico e o coloca no diretório referente do instrumento.

    Args:
        sub_dir_name (str): Nome do subdiretório que será armazenado as imagens.
        dir_saida_fig (Path): Path do diretório onde as figuras ficarão.
        cod_curso (int): Contém o codigo do curso que será utilizado para formar o nome da figura.
        cod_subgrupo (int): Contém o código do sub grupo que será utilizado para formar o nome da figura.
        options (list[str]): Lista que contém as opções de respostas que poderiam ser escolhidas.
        percentage (list[float]): Lista que contém as porcentagens de cada opção que foi escolhida.
        num_pergunta (int): Contém o número da pergunta que será utilizado para formar o nome da figura.
        pergunta (str): É a pergunta que dará título para a figura que contém o gráfico.
    Responses:
        String: Ele retorna o Path relativo em formato de string da figura, para que futuramente possa ser feito a relação da imagem no markdown.
    Raises: 
        None: Não há raise para nenhuma exception.
    """

    figGraph_name: str = f'fig_{cod_curso}_{cod_subgrupo}_{num_pergunta}'
    print(figGraph_name)

    labelLegend: list = [f'{l}, {s}%' for l, s in zip(options, percentage)]

    wp: dict = {'linewidth': 1, 'edgecolor': "black"}

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

    path: str = f'{sub_dir_name}/{figGraph_name}'
    return path


def controller_graph_generator(database_name: str, collection_name: Collection, opcoes: list[str], porcentagem: list[float], cod_curso: int, cd_subgrupo: int, nu_pergunta: int, pergunta:str) -> Path:
    """
    Função que realiza a chamada da função que gera os gráficos para cada documento que estiver no banco de dados.

    Args: 
        database_name (str): Nome do banco de dados/instrumento que será utilizado.
        collection_name (Collection): Collection do csv do instrumento.
        opcoes (list[str]): Lista contendo as opcoes de uma pergunta do instrumento.
        porcentagem (list[float]): Lista contendo a porcentagem de uma pergunta do instrumento.
        cod_curso (int): Código de um curso do instrumento.
        cd_subgrupo (int): Código de um subgrupo do instrumento.
        nu_pergunta (int): Número/Código da pergunta do instrumento.
        pergunta (str): A pergunta para que será gerado a figura.
    """

    #Realizando a busca pelo caminho para o diretório em que serão salvos as figuras
    dri_fig_name: str = f'figurasGraficos_{database_name}'
    diretorio_trabalho: Path = Path(f'relatorio/markdowns/{database_name}/figurasGrafico/')
    diretorio_trabalho.mkdir(parents=True, exist_ok=True)
    subdiretorio_trabalho: str = f'./figurasGrafico'

    final_path: str = graph_plot(subdiretorio_trabalho, diretorio_trabalho, cod_curso, cd_subgrupo, opcoes, porcentagem, nu_pergunta, pergunta)
    
    return final_path

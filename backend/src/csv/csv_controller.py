from pathlib import Path
import pandas as pd 
from pymongo.collection import Collection
from pymongo import MongoClient
from pymongo.database import Database
from pandas import DataFrame
from src.utils.percentage_update_database import percentage_calculator,insert_dict_disciplina,insert_percentage_dict_into_database
from pymongo.errors import PyMongoError
from pandas.errors import EmptyDataError

class CSVManagment:

    def find_path() -> Path:
        """
        Função que retorna o caminho do diretório que está o arquivo csv

        Returns:
            Path: Caminho para o diretório do arquivo csv.
        """
        path: Path = Path(__file__).parent.resolve()
        return path
    
    def csv_filter_pos_graduacao(csv_file_name: str) -> None:
        """
        Função criada para filtragem de CSVs brutos da Pós Graduação provenientes do NPD. Isso é feito adicionando colunas para chegar ao padrão pre-definido pela CPA.
        
        No caso do csv da pos graduação, ele possui parâmetros a mais que não são necessários, por isso, é feito uma manipulação para remover essas colunas e mudar as posições delas, além de adicionar se for de mestrado ou doutorado.
        
        Args:
            csv_file_name (str): Nome do arquivo CSV que será inserido no banco de dados.
        Returns:
            None: Não possui retorno, ele salva o arquivo csv filtrado diretamente no diretório.
        """
        columns_positions_toDrop_mainCsv: list = [0,1,2,3,5,6,7,22]
        cabecalho: list = [   
            'cd_curso',
            'nm_curso',
            'centro_de_ensino',
            'cd_grupo',
            'nm_grupo',
            'cd_subgrupo',
            'nm_subgrupo',
            'cd_disciplina',
            'nm_disciplina',
            'ordem_pergunta',
            'cd_pergunta',
            'nm_pergunta',
            'ordem_opcoes',
            'opcao',
            'respostas',
            'total_do_curso',
        ]

        dir_arquivo: Path = CSVManagment.find_path()

        df_principal: DataFrame = pd.read_csv(f'{dir_arquivo}/CSVs/{csv_file_name}', sep=',', header = 0)

        columns_to_drop_main_csv: list = df_principal.columns[columns_positions_toDrop_mainCsv]
        df_principal = df_principal.drop(columns=columns_to_drop_main_csv)


        df_principal.iloc[:, 2] = df_principal.apply(lambda row: f"{row.iloc[3]} em {row.iloc[2]}", axis=1)

        columns: int = df_principal.columns[3]
        df_principal = df_principal.drop(columns=[columns])

        colums_df = list(df_principal.columns)
        colums_df[0], colums_df[1] = colums_df[1], colums_df[0]
        colums_df[1], colums_df[2] = colums_df[2], colums_df[1]

        df_principal = df_principal[colums_df]

        index = 0
        for coluna in cabecalho:
            df_principal.rename(columns={df_principal.columns[index]: coluna}, inplace=True)
            index+=1 

        df_principal.dropna(subset=['respostas'], inplace=True)
        df_principal.to_csv(f'{dir_arquivo}/CSVs/csvFiltrado.csv', index=False)
    
    def csv_filter_docentes_and_tecnicos(csv_file_name) -> None:
        """
        Função criada para filtragem de CSVs brutos dos docentes e técnicos/agentes provenientes do NPD. Isso é feito removendo e adicionando colunas para chegar ao padrão pre-definido pela CPA.
        
        No caso do instrumento dos docentes e tecnicos, é necessário remover alguams colunas e inserir algumas que não estão presentes.
        
        Args:
            csv_file_name (str): Nome do arquivo CSV que será inserido no banco de dados.
        Returns:
            None: Não possui retorno, ele salva o arquivo csv filtrado diretamente no diretório.
        """
        
        
        cabecalho: list = [   
            'cd_grupo',
            'nm_grupo',
            'cd_subgrupo',
            'nm_subgrupo',
            'ordem_pergunta',
            'cd_pergunta',
            'nm_pergunta',
            'ordem_opcoes',
            'opcao',
            'respostas',
            'total_do_curso'
        ]

        index_columns_to_drop: list = [0,1,2,3,4,14]
        
        dir_arquivo: Path = CSVManagment.find_path()
        df_principal: DataFrame = pd.read_csv(f'{dir_arquivo}/CSVs/{csv_file_name}', sep=',', header = 0)
        
        columns_to_drop: list = df_principal.columns[index_columns_to_drop]
        df_principal = df_principal.drop(columns=columns_to_drop)

        index: int = 0
        for coluna in cabecalho: 
            df_principal.rename(columns={df_principal.columns[index]: coluna}, inplace=True)
            index+=1 
        
        df_principal = df_principal.groupby(['cd_grupo','nm_grupo','cd_subgrupo','nm_subgrupo','ordem_pergunta','cd_pergunta','nm_pergunta','ordem_opcoes','opcao']).sum().reset_index()
        df_principal.insert(0, 'cd_curso', 0)
        df_principal.insert(1, 'nm_curso', '-')
        df_principal.insert(2, 'centro_de_ensino', '-')
        df_principal.insert(7,'cd_disciplina', 0 )
        df_principal.insert(8, 'nm_disciplina', '-')
        print(df_principal)        
        df_principal.to_csv(f'{dir_arquivo}/CSVs/csvFiltrado.csv', index=False) 
        
    def csv_filter_discentes_and_ead(csv_file_name) -> None:
        """
        Função criada para filtragem de CSVs brutos dos discentes e EAD provenientes do NPD. Faz isso removendo e adicionando colunas para chegar ao padrão pre-definido pela CPA.
        
        No caso dos discentes e ead, eles possuem o csv que mais precisa passar por modificações para que ele funcione da maneira correta, sendo a primeira e maior rotina criada.
        
        Args:
            csv_file_name (str): Nome do arquivo CSV que será inserido no banco de dados.
        Returns:
            None: Não possui retorno, ele salva o arquivo csv filtrado diretamente no diretório.
        """

        header_graduacao: int = 22
        pos_drop_column_csvP: list = [0,1,2,3,5,12,13,19]
        pos_drop_column_csvP_sem_serie: list = [0,1,2,3,5,6,18]
        pos_drop_column_csv_cc: list = [1,4,5]
        cabecalho: list = [   
            'cd_curso', 
            'cd_grupo',
            'nm_grupo',
            'cd_subgrupo',
            'nm_subgrupo',
            'cd_disciplina',
            'nm_disciplina',
            'ordem_pergunta',
            'cd_pergunta',
            'nm_pergunta',
            'ordem_opcoes',
            'opcao',
            'respostas',
            'total_do_curso'
        ]
            
        dir_arquivo: Path = CSVManagment.find_path()
        
        df_principal: DataFrame = pd.read_csv(f'{dir_arquivo}/CSVs/{csv_file_name}', sep=',', header = 0)
        df_cursoCentro: DataFrame = pd.read_csv(f'{dir_arquivo}/CSVs/cursos_e_centros.csv', sep=',', header = 0)
        
        if len(df_principal.columns) < header_graduacao:
            columns_to_drop_csv_p: list = df_principal.columns[pos_drop_column_csvP_sem_serie]
            df_principal = df_principal.drop(columns=columns_to_drop_csv_p)
        else:
            columns_to_drop_csv_p = df_principal.columns[pos_drop_column_csvP]
            df_principal = df_principal.drop(columns=columns_to_drop_csv_p)
            header_graduacao = len(df_principal.columns)

        columns_to_drop_csv_cc: list = df_cursoCentro.columns[pos_drop_column_csv_cc]
        df_cursoCentro = df_cursoCentro.drop(columns=columns_to_drop_csv_cc)

        #Substituir nomes do header para evitar erros de nome
        index: int = 0
        for coluna in cabecalho:
            df_principal.rename(columns={df_principal.columns[index]: coluna}, inplace=True)
            index+=1 
        df_cursoCentro.rename(columns={df_cursoCentro.columns[0]: 'cd_curso'}, inplace=True)
        if len(df_principal.columns) == header_graduacao:
            df_principal = df_principal.groupby(['cd_curso', 'cd_grupo','nm_grupo','cd_subgrupo','nm_subgrupo','cd_disciplina','nm_disciplina','ordem_pergunta','cd_pergunta','nm_pergunta','ordem_opcoes','opcao']).sum().reset_index()
        df_final = pd.merge(df_principal, df_cursoCentro, on='cd_curso', how='outer')
        df_final.drop_duplicates(inplace=True)

        cabecalho.insert(1, 'Nome_Do_Curso')
        cabecalho.insert(2, 'Centro_de_Ensino')

        df_final = df_final[cabecalho]

        print(df_final)
        df_final.dropna(subset=['respostas'], inplace=True)
        df_final.to_csv(f'{dir_arquivo}/CSVs/csvFiltrado.csv', index=False) 

    def csv_filter_egressos(csv_file_name) -> None:
        """
        Função criada para filtragem de CSVs brutos dos Egressos provenientes do NPD. Faz isso removendo e adicionando colunas para chegar ao padrão pre-definido pela CPA.
        
        No caso dos Egresso, é necessário realizar mudanças simples, mas ele é extremamente semelhante com a dos Discentes. 
        
        Args:
            csv_file_name (str): Nome do arquivo CSV que será inserido no banco de dados.
        Returns:
            None: Não possui retorno, ele salva o arquivo csv filtrado diretamente no diretório.
        """
        columns_positions_toDrop_csv_cursoEcentro: list = [1,4,5]
        columns_positions_toDrop_mainCsv: list = [0,1,2,3,5,15]
        cabecalho: list = [   
            'cd_curso', 
            'cd_grupo',
            'nm_grupo',
            'cd_subgrupo',
            'nm_subgrupo',
            'cd_disciplina',
            'nm_disciplina',
            'ordem_pergunta',
            'cd_pergunta',
            'nm_pergunta',
            'ordem_opcoes',
            'opcao',
            'respostas',
            'total_do_curso'
        ]

        dir_arquivo: Path = CSVManagment.find_path()
        
        df_principal: DataFrame = pd.read_csv(f'{dir_arquivo}/CSVs/{csv_file_name}', sep=',', header = 0)
        df_cursoCentro: DataFrame = pd.read_csv(f'{dir_arquivo}/CSVs/cursos_e_centros.csv', sep=',', header = 0)

        columns_to_drop_main_csv: list = df_principal.columns[columns_positions_toDrop_mainCsv]
        df_principal = df_principal.drop(columns=columns_to_drop_main_csv)

        columns_to_drop_centroEcurso_csv: list = df_cursoCentro.columns[columns_positions_toDrop_csv_cursoEcentro]
        df_cursoCentro = df_cursoCentro.drop(columns=columns_to_drop_centroEcurso_csv)

        df_principal.insert(5, 'cd_disciplina', 0)
        df_principal.insert(6, 'nm_disciplina', '-')

        index: int = 0
        for coluna in cabecalho:
            df_principal.rename(columns={df_principal.columns[index]: coluna}, inplace=True)
            index+=1 
        df_cursoCentro.rename(columns={df_cursoCentro.columns[0]: 'cd_curso'}, inplace=True)

        df_final = pd.merge(df_principal, df_cursoCentro, on='cd_curso', how='outer')
        df_final.drop_duplicates(inplace=True)

        cabecalho.insert(1, 'Nome_Do_Curso')
        cabecalho.insert(2, 'Centro_de_Ensino')

        df_final = df_final[cabecalho]

        df_final.dropna(subset=['respostas'], inplace=True)
        df_final.to_csv(f'{dir_arquivo}/CSVs/csvFiltrado.csv', index=False)
    
    def insert_main_csv_to_database(collection_name: Collection, csv_file_name: str, modalidade: str) -> str | Exception:
        """
        Realiza a inserção dos dados provenientes do CSV do instrumento no banco de dados utilizando data frames, além de realizar a filtragem do csv.
        
        Args:
            collection_name (Collection): Collection do instrumento principal.
            csv_file_name (str): String contendo o nome do arquivo csv.
            modalidade (str): Modalidade/tipo do instrumento.
        Returns:
            String | Exception: Ele retorna ou uma string sinalizando que foi finalizado, ou uma exceção que pode vir acontecer na função.
        Raises:
            raise: Não há raises, apenas returns com as Exceptions geradas.
        
        """
        try:
            
            if modalidade == 'Discente' or modalidade == 'EAD':
                CSVManagment.csv_filter_discentes_and_ead(csv_file_name)
            elif modalidade == 'Docente' or modalidade == 'Agente':
                CSVManagment.csv_filter_docentes_and_tecnicos(csv_file_name)
            elif modalidade == 'Egresso':
                CSVManagment.csv_filter_egressos(csv_file_name)
            else: 
                return 'Modalidade não encontrada'
            
            filterCsv = 'csvFiltrado.csv'
            dirArquivo = CSVManagment.find_path()
            df = pd.read_csv(f'{dirArquivo}/CSVs/{filterCsv}', sep=',', header = 0)

            cabecalho = [
                'cd_curso', 
                'nm_curso', 
                'centro_de_ensino', 
                'cd_grupo',
                'nm_grupo',
                'cd_subgrupo',
                'nm_subgrupo',
                'cd_disciplina',
                'nm_disciplina',
                'ordem_pergunta',
                'cd_pergunta',
                'nm_pergunta',
                'ordem_opcoes',
                'opcao',
                'respostas',
                'total_do_curso']


            print('Inserindo infos no banco: \n')
            temp_pctdict = {}
            for i in range(len(df)):
                print(f"        %{round(100*i/len(df), 0)}")

                pergunta_atual = df.iloc[i,11]
                proxima_pergunta = df.iloc[i+1,11] if i < len(df)-1 else None

                temp_pctdict.update({df.iloc[i,13]: int(df.iloc[i,14])})

                if pergunta_atual != proxima_pergunta or (i+1) == len(df):
                    
                    nm_disciplina = df.iloc[i,8]
                    cd_disciplina = df.iloc[i,7]
                    
                    opcao_e_pct = percentage_calculator(temp_pctdict, int(df.iloc[i,15]))

                    collection_name.insert_one(
                        {
                        cabecalho[0]: int(df.iloc[i,0]),    #codigo_curso
                        cabecalho[1]:f'{df.iloc[i,1]}',     #nome_do_curso
                        cabecalho[2]: f'{df.iloc[i,2]}',    #centro_de_ensino
                        cabecalho[3]: int(df.iloc[i,3]),    #codigo_grupo
                        cabecalho[4]: str(df.iloc[i,4]),    #nome_grupo
                        cabecalho[5]: int(df.iloc[i,5]),    #codigo_subgrupo
                        cabecalho[6]: f'{df.iloc[i,6]}',    #nome_subgrupo
                        cabecalho[7]: int(df.iloc[i,7]),    #codigo_disciplina
                        cabecalho[8]: str(df.iloc[i,8]),    #nome_disciplina
                        cabecalho[9]: int(df.iloc[i,9]),    #ordem_pergunta
                        cabecalho[10]: int(df.iloc[i,10]),  #codigo_pergunta 
                        cabecalho[11]: f"{df.iloc[i,11]}",  #nome_pergunta
                        cabecalho[12]: int(df.iloc[i,12]),  #ordem_opcao
                        cabecalho[15]: int(df.iloc[i,15])   #total_do_curso
                        }
                    )

                    if nm_disciplina == '-' and (cd_disciplina == 0.0 or cd_disciplina == 0):
                        insert_percentage_dict_into_database(
                            collection_name, 'pct_por_opcao', opcao_e_pct, 
                            'cd_curso', int(df.iloc[i,0]), 
                            'cd_pergunta', int(df.iloc[i,10])
                        )
                    else:
                        insert_dict_disciplina(
                            collection_name, 'pct_por_opcao', opcao_e_pct, 
                            'cd_curso', int(df.iloc[i,0]), 
                            'cd_pergunta', int(df.iloc[i,10]), 
                            'cd_disciplina', int(df.iloc[i,7])
                        )

                    temp_pctdict = {}  # Reseta o dicionário para o próximo grupo
                    
            return 'Finalizado'
        except FileNotFoundError as e:
            return f"Arquivo não encontrado: {e}"
        except EmptyDataError as e:
            return f"O arquivo CSV está vazio ou corrompido: {e}"
        except KeyError as e:
            return f"Coluna não encontrada: {e}"
        except IndexError as e:
            return f"Erro de índice: {e}"
        except TypeError as e:
            return f"Erro de tipo: {e}"
        except ValueError as e:
            return f"Erro de valor: {e}"
        except PermissionError as e:
            return f"Permissão negada para salvar o arquivo: {e}"
        except PyMongoError as e:
            return f"Erro no MongoDB: {e}"
        except Exception as e:
            return f"Erro inesperado: {e}"

    def insert_curso_e_centro_csv_to_database(collection_name: Collection) -> str | Exception:
        '''
        Realiza a inserção do CSV curso e centro no database. 
        
        Args:
            collection_name (Collection): Collection do csv do instrumento.
        Returns:
            String | Exception: Ele retorna ou uma string sinalizando que foi finalizado, ou uma exceção que pode vir acontecer na função.
        Raises:
            raise: Não há raises, apenas returns com as Exceptions geradas.
        '''
        try: 
            csvArchive = 'cursos_e_centros.csv'
            dirArquivo = CSVManagment.find_path()
            df = pd.read_csv(f'{dirArquivo}/CSVs/{csvArchive}', sep=',', header = 0)

            print(df)

            cabecalho = [
                'cd_curso',
                'codigo_mec',
                'centro_de_ensino',
                'nm_curso',
                'matriculados',
                'ano_referencia'
            ]

            for i in range(len(df)):
                collection_name.insert_one(
                    {
                        cabecalho[0]: int(df.iloc[i,0]),
                        cabecalho[1]: float(df.iloc[i,1]),
                        cabecalho[2]: str(df.iloc[i,2]),
                        cabecalho[3]: str(df.iloc[i,3]),
                        cabecalho[4]: int(df.iloc[i,4]),
                        cabecalho[5]: int(df.iloc[i,5])
                    }
                )
            return 'Finalizado'
        except FileNotFoundError as e:
            return f"Arquivo não encontrado: {e}"
        except pd.errors.EmptyDataError as e:
            return f"O arquivo CSV está vazio ou corrompido: {e}"
        except KeyError as e:
            return f"Coluna não encontrada: {e}"
        except IndexError as e:
            return f"Erro de índice: {e}"
        except TypeError as e:
            return f"Erro de tipo: {e}"
        except ValueError as e:
            return f"Erro de valor: {e}"
        except PermissionError as e:
            return f"Permissão negada para salvar o arquivo: {e}"
        except PyMongoError as e:
            return f"Erro no MongoDB: {e}"
        except Exception as e:
            return f"Erro inesperado: {e}"

    def insert_centro_diretor_csv_database(collection_name: Collection) -> str | Exception:
        '''
        Realiza a inserção do csv centro_diretor no banco de dados.
        
        Args:
            collection_name (Collection): Collection do csv do instrumento.
        Returns:
            String | Exception: Ele retorna ou uma string sinalizando que foi finalizado, ou uma exceção que pode vir acontecer na função.
        Raises:
            raise: Não há raises, apenas returns com as Exceptions geradas.
        '''
        try:
            csvArchive = 'centros_e_diretores.csv'
            dirArquivo = CSVManagment.find_path()
            df = pd.read_csv(f'{dirArquivo}/CSVs/{csvArchive}', sep=',', header = 0)
            print(df)
            cabecalho = [
                'centro_de_ensino',
                'centro_descricao',
                'diretor',
                'diretor_adjunto',
                'ano_da_direcao'
            ]
            for i in range(len(df)):
                collection_name.insert_one(
                    {
                        cabecalho[0]: str(df.iloc[i,0]),
                        cabecalho[1]: str(df.iloc[i,1]),
                        cabecalho[2]: str(df.iloc[i,2]),
                        cabecalho[3]: str(df.iloc[i,3]),
                        cabecalho[4]: str(df.iloc[i,4]),
                    }
                )
            return 'Finalizado'
        except FileNotFoundError as e:
            return f"Arquivo não encontrado: {e}"
        except pd.errors.EmptyDataError as e:
            return f"O arquivo CSV está vazio ou corrompido: {e}"
        except KeyError as e:
            return f"Coluna não encontrada: {e}"
        except IndexError as e:
            return f"Erro de índice: {e}"
        except TypeError as e:
            return f"Erro de tipo: {e}"
        except ValueError as e:
            return f"Erro de valor: {e}"
        except PermissionError as e:
            return f"Permissão negada para salvar o arquivo: {e}"
        except PyMongoError as e:
            return f"Erro no MongoDB: {e}"
        except Exception as e:
            return f"Erro inesperado: {e}"

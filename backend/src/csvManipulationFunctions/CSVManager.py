from pathlib import Path
import pandas as pd 
from pymongo.collection import Collection
from pymongo import MongoClient
from pymongo.database import Database
from src.supportFunctions.percentageUpdateBD import *
from pymongo.errors import PyMongoError
from pandas.errors import EmptyDataError

class CSVManagment:

    def verifierMainCsv(verifier: str, collectionName: Collection) -> bool:
        """
        Função que verifica se os dados do CSV já foram inseridos no banco de dados

        :param verifier: Um valor a ser verificado no banco para ver se os dados já foram inseridos
        :type verifier: String or Int
        :param collectionName: Collection que estamos utilizando
        :type collectionName: Collection
        :return: Boolean que mostra se os dados estão no banco ou não
        :rtype: Boolean
        """
        for document in collectionName.find().limit(1):
            if document["cd_curso"] == verifier:
                return True
            return False

    def CSVReader() -> None:
        """
        Função que retorna o nome do arquivo CSV que será usado.

        :return: Nome do arquivo CSV que será usado
        :rtype: String
        """
        nameArchCSV = input("Digite o nome do arquivo CSV: ")
        return nameArchCSV
    
    def findPath() -> None:
        """
        Função que retorna o caminho do diretório que está o arquivo csv

        :return: Path para o arquivo onde está o arquivo CSV
        :rtype: Path
        """
        path = Path(__file__).parent.resolve()
        return path

    def bruteCSVFilter(csvFileName) -> None:
        
        #USADO SOMENTE PARA OS CSV DE GRADUAÇÃO QUE POSSUEM SERIE, PARA OS OUTROS A FUNÇÃO ACABA NÃO SENDO NECESSÁRIA.

        header_graduacao = 22
        posDropColumnCSVP = [0,1,2,3,5,12,13,19]
        posDropColumnCSVP_SemSerie = [0,1,2,3,5,6,18]
        posDropColumnCSVCC = [1,4,5]
        cabecalho = [   
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
            'total_do_curso']
            
        dirArquivo = CSVManagment.findPath()
        
        df_principal = pd.read_csv(f'{dirArquivo}/CSVs/{csvFileName}', sep=',', header = 0)
        df_cursoCentro = pd.read_csv(f'{dirArquivo}/CSVs/cursos_e_centros.csv', sep=',', header = 0)
        
        if len(df_principal.columns) < header_graduacao:
            columnsToDrop_CSVP = df_principal.columns[posDropColumnCSVP_SemSerie]
            print(columnsToDrop_CSVP)
            df_principal = df_principal.drop(columns=columnsToDrop_CSVP)
        else:
            columnsToDrop_CSVP = df_principal.columns[posDropColumnCSVP]
            df_principal = df_principal.drop(columns=columnsToDrop_CSVP)
            header_graduacao = len(df_principal.columns)

        columnsToDrop_CSVCC = df_cursoCentro.columns[posDropColumnCSVCC]
        df_cursoCentro = df_cursoCentro.drop(columns=columnsToDrop_CSVCC)

        #Substituir nomes do header para evitar erros de nome
        index = 0
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
        df_final.to_csv(f'{dirArquivo}/CSVs/csvFiltrado.csv', index=False) 


    def insertMainCSVtoDatabase(collectionName: Collection, csvFileName: str) -> print:
        """
        Realiza a leitura do arquivo csv transformando ele em um dataframe temporário (OBS: Futuramente talvez seja interessante dropar esse dataframe)
        
        :param database: O banco de dados que será feito as inserções
        :type database: Database
        :param collectionName: Coleção que será feito as insertions e updates
        :type: Collection 
        """
        try:
            CSVManagment.bruteCSVFilter(csvFileName)
            filterCsv = 'csvFiltrado.csv'
            dirArquivo = CSVManagment.findPath()
            df = pd.read_csv(f'{dirArquivo}/CSVs/{filterCsv}', sep=',', header = 0)

            print(df.columns.values)
            #O cabeçalho terá um formato padrão para evitar erros e problemas futuros, apenas sendo necessário manter a ordem de cada coluna
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

            # if CSVManagment.verifierMainCsv(df.iloc[0,0], collectionName) == True:
            #     return print("Os dados já foram inseridos no banco!")

            print('Inserindo infos no banco: \n')
            temp_pctdict = {}
            for i in range(len(df)):
                # print(f"        %{round(100*i/len(df), 0)}")
            
                disciplina_anterior = df.iloc[i-1, 7] if i > 0 else None
                disciplina_atual = df.iloc[i, 7]
                proxima_disciplina = df.iloc[i+1, 7] if i < len(df)-1 else None

                pergunta_anterior = df.iloc[i-1,11] if i > 0 else None
                pergunta_atual = df.iloc[i,11]
                proxima_pergunta = df.iloc[i+1,11] if i < len(df)-1 else None

                temp_pctdict.update({str(df.iloc[i,13]): int(df.iloc[i,14])})

                if pergunta_atual != proxima_pergunta or (i+1) == len(df):
                    
                    nm_disciplina = df.iloc[i,8]
                    cd_disciplina = df.iloc[i,7]
                    
                    opcao_e_pct = percentageCalculator(temp_pctdict, int(df.iloc[i,15]))

                    collectionName.insert_one(
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

                    if nm_disciplina == '-' and cd_disciplina == 0.0:
                        insertPercentageDictIntoDB(
                            collectionName, 'pct_por_opcao', opcao_e_pct, 
                            'cd_curso', int(df.iloc[i,0]), 
                            'cd_pergunta', int(df.iloc[i,10])
                        )
                    else:
                        insertDictDisciplina(
                            collectionName, 'pct_por_opcao', opcao_e_pct, 
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


    def insertCursoeCentroCSVtoDatabase(collectionName: Collection) -> print:
        '''
        Realiza a leitura do csv cursos e centros e faz a inserção dos dados no banco de dados
        
        :param collectionName: Coleção que será feito as insertions e updates
        :type: Collection 
        '''
        # csvArchive = CSVManagment.CSVReader()
        try: 
            csvArchive = 'cursos_e_centros.csv'
            dirArquivo = CSVManagment.findPath()
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
                # print(f"Inserindo infos no banco: %{round(100*i/len(df), 0)}")
                collectionName.insert_one(
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

    def insertCentroDiretorCSVDatabase(collectionName: Collection) -> print:
        '''
        Realiza a leitura do csv centro e diretor e faz a inserção dos dados no banco de dados
        
        :param collectionName: Coleção que será feito as insertions e updates
        :type: Collection 
        '''
        # csvArchive = CSVManagment.CSVReader()
        try:
            csvArchive = 'centros_e_diretores.csv'
            dirArquivo = CSVManagment.findPath()
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
                collectionName.insert_one(
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

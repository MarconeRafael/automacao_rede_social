import pandas as pd
from datetime import datetime
import os
import pandas as pd

def filtrar_perfis(dados_csv, nichos_aceitaveis, quantidade_minima_seguidores, quantidade_maxima_seguidores):
    """
    Filtra perfis de prestadores de serviço com base no número de seguidores e nichos aceitáveis.

    Parâmetros:
    - dados_csv (str): Caminho para o arquivo CSV contendo os dados.
    - nichos_aceitaveis (list): Lista de nichos aceitáveis.
    - quantidade_minima_seguidores (float): Número mínimo de seguidores.
    - quantidade_maxima_seguidores (float): Número máximo de seguidores.

    Retorna:
    - DataFrame: Um DataFrame contendo os perfis filtrados.
    """
    # Carregar o CSV gerado anteriormente
    df = pd.read_csv(dados_csv)

    # Filtrar perfis que são prestadores de serviço
    df_prestadores = df[df['Is_Enterprise_Label'] == 'Prestador de Serviço']

    # Filtrar perfis com número de seguidores dentro do intervalo especificado
    df_prestadores['seguidores'] = df_prestadores['seguidores'].apply(
        lambda x: float(
            str(x)
            .replace(' mil seguidores', '')
            .replace(' mi seguidores', '000')
            .replace(' seguidores', '')
            .replace(',', '.')
        )
    )
    df_prestadores = df_prestadores[
        (df_prestadores['seguidores'] >= quantidade_minima_seguidores) & 
        (df_prestadores['seguidores'] <= quantidade_maxima_seguidores)
    ]

    # Filtrar perfis cujo nicho esteja na lista de nichos aceitáveis
    df_prestadores = df_prestadores[df_prestadores['Niche'].isin(nichos_aceitaveis)]

    return df_prestadores

# teste de uso:
#dados_csv = "csvs/dados.csv"
# nichos_aceitaveis = ["Beleza", "Tecnologia", "Educação"]
# quantidade_minima_seguidores = 1000
# quantidade_maxima_seguidores = 100000
# perfis_filtrados = filtrar_perfis(dados_csv, nichos_aceitaveis, quantidade_minima_seguidores, quantidade_maxima_seguidores)
# print(perfis_filtrados)
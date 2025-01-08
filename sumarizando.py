import pandas as pd
from transformers import pipeline
import re
import os
numerostr = os.environ.get('numero', '2')
numero = int(numerostr)
# Função para gerar resumos
def gerar_resumo(texto, summarizer, max_length=150):
    try:
        resumo = summarizer(texto, max_length=max_length, min_length=50, do_sample=False)
        return resumo[0]['summary_text']
    except Exception as e:
        return f"Erro ao gerar resumo: {str(e)}"

# Função para extrair o nome de usuário da URL
def extrair_username(url):
    match = re.search(r'https://www.instagram.com/([a-zA-Z0-9._]+)', url)
    if match:
        return match.group(1)
    return url  # Retorna a URL original caso não consiga extrair o nome de usuário

# Função principal
def processar_arquivo(filename):
    # Carregar o DataFrame
    df_filtrado = pd.read_csv(filename)

    # Verificar o conteúdo do DataFrame
    print("Forma do DataFrame original:", df_filtrado.shape)
    print(df_filtrado.head())


    # Certificar-se de que a coluna 'bio' não contém valores vazios 
    df_filtrado = df_filtrado.dropna(subset=['bio'])

    # Verificar se há bios para processar
    if df_filtrado.empty:
        print("Não há bios para processar.")
    else:
        # Coluna de texto que contém as bios
        coluna_texto = 'bio'

        # Carregar o pipeline de resumo do Hugging Face (modelo T5 para resumo)
        summarizer = pipeline("summarization", model="t5-small", device=-1)  # device=-1 para usar a CPU
        if numero ==1:
            # Aplicar a função de extração de nome de usuário
            df_filtrado['Username'] = df_filtrado['Username'].apply(extrair_username)
        else:
            df_filtrado['Username'] = 'fullName'
        # Aplicar o modelo de resumo nas bios
        df_filtrado['resumo_bio'] = df_filtrado[coluna_texto].apply(lambda x: gerar_resumo(x, summarizer))
        
        # Selecionar apenas as colunas desejadas

        if numero ==1:
            df_resultado = df_filtrado[['Username', 'Niche', 'Is_Enterprise_Label', 'resumo_bio']]
        else:
             df_resultado = df_filtrado[['Username', 'Niche', 'resumo_bio']]

        # Exibir as novas colunas (resumo)
        print(df_resultado.head())

        # Salvar os resultados em um novo CSV
        path_resumo = 'csvs/resultados_com_resumos.csv'
        df_resultado.to_csv(path_resumo, index=False)
        return path_resumo
#processar_arquivo(filename)
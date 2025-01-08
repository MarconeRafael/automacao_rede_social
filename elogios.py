from openai import OpenAI
from keys import chave_openai
client = OpenAI(api_key=chave_openai)
import pandas as pd

# Função para gerar elogio usando GPT-4
def gerar_elogio(username, niche, bio):
    prompt = (
        f"Crie um elogio amigável e personalizado em português para o seguinte perfil:\n"
        f"Nome: {username}\n"
        f"Nicho: {niche}\n"
        f"Bio: {bio}\n"
        f"Elogio:"
    )
    try:
        response = client.chat.completions.create(model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um assistente que cria mensagens amigáveis e elogiosas em português."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.7)
        elogio = response.choices[0].message.content.strip()
        return elogio
    except Exception as e:
        return f"Erro: {e}"

#Teste
#df_para_elogio = pd.read_csv("csvs/resultados_com_resumos.csv")
# Aplicar a função a cada linha do DataFrame
#df_para_elogio['Elogio'] = df_para_elogio.apply(lambda row: gerar_elogio(row['Username'], row['Niche'], row['resumo_bio']), axis=1)
#df_para_elogio['Elogio'] = df_para_elogio.apply(lambda row: gerar_elogio(row['Username'], row['Niche'], row['resumo_bio']), axis=1)


# Salvar o resultado em um novo CSV
#df_para_elogio.to_csv("csvs/resultados_com_elogios.csv", index=False)
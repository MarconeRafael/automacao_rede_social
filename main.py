from keyword_scraper import * #login_instagram, search_hashtag_and_collect_post_links, collect_profile_from_post
from bio_analyzer import get_bio_from_profile
from filtrar_perfis import filtrar_perfis
import os
from sumarizando import processar_arquivo
from elogios import gerar_elogio
from bootI import executar_automacao
from keys import IG_USERNAME, IG_PASSWORD, maximo_seguidores, minimo_seguidores
from tratamento_dados import process_csv
import pandas as pd
from classificacao_público_conectepubli import carregar_dados, classificar_com_keywords, predict, salvar_resultados
os.environ['TESSDATA_PREFIX'] = '/usr/share/'

# Recupera as credenciais de login das variáveis de ambiente
#username = os.getenv("IG_USERNAME")
#password = os.getenv("IG_PASSWORD")
username = IG_USERNAME
password = IG_PASSWORD
# Verifica se as credenciais estão definidas

csv_dir = 'csvs'
2
numero = int(input("""
Digite:
       01 - para raspar dados do instagram
       02 - para trabalhar com dados importados
    
      
      escolha: """))
#esportando variável
os.environ['numero'] = str(numero)

if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)

def escolha(numero):
    if numero == 1:
        if not username or not password:
            raise ValueError("Username ou Password não definidos nas variáveis de ambiente!")

        # Configura o driver do Selenium
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        try:
            # Realiza o login
            login_instagram(driver, username, password)

            # Realiza a busca por hashtag e coleta os links das postagens
            hashtag = "restaurante"
            max_scrolls = 1
            max_posts = 1
            time.sleep(5)
            post_links = search_hashtag_and_collect_post_links(driver, hashtag, max_scrolls, max_posts)

            # Lista para armazenar as URLs dos perfis
            usernames = []

            # Agora coleta os perfis de cada postagem
            for post_url in post_links:
                profile_url = collect_profile_from_post(driver, post_url, usernames)
                if profile_url:
                    usernames.append(profile_url)

            # Exibe os links dos perfis encontrados
            for profile_link in usernames:
                print(f"Link do perfil: {profile_link}")

            # Chama a função para pegar as bios
            df_bios = get_bio_from_profile(driver, usernames)

            # Salvar o DataFrame em um arquivo CSV
            df_bios.to_csv('csvs/user_bios.csv', index=False)

            dados_csv = "csvs/user_bios.csv"

        finally:
            # Fecha o navegador de maneira segura, mesmo se houver um erro
            driver.quit()
        nichos_aceitaveis = ['restaurantgerar_elogioe', 'loja', 'consultoria']
        df_filtrado = filtrar_perfis(dados_csv, nichos_aceitaveis, minimo_seguidores, maximo_seguidores)
        # Gerar o nome do arquivo com data e hora
        filename = f'{csv_dir}/perfis_aceitos.csv'
        

        # Exporte para CSV com a coluna de seguidores já convertida
        df_filtrado.to_csv(filename, index=False)

        return filename

    elif numero == 2:
        path = "csvs/dataset_instagram-scraper-task_2024-12-25_20-02-54-303.csv"
        print("entrando em process_csv")

        filename = process_csv(path, minimo_seguidores, maximo_seguidores)
        return filename
    else:
        while True: # perguntar até ser um número válido
            print("Número inválido!\n")
            numero = int(input("""
            Digite:
                1 - para raspar dados do instagram
                2 - para trabalhar com dados importados
                3 - para cancelar                        
                
                escolha: """))
            filename = escolha(numero)

            if numero == 3:
                break
    

filename = escolha(numero)

# Chamar a função de processamento com o arquivo fornecido
print("entrando em processar_arquivo")
dados_bio_resumida = processar_arquivo(filename)   # isso irá resumir a bio
print("entrando em carregar_dados")
df = carregar_dados(dados_bio_resumida)
print("entrando em classificar_com_keywords")
classificados_keywords = classificar_com_keywords(df['resumo_bio'])
# Realizar a previsão com o modelo BERT
print("Entrando em predict")
resultados_bert = predict(df['resumo_bio'].tolist())
# Adicionar os resultados ao DataFrame
df['classificacao_keywords'] = classificados_keywords
df['classificacao_bert'] = resultados_bert
# Salvar os resultados em um novo arquivo CSV
compativeis = "csvs/classificados_conectepubli.csv"
print("entrando em salvar_resultados")
salvar_resultados(df, compativeis)

# Carregar o arquivo CSV

df_para_elogio = pd.read_csv(compativeis)

# Aplicar a função a cada linha do DataFrame
print("entrando em gerar_elogio")
df_para_elogio['Elogio'] = df_para_elogio.apply(lambda row: gerar_elogio(row['Username'], row['Niche'], row['resumo_bio']), axis=1)

csv_final = "csvs/resultados_com_elogios.csv"
# Salvar o resultado em um novo CSV
df_para_elogio.to_csv(csv_final, index=False)

# Executar o script
print("entrando em bootI")
executar_automacao(csv_final)
"""
# Lista para armazenar os dados do CSV
dados_csv = []

# Leitura do arquivo CSV
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        dados_csv.append({
            "username": row['Username'],
            "elogio": row['Elogio']
        })
# Testando a função com os dados do CSV
for dado in dados_csv:
    username = dado['username']
    elogio = dado['elogio']


"""
import time
import csv
from keyword_scraper import login_instagram
from utils import enviar_mensagem, monitorar_respostas, configurar_bot
from bootII import fboot2  # Importando a função de bootII
from formatador_JSON import gerar_mensagem
import os
numerostr = os.environ.get('numero', '2')
numero = int(numerostr)

# Função principal para executar a automação
def executar_automacao(csv_file_path):
    # Configurar o Instabot
    bot = configurar_bot()
    if numero == 1:
        # Lê os usernames e mensagens do CSV
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                username = row['Username']
                elogio = row['Elogio']

                # Criar a mensagem 1
                mensagem = gerar_mensagem(1, username, elogio)


                # Enviar a mensagem
                enviar_mensagem(bot, username, mensagem)

                # Monitorar respostas continuamente
                while True:
                    resposta = monitorar_respostas(bot)
                    if resposta:  # Se houver uma resposta
                        # Verificar a estrutura da tupla
                        print(f"Conteúdo de resposta: {resposta}")
                        
                        # Supondo que a resposta seja o primeiro elemento da tupla
                        resposta_texto = str(resposta[0])  # Garantir que resposta_texto é uma string
                        

                        fboot2(username, resposta_texto, bot)  # Chama bootII

                    time.sleep(30)  # Verifica respostas a cada meio 1 minuto
    else:
        # Lê os usernames e mensagens do CSV
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                username = row['fullName']
                elogio = row['Elogio']

                # Criar a mensagem 1
                mensagem = gerar_mensagem(1, username, elogio)


                # Enviar a mensagem
                enviar_mensagem(bot, username, mensagem)

                # Monitorar respostas continuamente
                while True:
                    resposta = monitorar_respostas(bot)
                    if resposta:  # Se houver uma resposta
                        # Verificar a estrutura da tupla
                        print(f"Conteúdo de resposta: {resposta}")
                        
                        # Supondo que a resposta seja o primeiro elemento da tupla
                        resposta_texto = str(resposta[0])  # Garantir que resposta_texto é uma string
                        

                        fboot2(username, resposta_texto, elogio, bot)  # Chama bootII

                    time.sleep(30)  # Verifica respostas a cada meio 1 minuto
#Teste
# Caminho do CSV teste
#csv_file_path = "csvs/marcone.csv"
#numero = 1
#executar_automacao(csv_file_path)
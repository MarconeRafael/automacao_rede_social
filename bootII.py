import csv
import time
import json
from textblob import TextBlob
from instabot import Bot  # Usando o Instabot
from bootIII import fboot3  # Importando a função de bootIII
from utils import monitorar_respostas, analisar_sentimento, enviar_mensagem
from formatador_JSON import gerar_mensagem


# Função principal do processo automatizado
def fboot2(username, response, elogio, bot):
    """
    Função chamada ao detectar uma resposta no Instagram.
    Recebe o username que respondeu e a mensagem de resposta como parâmetros.
    """
    # Analisando o sentimento da resposta

    sentimento = analisar_sentimento(response)
    
    if sentimento == "positivo":
        # Criar a mensagem 1
        mensagem2=  gerar_mensagem(2, username, elogio)
        # Enviar a mensagem
        enviar_mensagem(bot, username, mensagem2)
        while True:
            resposta = monitorar_respostas(bot)
            if resposta:  # Se houver uma resposta
                fboot3(username, resposta, bot)  # Chama bootII

            time.sleep(60)  # Verifica respostas a cada 1 minuto


    else:
        # Se o sentimento for negativo, enviar mensagem negativa
        mensagem_negativa = "Estamos à disposição caso precise de nós. Até mais!"
        enviar_mensagem(bot, username, mensagem_negativa)



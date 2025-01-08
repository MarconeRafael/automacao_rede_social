import json
from keys import whatsapp_link  # Importando o link do WhatsApp do arquivo keys.py
from utils import enviar_mensagem, analisar_sentimento

def fboot3(username, resposta2, bot):
    """
    Função chamada após detectar uma resposta positiva.
    Recebe o username e a mensagem 2.
    Agora, o link do WhatsApp é importado de keys.py.
    """
    # Analisar o sentimento da resposta
    sentimento = analisar_sentimento(resposta2)
    
    if sentimento == "positivo":
        # Enviar mensagem positiva com o link do WhatsApp
        mensagem_positiva = f"Perfeito! Aqui está o link do nosso WhatsApp para você tirar dúvidas ou começar sua campanha: {whatsapp_link}\nEstamos à disposição!"
        print(f"Enviando mensagem positiva para @{username}: {mensagem_positiva}")
        enviar_mensagem(bot, username, mensagem_positiva)
    else:
        # Enviar mensagem negativa/neutra
        mensagem_negativa = "Estamos à disposição caso precise de nós. Até mais!"
        print(f"Enviando mensagem negativa para @{username}: {mensagem_negativa}")
        enviar_mensagem(bot, username, mensagem_negativa)

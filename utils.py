from instabot import Bot  
from textblob import TextBlob  
from keys import IG_USERNAME, IG_PASSWORD
import time

def configurar_bot():
    bot = Bot()
    try:
        # Tentando fazer login com cookies desativados (evitar desafios automáticos)
        bot.login(username=IG_USERNAME, password=IG_PASSWORD, use_cookie=False)
    except Exception as e:
        if 'challenge_required' in str(e):
            print("Desafio necessário para login. Responda ao desafio manualmente.")
            while True:
                # Aguarda até o usuário completar o desafio manualmente
                resposta = input("Você resolveu o desafio manualmente? (Digite 'sim' quando estiver pronto): ")
                if resposta.lower() == 'sim':
                    try:
                        # Tenta fazer o login novamente após o desafio ser resolvido
                        bot.login(username=IG_USERNAME, password=IG_PASSWORD, use_cookie=False)
                        print("Login bem-sucedido após resolver o desafio.")
                        break  # Sai do loop após o login bem-sucedido
                    except Exception as e:
                        print(f"Erro ao tentar login após o desafio: {e}")
                else:
                    print("Aguarde enquanto o desafio é resolvido.")
        else:
            time.sleep(60) 
            bot = configurar_bot()
            print(f"Erro no login: {e}")
    return bot


# Função para enviar mensagem no Instagram Direct usando Instabot
def enviar_mensagem(bot, username, mensagem):
    try:
        # Enviar a mensagem usando Instabot
        bot.send_message(mensagem, [username])
        print(f"Mensagem enviada para @{username}.")
    except Exception as e:
        print(f"Erro ao enviar mensagem para @{username}: {e}")
def monitorar_respostas(bot):
    try:
        conversas = bot.get_messages()
        print(f"Tipo de conversas: {type(conversas)}")
        print(f"Conteúdo de conversas: {conversas}")

        if conversas:
            if isinstance(conversas, list):  # Se for uma lista
                for conversa in conversas:
                    if isinstance(conversa, dict):  # Se for um dicionário
                        username = conversa.get('user', 'Desconhecido')
                        mensagem = conversa.get('message', '')
                        print(f"Resposta detectada de @{username}. Mensagem recebida: {mensagem}")
                        return mensagem
                    else:
                        print("Formato de conversa não esperado: Não é um dicionário.")
            elif isinstance(conversas, dict):  # Caso seja um dicionário
                print("Recebendo uma conversa como dicionário. Verificando estrutura...")
                # Se for um dicionário, verifique seu conteúdo
                username = conversas.get('user', 'Desconhecido')
                mensagem = conversas.get('message', '')
                print(f"Resposta detectada de @{username}. Mensagem recebida: {mensagem}")
                return mensagem
            else:
                print("Formato de conversas não esperado.")
                return None
        else:
            print("Nenhuma conversa encontrada.")
            return None
    except Exception as e:
        print(f"Erro ao monitorar respostas: {e}")
        return None



# Função para analisar o sentimento de uma resposta
def analisar_sentimento(resposta):
    """
    Analisa o sentimento da resposta.
    Retorna 'positivo' ou 'negativo'.
    """
    blob = TextBlob(resposta)
    sentimento = blob.sentiment.polarity  # A pontuação de polaridade varia de -1 (negativo) a 1 (positivo)
    
    if sentimento >= 0.4:
        return "positivo"
    else:
        return "negativo"

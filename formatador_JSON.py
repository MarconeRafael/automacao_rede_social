import csv
import json
import os

from keys import whatsapp_link  

# Caminho do arquivo CSV
csv_file_path = "csvs/resultados_com_elogios.csv"

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

# Função para gerar a mensagem com base no número
def gerar_mensagem(numero, username, elogio):
    if numero == 1:
        return (
            f"Oi, @{username}! Tudo bem?\n"
            f"{elogio}\n"
            f"Já pensou em usar campanhas com influenciadores para aumentar suas vendas e alcançar novos públicos?\n"
            f"A Conecte Publi ajuda empresas como a sua a encontrar influenciadores perfeitos para o seu objetivo e orçamento, sem taxas e com pagamento seguro.\n"
            f"Se fizer sentido, posso te mostrar como funciona. O que acha?"
        )
    elif numero == 2:
        return (
            f"Que ótimo, @{username}! 😊\n"
            f"Vou explicar rapidinho como funciona a Conecte Publi:\n"
            f"1) Cadastro gratuito na nossa plataforma no site: https://conectepubli.com/\n"
            f"2) Crie uma campanha na nossa plataforma, especificando objetivos, tipo de conteúdo "
            f"(exemplo reels ou story) e orçamento.\n"
            f"3) Recebe propostas de influenciadores que se encaixam exatamente no que você procura "
            f"(UGC Creators, nano, micro, macro ou Top influenciadores).\n"
            f"4) Aprova e acompanha tudo: Produção do conteúdo, entrega e avaliação final.\n"
            f"5) Pagamentos seguros, o valor só é liberado após aprovação do trabalho entregue.\n"
            f"Nos preocupamos com o seu sucesso, por isso temos uma equipe disponível via "
            f"WhatsApp para te ajudar em cada etapa.\n"
            f"Você quer o nosso contato WhatsApp?"
        )
    else:
        return "Número inválido. Escolha 1 ou 2"

# Função para carregar o conteúdo existente do arquivo JSON
def carregar_mensagens():
    if os.path.exists('mensagens.json'):
        with open('mensagens.json', 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

# Função para salvar mensagens no arquivo JSON
def salvar_mensagens(mensagens):
    with open('mensagens.json', 'w', encoding='utf-8') as file:
        json.dump(mensagens, file, ensure_ascii=False, indent=4)

# Carregar mensagens existentes
mensagens = carregar_mensagens()

# Iterar sobre os dados do CSV e processar cada entrada
for dado in dados_csv:
    username = dado['username']
    elogio = dado['elogio']
    
    # Gerar a mensagem
    mensagem = gerar_mensagem(2, username, elogio)
    
    # Adicionar a nova mensagem à lista
    mensagens.append({
        'username': username,
        'mensagem': mensagem
    })

# Salvar todas as mensagens no arquivo JSON
salvar_mensagens(mensagens)

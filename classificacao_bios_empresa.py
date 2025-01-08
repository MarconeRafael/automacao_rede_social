import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from torch.nn.functional import softmax
from datetime import datetime
import os
# Carregar o CSV
df = pd.read_csv('csvs/dataset_instagram-scraper-task_2024-12-25_20-02-54-303.csv')

# Função para converter a quantidade de seguidores para número
def converter_seguidores(valor):
    if 'mil' in valor:
        return float(valor.split(' ')[0].replace(',', '.')) * 1000
    elif 'mi' in valor:
        return float(valor.split(' ')[0].replace(',', '.')) * 1000000
    else:
        return int(valor.split(' ')[0].replace('.', '').replace(',', ''))

# Aplicando a função para converter os seguidores
df['seguidores'] = df['seguidores'].apply(converter_seguidores)

# Carregar o tokenizer e o modelo BERT para português
tokenizer = BertTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased')
model = BertForSequenceClassification.from_pretrained('neuralmind/bert-base-portuguese-cased', num_labels=2)

# Função para classificar a bio (Pessoa Física ou Prestador de Serviço)
def classify_bio(bio_text):
    inputs = tokenizer(bio_text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Aplicando softmax para obter probabilidades
    probabilities = softmax(outputs.logits, dim=-1)
    
    # 0 -> Pessoa Física, 1 -> Prestador de Serviço
    prediction = torch.argmax(probabilities, dim=-1).item()
    
    # Se for prestador de serviço, extraímos o nicho
    niche = "none"
    if prediction == 1:
        niche = extract_niche(bio_text)
    
    return prediction, probabilities[0][prediction].item(), niche

# Função para extrair o nicho de uma bio de prestador de serviço
def extract_niche(bio_text):
    # Lista de palavras-chave para identificar nichos
    keywords = ['restaurante', 'empresa', 'companhia', 'loja', 'serviço', 'consultoria', 'hotel', 'clínica', 'escritório']
    
    # Procurar palavras-chave na bio
    bio_lower = bio_text.lower()
    found_keywords = [word for word in keywords if word in bio_lower]
    
    # Retornar até 3 palavras-chave
    return " ".join(found_keywords[:3]) if found_keywords else "none"

# Classificar todas as bios e armazenar os resultados
df['Is_Enterprise'], df['Confidence'], df['Niche'] = zip(*df['bio'].apply(lambda bio: classify_bio(bio)))

# Mapeamento para exibir 'Pessoa Física' ou 'Prestador de Serviço'
df['Is_Enterprise_Label'] = df['Is_Enterprise'].map({0: 'Pessoa Física', 1: 'Prestador de Serviço'})
csv_dir = 'csvs'

# Nome do arquivo com data e hora
filename = f'{csv_dir}/classificacao_bios.csv'

# Verificar se o diretório 'csvs' existe; se não, criar
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)
# Exporte para CSV com a coluna de seguidores já convertida
df.to_csv(filename, index=False)

# Exibir algumas classificações
print(df[['Username', 'bio', 'Is_Enterprise_Label', 'Niche', 'Confidence', 'seguidores']].head())
# Definir o diretório 'csvs'



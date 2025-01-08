import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from torch.utils.data import Dataset, DataLoader

# Definir as palavras-chave que representam o público alvo da Conecte Publi
keywords = ["marcas", "criadores de conteúdo", "plataforma", "parcerias", "tecnologia"]

# Carregar o modelo e o tokenizer BERT
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

def carregar_dados(csv_path):
    # Carregar o arquivo CSV com os dados
    df = pd.read_csv(csv_path)
    # Remover linhas com valores nulos na coluna 'resumo_bio'
    df = df.dropna(subset=['resumo_bio'])
    # Converter todos os valores da coluna 'resumo_bio' para strings
    df['resumo_bio'] = df['resumo_bio'].astype(str)
    return df

# Função para tokenizar os textos
def tokenize_function(texts):
    return tokenizer(list(texts), padding=True, truncation=True, return_tensors='pt')

# Classe personalizada Dataset para trabalhar com DataLoader
class BioDataset(Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        return item

    def __len__(self):
        return len(self.encodings['input_ids'])

# Função para classificar os resumos com base nas palavras-chave
def classificar_com_keywords(resumos):
    classificados = []
    for resumo in resumos:
        if any(keyword in resumo.lower() for keyword in keywords):
            classificados.append(1)  # Público alvo
        else:
            classificados.append(0)  # Não é público alvo
    return classificados

# Função para realizar a previsão com o modelo BERT
def predict(textos):
    encodings = tokenize_function(textos)
    dataset = BioDataset(encodings)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=False)
    
    all_preds = []
    with torch.no_grad():
        for batch in dataloader:
            outputs = model(**batch)
            logits = outputs.logits
            preds = torch.argmax(logits, dim=-1)
            all_preds.extend(preds.cpu().numpy())
    
    return all_preds

def salvar_resultados(df, csv_path):
    df.to_csv(csv_path, index=False)
    print(f"Classificação concluída e resultados salvos em '{csv_path}'")




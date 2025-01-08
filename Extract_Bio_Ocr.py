import os
from google.cloud import vision
from PIL import Image

def extract_bio_from_image(image_path):
    try:
        # Verifica se o arquivo existe
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"O arquivo {image_path} não foi encontrado.")

        # Inicializa o cliente do Google Vision
        client = vision.ImageAnnotatorClient()

        # Abre a imagem
        with open(image_path, 'rb') as image_file:
            content = image_file.read()

        # Cria o objeto de imagem para o Google Vision
        image = vision.Image(content=content)

        # Realiza a detecção de texto na imagem
        response = client.text_detection(image=image)
        texts = response.text_annotations

        if texts:
            # O primeiro item da lista 'texts' contém o texto completo
            extracted_text = texts[0].description
            print(f"Texto extraído: {extracted_text}")
            return extracted_text
        else:
            print("Nenhum texto detectado.")
            return "Nenhum texto detectado"

    except Exception as e:
        return f"Erro ao processar a imagem: {e}"

# Testando
image_path = "/home/m/projeto/PubliFlow/imagens/screenshot_0.png"
bio_text = extract_bio_from_image(image_path)
print(f"Texto extraído: {bio_text}")

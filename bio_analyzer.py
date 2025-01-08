import os
import time
import pandas as pd
from selenium.webdriver.common.by import By
from PIL import Image
from pytesseract import image_to_string
from Extract_Bio_Ocr import extract_bio_from_image
def get_bio_from_profile(driver, usernames):
    # Não inicializa o driver aqui, ele é passado como argumento
    data = []
    contador = 0
    for username in usernames:
        try:
            profile_url = f'{username}'
            driver.get(profile_url)
            print(f"Perfil {username} acessado com sucesso")
            time.sleep(8)

            # Extrair o nome de usuário para gerar um nome de arquivo seguro
            username_for_file = username.split('/')[-2]  # Pega o nome de usuário da URL

            # Substitui caracteres não permitidos por '_'
            screenshot_path = f"{username_for_file}_screenshot.png"
            #screenshot_path = f"imagens/screenshot_{contador}.png"
            driver.save_screenshot(screenshot_path)
        


            image_path = "/home/m/projeto/PubliFlow/imagens"
            bio_text = extract_bio_from_image(image_path)
            print(f"Texto extraído: {bio_text}")
            contador += 1
        except Exception as e:
            print(f"Erro ao acessar o perfil {username} {e}")
            data.append([username, 'Erro ao acessar'])

    # Criação do DataFrame com as bios coletadas
    df = pd.DataFrame(data, columns=['Username', 'bio_text'])
    return df

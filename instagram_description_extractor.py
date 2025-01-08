from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time
from keys import IG_USERNAME, IG_PASSWORD
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def login_instagram(driver, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(5)

def collect_instagram_posts(csv_path, driver):
    df = pd.read_csv(csv_path)
    columns = [f"post {i:02d}_description" for i in range(1, 10)] + [f"post {i:02d}_first_comment" for i in range(1, 10)]
    posts_df = pd.DataFrame(columns=columns)

    # Realiza o login uma vez, fora do loop
    login_instagram(driver, IG_USERNAME, IG_PASSWORD)

    for index, row in df.iterrows():
        username = row['Username']
        print(f"Acessando o perfil de {username}")

        # Usa o username como o link completo
        driver.get(username)
        time.sleep(3)

        posts_text = []
        first_comments = []

        for _ in range(5):  # Ajuste de rolagem
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        posts = driver.find_elements(By.XPATH, '//a[contains(@href, "/p/")]')
        print(f"Encontrados {len(posts)} posts para o usuário {username}")

        post_links = [post.get_attribute("href") for post in posts[:9]]

        for post_url in post_links:
            driver.get(post_url)
            time.sleep(3)  # Aguarda mais tempo para garantir que a página carregue

            try:
                # Espera até que a descrição esteja visível
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="C4VMK"]/span')))
                description = driver.find_element(By.XPATH, '//div[@class="C4VMK"]/span').text
                posts_text.append(description if description else "none")

                # Coleta o primeiro comentário
                try:
                    # Espera até que o primeiro comentário esteja visível
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="CMTs"]/div[1]//span')))
                    first_comment = driver.find_element(By.XPATH, '//div[@class="CMTs"]/div[1]//span').text
                    first_comments.append(first_comment if first_comment else "none")
                except Exception as comment_error:
                    print(f"Erro ao coletar primeiro comentário: {comment_error}")
                    first_comments.append("none")

            except Exception as e:
                print(f"Erro ao coletar descrição: {e}")
                posts_text.append("none")
                first_comments.append("none")

        posts_df.loc[index] = posts_text + first_comments + ['none'] * (9 - len(posts_text)) + ['none'] * (9 - len(first_comments))

        # Salvar periodicamente (opcional)
        if (index + 1) % 10 == 0:
            posts_df.to_csv('csvs/instagram_posts.csv', index=False)

    posts_df.to_csv('csvs/instagram_posts.csv', index=False)
    print("Processamento concluído.")

if __name__ == "__main__":
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    csv_path = 'csvs/perfis_aceitos.csv' 
    collect_instagram_posts(csv_path, driver)

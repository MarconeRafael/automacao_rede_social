import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from keys import IG_USERNAME, IG_PASSWORD

def login_instagram(driver, username, password):
    print("Iniciando login no Instagram...")
    driver.get("https://www.instagram.com/accounts/login/")
    #driver.get("https://www.instagram.com")

    time.sleep(5)

    username_input = driver.find_element("name", "username")
    password_input = driver.find_element("name", "password")
    time.sleep(2)

    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)
    print("Login realizado com sucesso!")

def search_hashtag_and_collect_post_links(driver, hashtag, max_scrolls, max_posts):
    print(f"Iniciando a pesquisa da hashtag #{hashtag}...")
    driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
    time.sleep(5)

    post_links = set()
    posts_collected = 0

    for scroll_count in range(max_scrolls):
        print(f"Rolando a página ({scroll_count+1}/{max_scrolls})...")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/p/")]')))
        
        posts = driver.find_elements(By.XPATH, '//a[contains(@href, "/p/")]')
        print(f"{len(posts)} postagens encontradas na página de hashtag.")

        for post in posts:
            if posts_collected >= max_posts:
                print(f"Limite de {max_posts} postagens atingido.")
                return list(post_links)

            post_url = post.get_attribute("href")
            post_links.add(post_url)
            posts_collected += 1

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    return list(post_links)

def collect_profile_from_post(driver, post_url, usernames):
    driver.get(post_url)
    time.sleep(8)

    try:
        profile_link = driver.find_element(By.XPATH, '//a[contains(@href, "/") and not(contains(@href, "/explore"))]').get_attribute("href")
        driver.get(profile_link)
        time.sleep(5)
        profile_url = driver.current_url
        print(f"Perfil encontrado: {profile_url}")
        #usernames.append(profile_url)
        return profile_url
    except Exception as e:
        print(f"Erro ao coletar perfil: {e}")
        return None

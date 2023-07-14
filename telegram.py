import pickle
from time import sleep, asctime
from requests import post
from telethon import TelegramClient, events
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.webdriver.chrome.options import Options
import os

# Configurar las opciones de Chrome

# from binance.client import Client
# client1 = Client(MIAPICTOMA.API_KEY, MIAPICTOMA.API_SECRET)
# sample API_ID from https://github.com/telegramdesktop/tdesktop/blob/f98fdeab3fb2ba6f55daf8481595f879729d1b84/Telegram/SourceFiles/config.h#L220
# or use your own
api_id = 3979768
api_hash = "d7cb423a678000f98d3fcc9388041b6f"

# fill in your own details here
phone = "+573012041605"
session_file = "yefardi"  # use your username if unsure
password = ""  # if you have two-step verification enabled

# contenido de la respuesta automatica


def envio(mess):
    # print('sol',mess)
    post(
        "https://api.telegram.org/bot1672385199:AAGw8Wocay7hrLUJIqNYZmcpZiLPtk-fla8/sendMessage",
        data={"chat_id": "-1146170349", "text": str(mess)},
    )


def deci(mon, red, precio):
    print(mon, red, precio)
    return round(float(mon) / (1 / float(precio)), red)


# Expresión regular para buscar la palabra "prepago"
prepago_regex = re.compile(r"\bprepago\b", re.IGNORECASE)
comercial_regex = re.compile(r"\bcomercial\b", re.IGNORECASE)

# Expresión regular para buscar enlaces de YouTube
youtube_regex = re.compile(r"\.?youtube\.com\/\S+")

if __name__ == "__main__":
    tarea = 16
    chrome_options = Options()
    mobile_emulation = {
        "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36",
    }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument("user-data-dir=C:\\Users\\House\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 7")
    webdriver_service = Service("C:\\Wemade\\chromedriver.exe")
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    # Obtener las cookies del navegador
    # Ruta al archivo que deseas verificar
    ruta_archivo = "cookies.pkl"
    driver.get("https://m.youtube.com/")
    dominio_actual = driver.current_url.split('/')[2]
    print(dominio_actual)


    # Verificar si el archivo existe
    if os.path.isfile(ruta_archivo):
        sleep(5)
        with open("cookies.pkl", "rb") as file:
            cookies = pickle.load(file)
        # Filtrar las cookies para mantener solo las del dominio actual
        cookies_filtradas = [cookie for cookie in cookies if dominio_actual in cookie['domain']]
        # Agregar las cookies al navegador
        # Agregar las cookies al navegador
        # for cookie in cookies_filtradas:
        #     driver.add_cookie(cookie)
    else:
        if input("Igresa para con") == "X":
            cookies = driver.get_cookies()

        # Guardar las cookies en un archivo
        with open("cookies.pkl", "wb") as file:
            pickle.dump(cookies, file)
    driver.get("https://m.youtube.com/")
    client = TelegramClient(session_file, api_id, api_hash, sequential_updates=True)
    group_id = -1001900149179

    @client.on(events.NewMessage(chats=group_id))
    async def handle_new_message(event):
        global tarea
        print(tarea)
        message = event.message
        chat_id = message.chat_id
        text = message.message
        if prepago_regex.search(text) and comercial_regex.search(text):
            print(
                f"Mensaje con la palabra 'prepago' recibido en el grupo {chat_id}: {text}"
            )
            tarea += 1
        if youtube_regex.search(text):
            print(
                f"Mensaje con enlace de YouTube recibido en el grupo {chat_id}: {text}"
            )
            tarea += 1
            url_regex = re.compile(r"https?://\S+")
            urls_encontradas = re.findall(url_regex, text)
            for url in urls_encontradas:
                driver.get(url)
            sleep(10)
            meGusta = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="app"]/div[1]/ytm-watch/div[2]/ytm-single-column-watch-next-results-renderer/ytm-slim-video-metadata-section-renderer/ytm-slim-video-action-bar-renderer/div/yt-smartimation/div/ytm-segmented-like-dislike-button-renderer/div/ytm-toggle-button-renderer[1]/button/yt-touch-feedback-shape/div/div[2]',
                    )
                )
            )
            meGusta.click()
            suscribir = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="app"]/div[1]/ytm-watch/div[2]/ytm-single-column-watch-next-results-renderer/ytm-slim-video-metadata-section-renderer/ytm-slim-owner-renderer/div/ytm-subscribe-button-renderer/yt-smartimation/div/div/div/button/yt-touch-feedback-shape/div/div[2]',
                    )
                )
            )
            suscribir.click()
            driver.save_screenshot("captura.png")
            group_entity = await client.get_entity(group_id)
            await client.send_file(
                group_entity, "captura.png", caption=f"Tarea {tarea}"
            )
            chat_entity = await client.get_entity(6071521816)
            await client.send_file(chat_entity, "captura.png", caption=f"Tarea {tarea}")

    print(asctime(), "-", "Auto-replying...oi")
    client.start(phone, password)
    client.run_until_disconnected()
    print(asctime(), "-", "Stopped!")

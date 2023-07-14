from PIL import Image
import undetected_chromedriver as uc
from dotenv import load_dotenv
from time import sleep, asctime
from requests import post
from telethon import TelegramClient, events
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.webdriver.chrome.options import Options
import os

load_dotenv()
pathProfile = os.getenv("PATH_PROFILE")
profile = os.getenv("PROFILE")
pathChromeDriver = os.getenv("PATH_DRIVER")
api_id = 3979768
api_hash = "d7cb423a678000f98d3fcc9388041b6f"
phone = "+573012041605"
session_file = "yefardi"  # use your username if unsure
password = ""  # if you have two-step verification enabled


def envio(mess):
    post(
        "https://api.telegram.org/bot1672385199:AAGw8Wocay7hrLUJIqNYZmcpZiLPtk-fla8/sendMessage",
        data={"chat_id": "5534289586", "text": str(mess)},
    )


def deci(mon, red, precio):
    print(mon, red, precio)
    return round(float(mon) / (1 / float(precio)), red)


# Expresión regular para buscar la palabra "prepago"
prepago_regex = re.compile(r"\bprepago\b", re.IGNORECASE)
comercial_regex = re.compile(r"\bcomercial\b", re.IGNORECASE)

# Expresión regular para buscar enlaces de YouTube
youtube_regex = re.compile(r"\.?youtube\.com\/\S+")
youtube2_regex = re.compile(r"/youtu\.be/")

if __name__ == "__main__":
    tarea = 0
    options = Options()
    options.add_argument(f"user-data-dir={pathProfile}")
    options.add_argument(f"--profile-directory={profile}")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Linux; Android 11; SM-G9910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36"
    )
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=options)
    driver.set_window_size(600, 800)
    sleep(2)
    driver.get("https://m.youtube.com/")
    client = TelegramClient(session_file, api_id, api_hash, sequential_updates=True)
    group_id = -548326689

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
        if youtube_regex.search(text) or youtube2_regex.search(text):
            print(
                f"Mensaje con enlace de YouTube recibido en el grupo {chat_id}: {text}"
            )
            tarea += 1
            url_regex = re.compile(r"https?://\S+")
            urls_encontradas = re.findall(url_regex, text)
            for url in urls_encontradas:
                driver.get(url)
            sleep(10)
            texto = (
                WebDriverWait(driver, 10)
                .until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            '//*[@id="app"]/div[1]/ytm-watch/div[2]/ytm-single-column-watch-next-results-renderer/ytm-slim-video-metadata-section-renderer/ytm-slim-owner-renderer/div/ytm-subscribe-button-renderer/yt-smartimation/div/div/div/button/div/span',
                        )
                    )
                )
                .text
            )
            if texto != "Suscrito":
                meGusta = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            '//*[@id="app"]/div[1]/ytm-watch/div[2]/ytm-single-column-watch-next-results-renderer/ytm-slim-video-metadata-section-renderer/ytm-slim-video-action-bar-renderer/div/yt-smartimation/div/ytm-segmented-like-dislike-button-renderer/div/toggle-button-with-animated-icon',
                        )
                    )
                )
                meGusta.click()
                suscribir = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            '//*[@id="app"]/div[1]/ytm-watch/div[2]/ytm-single-column-watch-next-results-renderer/ytm-slim-video-metadata-section-renderer/ytm-slim-owner-renderer/div',
                        )
                    )
                )
                suscribir.click()

            sleep(5)
            driver.save_screenshot("cap.png")
            img = Image.open("cap.png")
            cropped = img.crop((0, 0, 566, 712))  # (left, upper, right, lower)
            cropped.save("captura.png")
            group_entity = await client.get_entity(group_id)
            await client.send_file(
                group_entity, "captura.png", caption=f"Tarea {tarea}"
            )
            chat_entity = await client.get_entity(5534289586)
            await client.send_file(chat_entity, "captura.png", caption=f"Tarea {tarea}")

    print(asctime(), "-", "Auto-replying...oi")
    client.start(phone, password)
    client.run_until_disconnected()
    print(asctime(), "-", "Stopped!")

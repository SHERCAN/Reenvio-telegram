from PIL import Image
import undetected_chromedriver as uc
from dotenv import load_dotenv
from time import sleep, asctime
from telethon import TelegramClient, events
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.webdriver.chrome.options import Options
import os
import random

load_dotenv()
pathProfile = os.getenv("PATH_PROFILE")
profile = os.getenv("PROFILE")
pathChromeDriver = os.getenv("PATH_DRIVER")
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")
session_file = "Shercan"
# Mis chats
# grupoChat = -916304576
# comercialChat = 742390776

# Los chats de la piramide
grupoChat = -1001842834987
comercialChat = 5962167568
password = ""

# Expresión regular para buscar la palabra "prepago"
prepago_regex = re.compile(r"\bprepago\b", re.IGNORECASE)
comercial_regex = re.compile(r"\bcomercial\b", re.IGNORECASE)

# Expresión regular para buscar enlaces de YouTube
youtube_regex = re.compile(r"\.?youtube\.com\/\S+")
youtube2_regex = re.compile(r"/youtu\.be/")


class Chrome:
    def optionsChrome(self) -> None:
        self.options = Options()
        self.options.add_argument(f"user-data-dir={pathProfile}")
        self.options.add_argument(f"--profile-directory={profile}")
        self.options.add_argument(
            "--user-agent=Mozilla/5.0 (Linux; Android 11; SM-G9910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36"
        )
        self.options.add_argument("--disable-blink-features=AutomationControlled")

    def openPage(self, page: str) -> None:
        self.optionsChrome()
        self.driver = uc.Chrome(executable_path=pathChromeDriver, options=self.options)
        self.zoom_level = 0.75  # 75% de zoom
        self.driver.execute_script(
            "document.body.style.zoom = '{}';".format(self.zoom_level)
        )
        self.driver.set_window_size(500, 800)
        self.driver.get(page)

    def closePage(self) -> None:
        self.driver.quit()


chrome = Chrome()
if __name__ == "__main__":
    sleep(2)
    client = TelegramClient(session_file, api_id, api_hash, sequential_updates=True)

    @client.on(events.NewMessage(chats=grupoChat))
    async def handle_new_message(event):
        tarea = 0
        message = event.message
        chat_id = message.chat_id
        text = message.message
        numero_mision = re.search(r"Misión: (\d+)", text)
        if numero_mision:
            tarea = numero_mision.group(1)
        if prepago_regex.search(text) and comercial_regex.search(text):
            print(
                f"Mensaje con la palabra 'prepago' recibido en el grupo {chat_id}: {tarea}"
            )
        if youtube_regex.search(text) or youtube2_regex.search(text):
            print(
                f"Mensaje con enlace de YouTube recibido en el grupo {chat_id}: {tarea}"
            )
            url_regex = re.compile(r"https?://\S+")
            urls_encontradas = re.findall(url_regex, text)
            for url in urls_encontradas:
                chrome.openPage(url)
            sleep(10)
            texto = (
                WebDriverWait(chrome.driver, 10)
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
                meGusta = WebDriverWait(chrome.driver, 10).until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            '//*[@id="app"]/div[1]/ytm-watch/div[2]/ytm-single-column-watch-next-results-renderer/ytm-slim-video-metadata-section-renderer/ytm-slim-video-action-bar-renderer/div/yt-smartimation/div/ytm-segmented-like-dislike-button-renderer/div/toggle-button-with-animated-icon',
                        )
                    )
                )
                meGusta.click()
                suscribir = WebDriverWait(chrome.driver, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            '//*[@id="app"]/div[1]/ytm-watch/div[2]/ytm-single-column-watch-next-results-renderer/ytm-slim-video-metadata-section-renderer/ytm-slim-owner-renderer/div',
                        )
                    )
                )
                suscribir.click()

            sleep(5)
            chrome.driver.save_screenshot("cap.png")
            img = Image.open("cap.png")
            cropped = img.crop(
                (0, 0, img.width - 17, img.height)
            )  # (left, upper, right, lower)
            cropped.save("captura.png")
            chrome.closePage()
            numero_aleatorio = random.randint(2, 300)
            sleep(numero_aleatorio)
            group_entity = await client.get_entity(grupoChat)
            await client.send_file(
                group_entity, "captura.png", caption=f"Misión {tarea}"
            )
            chat_entity = await client.get_entity(comercialChat)
            await client.send_file(
                chat_entity, "captura.png", caption=f"Misión {tarea}"
            )

    print(asctime(), "-", "Auto-replying...oi")
    client.start(phone, password)
    client.run_until_disconnected()
    print(asctime(), "-", "Stopped!")

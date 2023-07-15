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


class Variables:
    def __init__(self):
        load_dotenv()
        self.pathProfile = os.getenv("PATH_PROFILE")
        self.profile = os.getenv("PROFILE")
        self.pathChromeDriver = os.getenv("PATH_DRIVER")
        self.api_id = 3979768
        self.api_hash = "d7cb423a678000f98d3fcc9388041b6f"
        self.phone = "+573012041605"
        self.session_file = "yefardi"
        self.password = ""
        self.grupoChat = -548326689
        self.comercialChat = 5534289586
        self.tarea = 0

    def __call__(self):
        return self.__dict__


class Expresiones:
    def __init__(self) -> None:

        # Expresión regular para buscar la palabra "prepago"
        self.prepago_regex = re.compile(r"\bprepago\b", re.IGNORECASE)
        self.comercial_regex = re.compile(r"\bcomercial\b", re.IGNORECASE)

        # Expresión regular para buscar enlaces de YouTube
        self.youtube_regex = re.compile(r"\.?youtube\.com\/\S+")
        self.youtube2_regex = re.compile(r"/youtu\.be/")

    def __call__(self):
        return self.__dict__


class Telegram():
    def __init__(self) -> None:
        self.options = Options()
        self.options.add_argument(f"user-data-dir={Variables().pathProfile}")
        self.options.add_argument(f"--profile-directory={Variables().profile}")
        self.options.add_argument(
            "--user-agent=Mozilla/5.0 (Linux; Android 11; SM-G9910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36"
        )
        self.options.add_argument(
            "--disable-blink-features=AutomationControlled")
        self.driver = uc.Chrome(options=self.options)
        self.driver.set_window_size(600, 800)
        sleep(1)
        self.driver.get("https://m.youtube.com/")
        sleep(1)
        self.client = TelegramClient(
            Variables().session_file, Variables().api_id, Variables().api_hash, sequential_updates=True)


tele = Telegram()


@tele.client.on(events.NewMessage(chats=Variables().grupoChat))
async def handle_new_message(event):
    message = event.message
    chat_id = message.chat_id
    text = message.message
    if Expresiones().prepago_regex.search(text) and Expresiones().comercial_regex.search(text):
        print(
            f"Mensaje con la palabra 'prepago' recibido en el grupo {chat_id}: {text}"
        )
        Variables().tarea += 1
    if Expresiones().youtube_regex.search(text) or Expresiones().youtube2_regex.search(text):
        print(
            f"Mensaje con enlace de YouTube recibido en el grupo {chat_id}: {text}"
        )
        Variables().tarea += 1
        url_regex = re.compile(r"https?://\S+")
        urls_encontradas = re.findall(url_regex, text)
        for url in urls_encontradas:
            tele.driver.get(url)
            print(url)
        sleep(10)
        texto = (
            WebDriverWait(tele.driver, 10)
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
            meGusta = WebDriverWait(tele.driver, 10).until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="app"]/div[1]/ytm-watch/div[2]/ytm-single-column-watch-next-results-renderer/ytm-slim-video-metadata-section-renderer/ytm-slim-video-action-bar-renderer/div/yt-smartimation/div/ytm-segmented-like-dislike-button-renderer/div/toggle-button-with-animated-icon',
                    )
                )
            )
            meGusta.click()
            suscribir = WebDriverWait(tele.driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="app"]/div[1]/ytm-watch/div[2]/ytm-single-column-watch-next-results-renderer/ytm-slim-video-metadata-section-renderer/ytm-slim-owner-renderer/div',
                    )
                )
            )
            suscribir.click()

        sleep(5)
        tele.driver.save_screenshot("cap.png")
        img = Image.open("cap.png")
        cropped = img.crop((0, 0, 566, 712))  # (left, upper, right, lower)
        cropped.save("captura.png")
        group_entity = await tele.client.get_entity(Variables().grupoChat)
        await tele.client.send_file(
            group_entity, "captura.png", caption=f"Tarea {Variables().tarea}"
        )
        chat_entity = await tele.client.get_entity(Variables().comercialChat)
        await tele.client.send_file(chat_entity, "captura.png", caption=f"Tarea {Variables().tarea}")
if __name__ == "__main__":

    print(asctime(), "-", "Auto-replying...oi")
    tele.client.start(Variables().phone, Variables().password)
    tele.client.run_until_disconnected()
    print(asctime(), "-", "Stopped!")

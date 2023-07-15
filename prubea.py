import re
from selenium.webdriver.chrome.options import Options


class Variables:
    def __init__(self):
        self.api_id = 3979768
        self.api_hash = "d7cb423a678000f98d3fcc9388041b6f"
        self.phone = "+573012041605"
        self.session_file = "yefardi"
        self.password = ""
        self.grupoChat = -548326689
        self.comercialChat = 5534289586
        self.tare = 0

    def __call__(self):
        return self.__dict__


setattr(Variables, "tare", 1)
Variables.tare = 2
print(Variables.tare)


class Telegram(Options):
    def __init__(self) -> None:
        self.options = Options
        self.options.add_argument(f"user-data-dir={Variables().pathProfile}")
        self.options.add_argument(f"--profile-directory={Variables().profile}")


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


Expresiones
text = "De http://youtube.com/ caterine"
url_regex = re.compile(r"https?://\S+")
urls_encontradas = re.findall(url_regex, text)
print(urls_encontradas)

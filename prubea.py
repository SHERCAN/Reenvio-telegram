# from time import sleep

# import undetected_chromedriver as uc
# from dotenv import load_dotenv
# import os

# load_dotenv()
# pathProfile = os.getenv("PATH_PROFILE")
# profile = os.getenv("PROFILE")
# pathChromeDriver = os.getenv("PATH_DRIVER")
# from selenium.webdriver.chrome.options import Options

# if __name__ == "__main__":
#     # chrome_options = uc.ChromeOptions()
#     # chrome_options.add_argument(f"user-data-dir={pathProfile}")
#     # chrome_options.add_argument(f"--profile-directory={profile}")
#     # # chrome_options.add_argument(
#     # #     "--window-size=375,812"
#     # # )  # Tamaño de la ventana del dispositivo móvil
#     # chrome_options.add_argument(
#     #     r"--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
#     # )  # Agrega el user-agent de un dispositivo móvil
#     # driver = uc.Chrome(
#     #     options=chrome_options,
#     #     use_subprocess=True,
#     # )
#     # driver.get("https://m.youtube.com/")
#     # sleep(5)

#     options = Options()
#     mobile_emulation = {
#         "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
#         "userAgent": "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36",
#     }
#     # options.add_experimental_option("prefs", mobile_emulation)
#     # "prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})
#     options.add_argument(f"user-data-dir={pathProfile}")
#     options.add_argument(f"--profile-directory={profile}")
#     options.add_argument(
#         "--user-agent=Mozilla/5.0 (Linux; Android 11; SM-G9910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36"
#     )
#     # options.add_argument(f"--user-agent={user_agent}")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     # mobile_emulation = {"deviceName": "iPhone X"}
#     # options.add_experimental_option("mobileEmulation", mobile_emulation)

#     driver = uc.Chrome(options=options)
#     driver.set_window_size(600, 800)
#     driver.get("https://m.youtube.com/watch?v=dAh7fUFGHa0")
#     sleep(10)
#     foto = driver.get_screenshot_as_png()
#     with open("foto.png", "wb") as file:
#         file.write(foto)
#     driver.get("https://www.google.com")
#     sleep(10)

lista =[]
if lista:
    print("Si")
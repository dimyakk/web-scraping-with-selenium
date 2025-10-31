
"""
===============================================================================
Project: InternetSpeedXBot
Author:  Joaquin Albano
Date:    2025-10-14
Version: 1.3.0
Python:  3.12+
-------------------------------------------------------------------------------
Description:
    Este script crea un bot automatizado que:
      1. Mide la velocidad de Internet (download / upload) usando Selenium
         con la web de Speedtest.net.
      2. Publica automáticamente un tweet mencionando al proveedor
         si la velocidad es menor a la contratada, usando Tweepy y la API de X.

    El código está diseñado para ser resiliente ante fallos de red mediante
    un sistema de reintentos (retry) y manejo explícito de excepciones.
-------------------------------------------------------------------------------
Dependencies:
    - selenium >= 4.22.0
    - tweepy >= 4.14.0
    - python-dotenv
    - Google Chrome (instalado y compatible con el driver)

Environment Variables (.env):
    X_API_KEY
    X_API_KEY_SECRET
    X_ACCESS_TOKEN
    X_ACCESS_TOKEN_SECRET

Usage:
    $ python main.py
-------------------------------------------------------------------------------
License:
    MIT License - Este script puede ser utilizado y modificado libremente
    con atribución al autor original.
===============================================================================
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
from dotenv import load_dotenv
import tweepy

load_dotenv()

PROMISED_DOWN = 300
PROMISED_UP = 150
api_key = os.getenv("X_API_KEY")
api_secret = os.getenv("X_API_KEY_SECRET")
access_token = os.getenv("X_ACCESS_TOKEN")
token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

"""InternetSpeedXBot: mide la velocidad de Internet y publica un tweet.

Este módulo contiene la clase `InternetSpeedXBot` y la función `retry()`.
Permite automatizar la medición de velocidad de conexión usando Selenium
y publicar los resultados en X (Twitter) usando la API oficial a través de Tweepy.

Uso típico:
    bot = InternetSpeedXBot()
    bot.get_internet_speed()
    bot.tweet_at_provider()
"""

def retry(func, retries=5, description=""):
    """Reintenta ejecutar una función ante errores temporales de Selenium o red.

        Args:
            func (Callable): Función que se intentará ejecutar.
            retries (int, optional): Número máximo de intentos. Por defecto es 5.
            description (str, optional): Descripción del proceso para imprimir en consola.

        Raises:
            TimeoutException: Si la función falla después de agotar los reintentos.

        Returns:
            Any: El valor retornado por `func` si se ejecuta correctamente.
    """

    for attempt in range(1, retries + 1):
        try:
            return func()
        except TimeoutException:
            print(f"Intento {attempt}/{retries} fallido al {description}. Reintentando...")
            time.sleep(2)
    raise TimeoutException(f"Error: no se pudo completar {description} después de {retries} intentos.")

class InternetSpeedXBot:

    """ Bot que mide la velocidad de Internet y publica un tweet con los resultados.

        Combina Selenium (para obtener los datos de Speedtest.net)
        con Tweepy (para interactuar con la API de X / Twitter).

        Attributes:
            down (float): Velocidad de descarga (Mbps).
            up (float): Velocidad de subida (Mbps).
            driver (webdriver.Chrome): Instancia del navegador controlada por Selenium.
            wait (WebDriverWait): Objeto de espera explícita para sincronización con elementos.

        Example:
            # >>> bot = InternetSpeedXBot()
            # >>> bot.get_internet_speed()
            # >>> bot.tweet_provider()
            🕓 Ejecutando test de velocidad...
            Velocidad de bajada: 125.5
            Velocidad de subida: 48.2
            # >>> bot.tweet_at_provider()
            ✅ Tweet publicado con ID: 1827364519287346
    """

    def __init__(self):

        """Inicializa la instancia y configura el WebDriver de Chrome.

           Crea el navegador con opciones y preferencias predefinidas:
           - perfil de usuario (user-data-dir)
           - bloqueo de permisos (notificaciones, geolocalización, cámara, micrófono)
           - flags para reducir detección de automatización

           No retorna nada. Si la inicialización del driver falla, se propagará la excepción
           correspondiente de Selenium (por ejemplo, `WebDriverException`).
        """

        self.down = 0
        self.up = 0

        # ---------- CONFIGURACION DEL DRIVER E INICIACION DEL NAVEGADOR ----------
        # Evita la detección de automatización
        service = Service()
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Perfil limpio o nuevo (sin cookies viejas de X)
        options.add_argument(f"--user-data-dir={os.getcwd()}/chrome_profile_xbot")

        # Bloquear permisos innecesarios
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.media_stream_mic": 2,
            "profile.default_content_setting_values.media_stream_camera": 2,
        }
        options.add_experimental_option("prefs", prefs)

        # Mantiene abierto el navegador
        options.add_experimental_option("detach", True)

        # Inicio del driver con configuracion y servicio
        self.driver = webdriver.Chrome(service=service, options=options)

        # Espera explícita (para usar más adelante)
        self.wait = WebDriverWait(self.driver, 15)

    def get_internet_speed(self):

        """Ejecuta un test de velocidad en Speedtest.net y guarda los resultados.

            Flujo:
                1. Abre `https://www.speedtest.net`.
                2. Acepta cookies si aparece el banner.
                3. Inicia la prueba de velocidad.
                4. Espera hasta que los resultados estén disponibles.
                5. Guarda la velocidad de descarga (`self.down`) y subida (`self.up`).

            Utiliza `retry()` para manejar errores de red o tiempo de espera.

            Raises:
                TimeoutException: Si los elementos no aparecen dentro del tiempo límite.
                WebDriverException: Si el navegador falla durante la ejecución.

            Example:
                # >>> bot = InternetSpeedXBot()
                # >>> bot.get_internet_speed()
                🕓 Ejecutando test de velocidad...
                Velocidad de bajada: 125.4
                Velocidad de subida: 49.8
        """

        def run_speedtest():
            print("🕓 Ejecutando test de velocidad...")
            self.driver.get("https://www.speedtest.net/")

            time.sleep(10)

            # Aceptar cookies si aparecen
            try:
                cookie_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
                cookie_btn.click()
            except (TimeoutException, NoSuchElementException):
                print("No aparecio el boton de cookies, continuando...")

            self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'start-text'))).click()

            #time.sleep(45)
            self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "result-container-speed")))

            self.down = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span[class*='download-speed']"))).text
            self.up = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span[class*='upload-speed']"))).text

        retry(run_speedtest, description="ejecutar test de velocidad")
        print(f"Velocidad de bajada: {self.down}")
        print(f"Velocidad de subida: {self.up}")

    def tweet_at_provider(self):

        """Publica un tweet en X con los resultados de velocidad de Internet.

        Usa la API oficial de X (Twitter) mediante Tweepy para autenticar y publicar
        automáticamente un tweet que compara la velocidad real con la prometida.

        Raises:
            tweepy.errors.TweepyException: Si ocurre un error de autenticación o conexión.

        Example:
            # >>> bot.tweet_at_provider()
            ✅ Tweet publicado con ID: 1827364519287346
        """

        try:
            client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=token_secret
            )

            response = client.create_tweet(text=f"Porque mi velocidad de internet es de {self.down}Mbps de bajada y {self.up}Mbps de subida? Cuando yo estoy pagando por una subida de "
                                     f"{PROMISED_UP}Mbps y una bajada de {PROMISED_DOWN}Mbps")

            print(f"✅ Tweet publicado con ID: {response.data['id']}")

        except tweepy.errors.TweepyException as e:
            print(f"❌ Error al publicar el tweet: {e}")

if __name__ == "__main__":
    bot = InternetSpeedXBot()
    bot.get_internet_speed()
    bot.tweet_at_provider()
    bot.driver.quit()

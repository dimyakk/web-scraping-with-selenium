# ======== LIBRERÍAS ESTÁNDAR DE PYTHON ========
import os                                                               # Para manejar rutas de archivos y variables de entorno
import time                                                             # Para pausas temporales (sleep) en flujos controlados
import random
from dotenv import load_dotenv                                          # Para leer las credenciales desde un archivo .env (buena práctica)

# ======== SELENIUM CORE ========
from selenium import webdriver                                          # Núcleo para controlar el navegador
from selenium.webdriver.chrome.service import Service                   # Maneja el proceso de ChromeDriver
from selenium.webdriver.chrome.options import Options                   # Permite configurar opciones del navegador

# ======== LOCALIZACIÓN DE ELEMENTOS ========
from selenium.webdriver.common.by import By                             # Para encontrar elementos (por ID, CSS, XPATH, etc.)

# ======== ESPERAS Y CONDICIONES ========
from selenium.webdriver.support.ui import WebDriverWait                 # Para esperas explícitas
from selenium.webdriver.support import expected_conditions as EC        # Condiciones para usar con WebDriverWait

# ======== EXCEPCIONES DE SELENIUM ========
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException
)


class InstFollower:
    """
    Clase principal del bot de Instagram para automatizar acciones de seguimiento de usuarios.

    Esta clase gestiona todo el flujo de automatización con Selenium:
      1. Inicia sesión en Instagram utilizando credenciales almacenadas en variables de entorno.
      2. Cierra las ventanas emergentes post-login ("Guardar información", "Activar notificaciones").
      3. Accede al perfil objetivo y abre la lista de seguidores.
      4. Recorre el modal de seguidores, scrollea dinámicamente y sigue a una cantidad definida de usuarios.

    El bot está diseñado para adaptarse a distintas configuraciones de idioma (español, portugués e inglés)
    y versiones de interfaz de Instagram, utilizando selectores robustos basados en roles, texto visible y
    desplazamientos por eventos de rueda simulados (WheelEvent).

    Atributos:
        driver (webdriver.Chrome): Instancia principal del navegador controlado por Selenium.
        wait (WebDriverWait): Controlador de espera explícita para sincronizar interacciones dinámicas.
        instagram_user (str): Nombre de usuario obtenido desde el archivo `.env` (variable USERNAME).
        instagram_pass (str): Contraseña de la cuenta obtenida desde el archivo `.env` (variable PASSWORD).

    Métodos:
        login():
            Inicia sesión en Instagram con las credenciales configuradas.
        skip_popups():
            Cierra las ventanas emergentes que aparecen tras iniciar sesión.
        find_followers():
            Abre el perfil objetivo y muestra la lista de seguidores.
        follow():
            Sigue automáticamente a una cantidad determinada de usuarios (por defecto 15),
            desplazándose dentro del modal y manejando posibles popups de confirmación.

    Example:
        # >>> from instafollower import InstFollower
        # >>> bot = InstFollower()
        # >>> bot.login()
        Iniciando sesion en Instagram
        # >>> bot.find_followers()
        Ventana de seguidores abierta correctamente.
        # >>> bot.follow()
        [1/15] Seguido.
        ✅ Finalizado. Total seguidos: 15
    """

    def __init__(self):
        # ====================== CONFIGURACIÓN ======================
        load_dotenv()  # Carga las variables desde .env
        self.instagram_user = os.getenv("INTRAGRAM_USERNAME")
        self.instagram_pass = os.getenv("INSTAGRAM_PASSWORD")

        # Configuración del driver
        service = Service()
        options = Options()
        options.add_argument("--start-maximized")                                   #Hace que Chrome se abra directamente maximizado (a pantalla completa)
        options.add_argument("--disable-infobars")                                  #Oculta la barra de información “Chrome is being controlled by automated test software”
        options.add_argument("--disable-extensions")                                #Desactiva todas las extensiones del navegador
        options.add_argument("--disable-blink-features=AutomationControlled")       #Desactiva una API interna de Chrome llamada “AutomationControlled"
        options.add_experimental_option(
            "excludeSwitches",                                                #Elimina el switch interno --enable-automation al iniciar Chrome (deja rastros de
            ["enable-automation"]                                             #automatizacon)
        )
        options.add_experimental_option(                                            #Deshabilita la extensión de automatización que Selenium inyecta automáticamente
            "useAutomationExtension",
            False
        )
        options.add_experimental_option("prefs", {                      #Deshabilita la ventana emergente del navegador para guardar passwords
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        })
        options.add_experimental_option("detach", True)                 #Mantiene abierto el navegador

        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 15)

    def login(self):
        """
        Inicia sesión en Instagram con las credenciales almacenadas en el archivo `.env`.

        Abre la página principal de Instagram, espera la carga del formulario de inicio de sesión,
        completa los campos de usuario y contraseña, y envía el formulario. Una vez dentro,
        ejecuta `skip_popups()` para cerrar las ventanas emergentes post-login.

        Args:
            self: Instancia actual del objeto que contiene el `driver`, `wait`,
                `instagram_user` y `instagram_pass`.

        Raises:
            TimeoutException: Si los campos de login o el botón de envío no se cargan a tiempo.
            NoSuchElementException: Si alguno de los elementos del formulario no existe en el DOM.
            WebDriverException: Si ocurre un error con el navegador o la sesión de Selenium.

        Returns:
            None: No devuelve valor. Muestra en consola el estado del proceso.

        Example:
            # >>> bot = InstaFollower()
            # >>> bot.login()
            Iniciando sesion en Instagram
            Popup 'Guardar información' cerrado con texto: Agora não
            Popups de Instagram manejados correctamente.
        """

        self.driver.get("https://www.instagram.com/")

        time.sleep(5)

        self.wait.until(EC.visibility_of_element_located((By.NAME, 'username'))).send_keys(self.instagram_user)
        self.wait.until(EC.visibility_of_element_located((By.NAME, 'password'))).send_keys(self.instagram_pass)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()

        print('Iniciando sesion en Instagram')

        self.skip_popups()

    def skip_popups(self):
        """
       Cierra las ventanas emergentes que aparecen después del inicio de sesión en Instagram.

       Se manejan dos tipos de popups:
         1. "Guardar información de inicio de sesión"
         2. "Activar notificaciones"

       El método busca los botones correspondientes por texto visible,
       siendo compatible con interfaces en portugués, español e inglés.
       Los textos admitidos se definen en listas (`textos_guardar`, `textos_notificaciones`).

       Args:
           self: Instancia del objeto con `driver` y `wait` activos.

       Raises:
           TimeoutException: Si los popups no aparecen dentro del tiempo de espera.
           NoSuchElementException: Si los botones no existen o cambian de estructura.
           WebDriverException: Si el navegador no responde al intentar clickear un botón.

       Returns:
           None: No devuelve valor. Imprime en consola los textos detectados y acciones realizadas.

       Example:
           # >>> bot.skip_popups()
           Popup 'Guardar información' cerrado con texto: Agora não
           Popup 'Notificaciones' cerrado con texto: Not now
           Popups de Instagram manejados correctamente.
        """

        # Primer popup: Guardar información
        textos_guardar = ["Agora não", "Not now", "Ahora no"]
        for texto in textos_guardar:

            try:
                self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"//div[@role='button' and contains(., '{texto}')]")
                    )
                ).click()
                print(f"Popup 'Guardar información' cerrado con texto: {texto}")
                break

            except (NoSuchElementException, TimeoutException):
                print("Elemento no encontrado, continuando..")

        # Segundo popup: Activar notificaciones
        textos_notificaciones = ["Agora não", "Not now", "Ahora no", "Não agora", "No ahora"]
        for texto in textos_notificaciones:

            try:
                self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                         f"//button[contains(., '{texto}') or //div[@role='button' and contains(., '{texto}')]]")
                    )
                ).click()
                print(f"Popup 'Notificaciones' cerrado con texto: {texto}")
                break

            except (NoSuchElementException, TimeoutException):
                print("Elemento no encontrado, continuando..")

        print("Popups de Instagram manejados correctamente.")


    def find_followers(self):
        """
       Abre el perfil objetivo en Instagram y accede a su lista de seguidores.

       Carga la página del perfil especificado (actualmente fijo como 'chefsteps'),
       espera la visibilidad del enlace 'Seguidores' (`/followers/`),
       y hace clic en él para abrir la ventana modal de la lista de seguidores.

       Args:
           self: Instancia del objeto con `driver` y `wait` activos.

       Raises:
           TimeoutException: Si el enlace de seguidores no se carga a tiempo.
           NoSuchElementException: Si el botón de seguidores no existe o cambió de estructura.
           WebDriverException: Si el navegador se cierra o falla durante la interacción.

       Returns:
           None: No devuelve valor. Imprime mensajes de estado en consola.

       Example:
           # >>> bot = InstaFollower()
           # >>> bot.find_followers()
           Ventana de seguidores abierta correctamente.
       """
        self.driver.get("https://www.instagram.com/chefsteps/")

        try:
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers/')]"))
            ).click()

        except (NoSuchElementException, TimeoutException):
            print("Elemento no encontrado")

    def follow(self):
        """
        Sigue hasta 15 personas desde la lista de seguidores.
        - Trabaja dentro de div[role='dialog'].
        - Scrollea el diálogo con WheelEvent (no depende de clases).
        - Maneja el popup de 'Dejar de seguir' tocando 'Cancelar'.
        - Pausas aleatorias para comportamiento humano.

        Flujo:
        1. Espera el modal de seguidores (div[role='dialog']).
        2. Define un scroll sintético con WheelEvent para no depender de clases internas.
        3. Entra en un bucle hasta lograr 15 follows o 10 iteraciones sin nuevos botones.
        4. Busca botones “Seguir/Follow” dentro del diálogo.
        5. Si no hay, scrollea y reintenta.
        6. Si hay:
            - Centra el botón.
            - Click.
            - Si salta el popup de “Dejar de seguir”, cierra con “Cancelar”.
        7. Pausas aleatorias entre acciones.
        8. Entre tandas, scrollea para cargar más perfiles.
        9. Finaliza con el conteo.

        Args:
        self: Instancia del objeto que contiene el `driver` y `wait` de Selenium.

        Raises:
            TimeoutException: Si la ventana modal de seguidores no se abre a tiempo.
            ElementClickInterceptedException: Si otro elemento (como un popup) bloquea el botón.
            StaleElementReferenceException: Si el DOM cambia antes de interactuar con un botón.
            NoSuchElementException: Si algún botón o diálogo deja de existir durante la ejecución.
            WebDriverException: Si el navegador o la sesión de Selenium se cierran inesperadamente.

        Returns:
            None: No devuelve ningún valor. Imprime mensajes de progreso en consola.

        Example:
            # >>> bot = InstaFollower()
            # >>> bot.login()
            # >>> bot.open_followers("target_account")
            # >>> bot.follow()
            Iniciando secuencia de follow...
            Ventana de seguidores detectada.
            [1/15] Seguido.
            [2/15] Seguido.
            ...
            ✅ Finalizado. Total seguidos: 15

        """

        target = 15
        followed = 0
        print("Iniciando secuencia de follow...")

        try:
            # 1) Esperar el diálogo de seguidores
            dialog = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']")))
            print("Ventana de seguidores detectada.")

            # helper: scroll del diálogo sin conocer clases internas
            def scroll_dialog(amount=800):
                """
                Desplaza hacia abajo el diálogo de seguidores simulando un evento de rueda del mouse.
                Se usa execute_script() que permite ejecutar codigo JavaScript directamente desde el navegador que
                controla Selenium.

                Script: la constante 'dlg' toma como valor el primer argumento que recibe el script (el 'dialog'
                de Python), y luego lanza un evento de scroll artifical (WheelEvent: en JS se dispara cuando el
                usuario gira la rueda del mouse o hace scroll con el tackpad) sobre el dialogo.

                Parametros del evento:
                - deltaY: indica cuanto se desplaza verticalmente hacia abajo.
                - bubbles: en true permite que el evento se propague hacia arriba en el DOM.
                - cancelable: en true permite que el evento pueda ser interceptado o cancelado por scripts de la pagina.

                :param amount: Cantidad de píxeles que se desplaza verticalmente (positivo = hacia abajo).
                :return: None
                """
                try:
                    self.driver.execute_script(
                        """
                        const dlg = arguments[0];
                        dlg.dispatchEvent(new WheelEvent('wheel', { 
                                                            deltaY: arguments[1], 
                                                            bubbles: true,
                                                            cancelable: true 
                        }));
                        """,
                        dialog, amount
                    )
                except (StaleElementReferenceException, NoSuchElementException):
                    pass

            # 2) Bucle principal
            empty_runs = 0
            while followed < target and empty_runs < 10:
                try:
                    # Reobtener el diálogo cada vuelta por si re-renderiza
                    dialog = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
                except NoSuchElementException:
                    print("El diálogo desapareció.")
                    break

                # Botones 'Seguir' o 'Follow' visibles dentro del diálogo
                buttons = dialog.find_elements(
                    By.XPATH, ".//button[normalize-space()='Seguir' or normalize-space()='Follow']"
                )

                if not buttons:
                    empty_runs += 1
                    scroll_dialog(900)
                    time.sleep(random.uniform(0.8, 1.4))
                    continue
                else:
                    empty_runs = 0

                for btn in buttons:
                    if followed >= target:
                        break
                    try:
                        # Llevar al viewport y click
                        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                        time.sleep(random.uniform(0.3, 0.8))
                        btn.click()
                        followed += 1
                        print(f"[{followed}/{target}] Seguido.")
                        time.sleep(random.uniform(1.2, 2.8))  # pausa humana

                    except ElementClickInterceptedException:
                        # Popup 'Dejar de seguir' → 'Cancelar'
                        try:
                            cancel = self.wait.until(
                                EC.element_to_be_clickable((
                                    By.XPATH,
                                    "//div[@role='dialog']//button[contains(., 'Cancelar') or contains(., 'Cancel')]"
                                ))
                            )
                            cancel.click()
                            print("Ya estaba seguido. Cancelado y continuo.")
                            time.sleep(random.uniform(0.8, 1.5))
                        except TimeoutException:
                            pass
                        continue
                    except (StaleElementReferenceException, NoSuchElementException):
                        continue

                # Scroll entre tandas
                scroll_dialog(900)
                time.sleep(random.uniform(0.9, 1.7))

            print(f"✅ Finalizado. Total seguidos: {followed}")

        except TimeoutException:
            print("No se abrió el diálogo de seguidores a tiempo.")
        except Exception as e:
            print(f"Error en follow(): {e}")
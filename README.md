# 🤖 Instagram Follower Bot

Automatiza el seguimiento de usuarios en Instagram usando **Python + Selenium**.  
El bot inicia sesión con tus credenciales, abre la lista de seguidores de un perfil y sigue a un número definido de usuarios, manejando automáticamente los popups y el desplazamiento dentro de la ventana modal.

---

## 🧭 Tabla de contenidos
- [Características](#-características)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Requisitos previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Variables de entorno](#-variables-de-entorno)
- [Detalles técnicos](#-detalles-técnicos)
- [Autor](#-autor)
- [Licencia](#-licencia)

---

## 🚀 Características

- **Inicio de sesión automático** usando credenciales almacenadas en `.env`.
- **Compatibilidad multi-idioma** (Español, Portugués e Inglés).
- **Gestión de popups** (“Guardar información”, “Activar notificaciones”).
- **Scroll dinámico** del modal mediante `WheelEvent` de JavaScript.
- **Simulación de pausas humanas** entre acciones (`random.uniform`).
- **Control de errores**: maneja DOM dinámico y popups de confirmación (“Cancelar”).
- **Documentación completa** con docstrings estilo Google.

---

## 🧱 Estructura del proyecto

```
Instagram Bot/
│
├── instafollower.py    # Clase principal con toda la lógica del bot
├── main.py             # Punto de entrada del programa
├── .env                # Variables de entorno (credenciales)
├── .gitignore          # Exclusión de archivos sensibles
├── README.md           # Documentación del proyecto
└── requirements.txt    # Dependencias del entorno virtual
```

---

## ⚙️ Requisitos previos

- Python **3.12+**
- Google Chrome (instalado)
- Chromedriver (compatible con tu versión de Chrome)
- Cuenta de Instagram válida (sin 2FA durante pruebas)
- Entorno virtual (opcional, pero recomendado)

---

## 📦 Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/dimyakk/instagram-follower-bot.git
cd instagram-follower-bot

# 2. Crear y activar entorno virtual
python -m venv .venv
 # En Linux / Mac
source .venv/bin/activate    
# o en Windows:
.venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

## ▶️ Uso

```bash
# Ejecutar el bot
python main.py
```

El bot realizará automáticamente los siguientes pasos:
1. Inicia sesión en tu cuenta de Instagram.
2. Cierra los popups iniciales.
3. Abre el perfil objetivo (actualmente configurado como `chefsteps`).
4. Sigue hasta 15 usuarios nuevos desde el modal de seguidores.

---

## 🔑 Variables de entorno

Crea un archivo llamado `.env` en la raíz del proyecto con el siguiente formato:

```
USERNAME="tu_usuario_instagram"
PASSWORD="tu_contraseña_instagram"
```

---

## 🧠 Detalles técnicos

- Lenguaje: **Python 3.12+**
- Librerías:
  - `selenium`
  - `python-dotenv`
  - `time`, `random`
- Principales clases y métodos:
  - `InstFollower` → clase principal del bot.
  - `login()` → inicia sesión.
  - `skip_popups()` → maneja popups post-login.
  - `find_followers()` → abre el modal de seguidores.
  - `follow()` → sigue a nuevos usuarios.

---

## 👨‍💻 Autor

**Joaquín Albano**  
Estudiante de programación y entusiasta de la automatización con Python.  
📧 Contacto: [jalbano1998@gmail.com]

---

## 📄 Licencia

**MIT License**  
Este proyecto puede ser usado, modificado y distribuido libremente con atribución al autor original.

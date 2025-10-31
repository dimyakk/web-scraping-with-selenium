# 🐍 TwitterBot – Medidor de Velocidad de Internet y Publicador en X (Twitter)

Bot automatizado en Python que mide la velocidad de descarga y subida de tu conexión a internet, y publica los resultados en X (Twitter) utilizando la API de Tweepy.

---

## 🚀 Funcionalidades
- Realiza pruebas de velocidad de internet en tiempo real usando **Selenium**.
- Se autentica y publica los resultados automáticamente en **X (Twitter)**.
- Almacena las credenciales de la API de forma segura usando **dotenv**.
- Diseñado para una fácil automatización y programación (scheduler).

---

## 🧩 Estructura del Proyecto
```
TwitterBot/
├── main.py
├── .env
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Instalación

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/dimyakk/TwitterBot.git
cd TwitterBot
```

### 2️⃣ Crear y activar un entorno virtual
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto con tus credenciales de la API de Twitter:

```
X_API_KEY=tu_api_key
X_API_KEY_SECRET=tu_api_secret
X_ACCESS_TOKEN=tu_access_token
X_ACCESS_TOKEN_SECRET=tu_token_secret
```

---

## ▶️ Uso

Ejecutar el bot manualmente:
```bash
python main.py
```

O programarlo con **Windows Task Scheduler** o **Cron** para publicar automáticamente.

---

## 🧠 Tecnologías Utilizadas
- Python 3.12
- Selenium
- Tweepy
- python-dotenv

---

## 📄 Licencia
Este proyecto es de código abierto y está disponible bajo la licencia **MIT**.

---

## 👤 Autor
**Joaquin Dimyakk**
GitHub: [@dimyakk](https://github.com/dimyakk)

# 🐍 TwitterBot – Internet Speed Checker & X (Twitter) Poster

Automated Python bot that measures your internet download/upload speed and posts the result to **X (Twitter)** using the Tweepy API.

---

## 🚀 Features
- Performs real-time internet speed tests using **Selenium**.
- Authenticates and posts updates automatically on **X (Twitter)**.
- Stores API credentials securely using **dotenv**.
- Designed for easy automation and scheduling.

---

## 🧩 Project Structure
```
TwitterBot/
├── main.py
├── .env
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/dimyakk/TwitterBot.git
   cd TwitterBot
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root with your Twitter API credentials:
   ```
   X_API_KEY=your_api_key
   X_API_KEY_SECRET=your_api_secret
   X_ACCESS_TOKEN=your_access_token
   X_ACCESS_TOKEN_SECRET=your_token_secret
   ```

---

## ▶️ Usage

Run the bot manually:
```bash
python main.py
```

Or schedule it with Windows Task Scheduler / Cron for automatic posting.

---

## 🧠 Technologies Used
- **Python 3.12**
- **Selenium**
- **Tweepy**
- **python-dotenv**

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).

---

## 👤 Author
**Joaquin Dimyakk**  
GitHub: [@dimyakk](https://github.com/dimyakk)

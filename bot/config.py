import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://api-remittances.puentecubano360.com",
)

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError(
        "No se encontró TELEGRAM_BOT_TOKEN en el archivo .env"
    )
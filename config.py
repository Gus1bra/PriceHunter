import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_PATH = os.getenv("DB_PATH", "price_hunter.db")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
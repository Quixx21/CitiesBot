import os

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

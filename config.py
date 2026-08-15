import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
if not BOT_TOKEN and os.getenv("RENDER") is None:
    print("Warning: BOT_TOKEN is not set.")

PORT = int(os.getenv("PORT", 8000))
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").rstrip("/")
MAX_IMAGES = int(os.getenv("MAX_IMAGES", 12))
MIN_IMAGES = int(os.getenv("MIN_IMAGES", 2))
SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", 1800))  # 30 minutes in seconds

BASE_DIR = Path(__file__).resolve().parent
TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

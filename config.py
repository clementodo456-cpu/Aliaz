import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MAX_IMAGES = int(os.getenv("MAX_IMAGES", 12))
MIN_IMAGES = int(os.getenv("MIN_IMAGES", 2))
SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", 1800))  # 30 minutes in seconds

BASE_DIR = Path(__file__).resolve().parent
TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

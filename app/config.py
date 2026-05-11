import os
from dotenv import load_dotenv

load_dotenv()

# Database
DB_PATH = os.getenv("DB_PATH", "data/offers.db")

# OTOMOTO
OTOMOTO_BASE_URL = "https://www.otomoto.pl/osobowe/bmw/e46/"
OTOMOTO_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
}

# Region: Dolny Śląsk = ID 10
REGION_ID = 10
REGION_NAME = "Dolny Śląsk"

# Model
MODEL = "E46"
BRAND = "BMW"

# Discord
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

# Scraping
SCRAPE_INTERVAL_SECONDS = int(os.getenv("SCRAPE_INTERVAL_SECONDS", "300"))  # 5 minutes
REQUEST_TIMEOUT = 10

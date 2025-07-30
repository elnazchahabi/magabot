# config.py
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
ADMINS = [int(x) for x in os.getenv("ADMINS", "").split(",") if x]

# megabot/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str = "your-key-here"
    # سایر تنظیمات

settings = Settings()

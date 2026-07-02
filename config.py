import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    DEFAULT_MAX_PAGES = int(os.getenv("DEFAULT_MAX_PAGES", "5"))


settings = Settings()
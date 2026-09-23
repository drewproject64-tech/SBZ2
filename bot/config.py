import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/sbz2.db").strip()

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is required.")

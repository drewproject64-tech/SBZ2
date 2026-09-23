# SB24GZ - Live

A simple Telegram-native discovery bot with exactly three core functions:

1. Live Channels
2. Search
3. Featured

## Local setup

1. Copy .env.example to .env.
2. Set BOT_TOKEN.
3. Install dependencies with pip install -r requirements.txt.
4. Start with python -m bot.main.

The bot stores its directory in SQLite and does not require an external website for its core functionality.

## Production

Deploy the included Dockerfile on Render as a worker and set BOT_TOKEN as a secret environment variable.

No gambling, casino, betting, odds, deposit, withdrawal, or gambling-promotion functionality is included in this project.

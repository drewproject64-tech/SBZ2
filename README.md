# TextMate Telegram Bot

TextMate is a self-contained Telegram text utility bot. Its tools perform the advertised actions directly inside the Telegram chat.

## Core functions

1. Count Text — counts characters, words and lines.
2. Clean Text — removes repeated spaces and blank lines.
3. Change Case — converts text to uppercase, lowercase or title case.

No external website, landing page, redirect, channel directory, gambling feature, payment flow, or third-party destination is required for the core user experience.

## Local setup

1. Copy .env.example to .env.
2. Set BOT_TOKEN.
3. Install dependencies:
   pip install -r requirements.txt
4. Start:
   python -m bot.main

## Render

Deploy as a Docker worker and set BOT_TOKEN as a secret environment variable.

## Ad destination alignment

The bot destination directly provides the text tools described in the advertising copy. Users can open the bot and immediately use Count Text, Clean Text, and Change Case without being sent to another landing page.

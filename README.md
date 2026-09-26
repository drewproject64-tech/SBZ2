# SB24GZ Text Bot

SB24GZ Text Bot is a self-contained Telegram text utility bot. It provides simple text tools directly inside Telegram.

## Core functions

1. Count Text — counts characters, words and lines.
2. Clean Text — removes repeated spaces and blank lines.
3. Change Case — converts text to uppercase, lowercase or title case.

## Bot identity

**Bot name:** SB24GZ Text Bot

**About:**
Simple text tools for counting, cleaning, and changing text case.

**Description:**
SB24GZ Text Bot provides three practical text tools directly in Telegram: count words and characters, clean extra spaces and blank lines, and change text between uppercase, lowercase, and title case.

## Local setup

1. Copy .env.example to .env.
2. Set BOT_TOKEN.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Start:
   `python -m bot.main`

## Render

Deploy as a Docker worker and set BOT_TOKEN as a secret environment variable.

## Destination alignment

The bot performs all advertised text functions directly inside Telegram. No external website, landing page, redirect, payment flow, or third-party destination is required.

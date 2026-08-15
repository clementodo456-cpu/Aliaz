# 📸 Photo Collage Creator Telegram Bot

A Telegram bot (`@aliazsteelbot`) built with Python 3.11+, Pillow, and `python-telegram-bot` configured for Render Background Worker deployment.

## Features
- Upload 2 to 12 images.
- Multiple collage layouts (Grid 2x2, Grid 3x3, 1 Large + 2 Small, Strips, Auto).
- Color background customization (white, black, gray, custom HEX).
- Custom border spacing and image fitting modes (crop, fit, stretch).
- Operates via Telegram Long Polling inside a continuous Background Worker container.

## Local Execution
1. Install dependencies: `pip install -r requirements.txt`
2. Create `.env` file with `BOT_TOKEN`
3. Run: `python bot.py`

## Deploy to Render (Background Worker)
1. Push repository to GitHub.
2. Create a **Background Worker** service on Render.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python bot.py`
5. Add Environment Variable: `BOT_TOKEN`

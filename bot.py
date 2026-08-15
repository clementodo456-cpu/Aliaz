import os
import sys
import logging
import asyncio
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Route
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from config import BOT_TOKEN, PORT, WEBHOOK_URL
from handlers.start import start_command
from handlers.help import help_command, about_command, settings_command, cancel_command
from handlers.collage import handle_photo_upload
from handlers.callbacks import handle_callback_query, handle_text_input

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Telegram Application
application = Application.builder().token(BOT_TOKEN).build()

# Register Handlers
application.add_handler(CommandHandler("start", start_command))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("about", about_command))
application.add_handler(CommandHandler("settings", settings_command))
application.add_handler(CommandHandler("cancel", cancel_command))
application.add_handler(CommandHandler("create", start_command))

application.add_handler(MessageHandler(filters.PHOTO, handle_photo_upload))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))
application.add_handler(CallbackQueryHandler(handle_callback_query))

# Starlette HTTP Webserver Endpoints
async def health_check(request):
    return PlainTextResponse("OK", status_code=200)

async def telegram_webhook(request):
    try:
        data = await request.json()
        update = Update.de_json(data, application.bot)
        await application.update_queue.put(update)
        return Response(status_code=200)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return Response(status_code=500)

async def on_startup():
    await application.initialize()
    await application.start()
    if WEBHOOK_URL:
        webhook_endpoint = f"{WEBHOOK_URL}/webhook"
        logger.info(f"Setting Telegram Webhook to {webhook_endpoint}")
        await application.bot.set_webhook(url=webhook_endpoint)

async def on_shutdown():
    logger.info("Stopping Application...")
    await application.stop()
    await application.shutdown()

starlette_app = Starlette(
    routes=[
        Route("/health", health_check, methods=["GET"]),
        Route("/webhook", telegram_webhook, methods=["POST"]),
    ],
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
)

if __name__ == "__main__":
    if WEBHOOK_URL:
        import uvicorn
        uvicorn.run(starlette_app, host="0.0.0.0", port=PORT)
    else:
        logger.info("Starting local polling engine...")
        application.run_polling()

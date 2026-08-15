import logging
import sys
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from config import BOT_TOKEN
from handlers.start import start_command
from handlers.help import help_command, about_command, settings_command, cancel_command
from handlers.collage import handle_photo_upload
from handlers.callbacks import handle_callback_query, handle_text_input

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    if not BOT_TOKEN:
        logger.critical("BOT_TOKEN environment variable is missing. Exiting.")
        sys.exit(1)

    logger.info("Initializing Photo Collage Bot for Render Background Worker...")
    
    # Initialize Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("cancel", cancel_command))
    application.add_handler(CommandHandler("create", start_command))

    # Message & Callback Handlers
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo_upload))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # Run Long Polling Loop
    logger.info("Starting long polling engine...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

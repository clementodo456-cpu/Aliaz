from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import get_main_menu_keyboard

HELP_TEXT = (
    "📖 *How to Use Photo Collage Creator*\n\n"
    "1️⃣ Tap *Create Collage* or send /create.\n"
    "2️⃣ Upload 2 to 12 photos (one-by-one or as an album).\n"
    "3️⃣ Tap *Choose Layout* and select your preferred style.\n"
    "4️⃣ Select background colors, spacing, and image fit mode.\n"
    "5️⃣ Download your finished collage JPEG!\n\n"
    "Commands:\n"
    "/start - Restart bot\n"
    "/create - Start a new collage\n"
    "/help - Instructions\n"
    "/settings - Adjust defaults\n"
    "/cancel - Reset active session\n"
    "/about - About this bot"
)

ABOUT_TEXT = (
    "🤖 *About Photo Collage Creator*\n\n"
    "Created for @aliazsteelbot.\n"
    "Powered by Python 3.11+, Pillow & python-telegram-bot.\n"
    "Deploys effortlessly on Render Web Services."
)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_TEXT, parse_mode="Markdown")

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(ABOUT_TEXT, parse_mode="Markdown")

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("⚙️ Use inline buttons during collage creation to tweak styles.", reply_markup=get_main_menu_keyboard())

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    from services.session_manager import session_manager
    session_manager.delete_session(user_id)
    await update.message.reply_text("🗑️ Active collage session cleared.", reply_markup=get_main_menu_keyboard())

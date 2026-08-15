from telegram import Update
from telegram.ext import ContextTypes
from services.session_manager import session_manager
from utils.keyboards import get_main_menu_keyboard

WELCOME_TEXT = (
    "📸 *Photo Collage Creator*\n\n"
    "Create beautiful photo collages directly in Telegram. Upload your photos, "
    "choose a layout, customize your background and borders, and download your collage instantly."
)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    session = session_manager.get_session(user_id)
    session.clear_photos()
    session.state = "IDLE"

    if update.message:
        await update.message.reply_text(WELCOME_TEXT, parse_mode="Markdown", reply_markup=get_main_menu_keyboard())

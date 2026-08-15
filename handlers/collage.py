import uuid
import logging
from telegram import Update
from telegram.ext import ContextTypes
from config import TEMP_DIR, MAX_IMAGES, MIN_IMAGES
from services.session_manager import session_manager
from utils.keyboards import get_upload_menu_keyboard

logger = logging.getLogger(__name__)

async def handle_photo_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    session = session_manager.get_session(user_id)

    if session.state != "AWAITING_PHOTOS" and len(session.photos) == 0:
        session.state = "AWAITING_PHOTOS"

    if len(session.photos) >= MAX_IMAGES:
        await update.message.reply_text(
            f"⚠️ Maximum limit reached ({MAX_IMAGES} photos). Tap *Choose Layout* to proceed.",
            parse_mode="Markdown",
            reply_markup=get_upload_menu_keyboard(len(session.photos))
        )
        return

    photo_file = await update.message.photo[-1].get_file()
    file_path = TEMP_DIR / f"user_{user_id}_{uuid.uuid4().hex[:8]}.jpg"

    try:
        await photo_file.download_to_drive(custom_path=file_path)
        count = session_manager.add_photo(user_id, str(file_path))

        await update.message.reply_text(
            f"📥 Photo received! Total: *{count}/{MAX_IMAGES}* photos.\n"
            f"{'✅ Minimum photos reached. You can add more or create your collage!' if count >= MIN_IMAGES else f'Send at least {MIN_IMAGES - count} more photo(s).'}",
            parse_mode="Markdown",
            reply_markup=get_upload_menu_keyboard(count)
        )
    except Exception as e:
        logger.error(f"Error downloading user photo: {e}")
        await update.message.reply_text("⚠️ Couldn't process that image. Please send a valid photo and try again.")

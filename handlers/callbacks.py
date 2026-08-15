import os
import uuid
import logging
from telegram import Update
from telegram.ext import ContextTypes
from config import MIN_IMAGES, TEMP_DIR
from services.session_manager import session_manager
from services.collage_engine import create_collage
from utils.validators import validate_hex_color, parse_spacing
from utils.keyboards import (
    get_main_menu_keyboard,
    get_upload_menu_keyboard,
    get_layout_keyboard,
    get_bg_keyboard,
    get_spacing_keyboard,
    get_fit_keyboard,
    get_finish_keyboard
)

logger = logging.getLogger(__name__)

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id
    session = session_manager.get_session(user_id)

    if data == "action_create":
        session.clear_photos()
        session.state = "AWAITING_PHOTOS"
        await query.edit_message_text(
            "📥 Please send your photos (2 to 12 images). You can send them one-by-one or as a group.",
            reply_markup=get_upload_menu_keyboard(0)
        )

    elif data == "action_how_it_works":
        await query.edit_message_text(
            "ℹ️ *How It Works*\n\n1. Send 2-12 photos.\n2. Choose layout & customization.\n3. Receive your high-resolution collage JPEG!",
            parse_mode="Markdown",
            reply_markup=get_main_menu_keyboard()
        )

    elif data == "action_settings":
        await query.edit_message_text("⚙️ Settings are configured during collage creation.", reply_markup=get_main_menu_keyboard())

    elif data == "action_add_more":
        session.state = "AWAITING_PHOTOS"
        await query.message.reply_text("📸 Send more photos now!")

    elif data == "action_choose_layout":
        if len(session.photos) < MIN_IMAGES:
            await query.message.reply_text(f"⚠️ Please upload at least {MIN_IMAGES} photos first!")
            return
        await query.edit_message_text("🎨 Choose a layout configuration:", reply_markup=get_layout_keyboard())

    elif data.startswith("layout_"):
        layout_choice = data.replace("layout_", "")
        session.layout = layout_choice
        await query.edit_message_text("🎨 Choose background color:", reply_markup=get_bg_keyboard())

    elif data.startswith("bg_"):
        choice = data.replace("bg_", "")
        if choice == "custom":
            session.state = "AWAITING_HEX"
            await query.edit_message_text("✏️ Please send a valid HEX color code (e.g. `#FF5733` or `#000000`):")
            return
        session.bg_color = validate_hex_color(choice) or "#FFFFFF"
        await query.edit_message_text("📐 Select border spacing:", reply_markup=get_spacing_keyboard())

    elif data.startswith("spacing_"):
        spacing_choice = data.replace("spacing_", "")
        session.spacing = parse_spacing(spacing_choice)
        await query.edit_message_text("🖼️ Choose image fit mode:", reply_markup=get_fit_keyboard())

    elif data.startswith("fit_"):
        fit_choice = data.replace("fit_", "")
        session.fit_mode = fit_choice
        
        # Trigger generation
        await execute_collage_generation(query, user_id)

    elif data == "action_cancel":
        session_manager.delete_session(user_id)
        await query.edit_message_text("🗑️ Session cancelled and temp files deleted.", reply_markup=get_main_menu_keyboard())

async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    session = session_manager.get_session(user_id)
    text = update.message.text.strip()

    if session.state == "AWAITING_HEX":
        hex_val = validate_hex_color(text)
        if not hex_val:
            await update.message.reply_text("⚠️ Invalid HEX color code. Please send a format like `#FFFFFF` or `#000000`:")
            return
        session.bg_color = hex_val
        session.state = "IDLE"
        await update.message.reply_text("📐 Select border spacing:", reply_markup=get_spacing_keyboard())

async def execute_collage_generation(query, user_id: int) -> None:
    session = session_manager.get_session(user_id)
    out_file = TEMP_DIR / f"collage_{user_id}_{uuid.uuid4().hex[:8]}.jpg"

    try:
        await query.edit_message_text("📥 Downloading your photos...")
        await query.message.reply_text("🎨 Creating your collage...")
        
        output_path = create_collage(
            photo_paths=session.photos,
            layout_name=session.layout,
            bg_color=session.bg_color,
            spacing=session.spacing,
            fit_mode=session.fit_mode,
            corner_radius=session.corner_radius,
            title=session.title,
            output_path=str(out_file)
        )

        await query.message.reply_text("✨ Almost done...")
        
        with open(output_path, "rb") as photo:
            await query.message.reply_photo(
                photo=photo,
                caption="✅ Your collage is ready!",
                reply_markup=get_finish_keyboard()
            )
    except Exception as e:
        logger.error(f"Error during collage generation: {e}")
        await query.message.reply_text("⚠️ An error occurred while generating your collage. Please try again.")
    finally:
        if os.path.exists(out_file):
            os.remove(out_file)

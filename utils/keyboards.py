from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🖼️ Create Collage", callback_data="action_create")],
        [InlineKeyboardButton("ℹ️ How It Works", callback_data="action_how_it_works"),
         InlineKeyboardButton("⚙️ Settings", callback_data="action_settings")],
        [InlineKeyboardButton("🗑️ Cancel", callback_data="action_cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_upload_menu_keyboard(photo_count: int) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("➕ Add More", callback_data="action_add_more"),
         InlineKeyboardButton("🎨 Choose Layout", callback_data="action_choose_layout")],
        [InlineKeyboardButton("🗑️ Clear Photos / Cancel", callback_data="action_cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_layout_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🔲 Grid 2×2", callback_data="layout_grid_2x2"),
         InlineKeyboardButton("🔲 Grid 3×3", callback_data="layout_grid_3x3")],
        [InlineKeyboardButton("🖼️ 1 Large + 2 Small", callback_data="layout_1l_2s"),
         InlineKeyboardButton("🖼️ 1 Large + 3 Small", callback_data="layout_1l_3s")],
        [InlineKeyboardButton("🖼️ 2×2 + Featured", callback_data="layout_2x2_featured")],
        [InlineKeyboardButton("📐 Vertical Strip", callback_data="layout_vertical"),
         InlineKeyboardButton("📐 Horizontal Strip", callback_data="layout_horizontal")],
        [InlineKeyboardButton("🎨 Auto Layout", callback_data="layout_auto")],
        [InlineKeyboardButton("🗑️ Cancel", callback_data="action_cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_bg_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("⚪ White", callback_data="bg_white"),
         InlineKeyboardButton("⚫ Black", callback_data="bg_black")],
        [InlineKeyboardButton("🌫️ Light Gray", callback_data="bg_light_gray"),
         InlineKeyboardButton("🎨 Custom HEX", callback_data="bg_custom")],
        [InlineKeyboardButton("🗑️ Cancel", callback_data="action_cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_spacing_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("None (0px)", callback_data="spacing_none"),
         InlineKeyboardButton("Small (10px)", callback_data="spacing_small")],
        [InlineKeyboardButton("Medium (20px)", callback_data="spacing_medium"),
         InlineKeyboardButton("Large (35px)", callback_data="spacing_large")],
        [InlineKeyboardButton("🗑️ Cancel", callback_data="action_cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_fit_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("✂️ Crop (Fill)", callback_data="fit_crop"),
         InlineKeyboardButton("🔍 Fit (Contain)", callback_data="fit_fit")],
        [InlineKeyboardButton("↔️ Stretch", callback_data="fit_stretch")],
        [InlineKeyboardButton("🗑️ Cancel", callback_data="action_cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_finish_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🔄 Create Another", callback_data="action_create"),
         InlineKeyboardButton("🎨 Change Layout", callback_data="action_choose_layout")],
        [InlineKeyboardButton("🗑️ Delete Session", callback_data="action_cancel")]
    ]
    return InlineKeyboardMarkup(keyboard)

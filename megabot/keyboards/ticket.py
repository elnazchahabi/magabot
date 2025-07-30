from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def ticket_admin_buttons(ticket_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 پاسخ دادن", callback_data=f"reply_{ticket_id}")],
    ])

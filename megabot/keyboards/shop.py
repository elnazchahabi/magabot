from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def product_buttons(products):
    buttons = [
        [InlineKeyboardButton(text=product.title, callback_data=f"buy_{product.id}")]
        for product in products
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

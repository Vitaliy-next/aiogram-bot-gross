from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def shop_reply_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛒 Покупай маски")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

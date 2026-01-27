from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def products_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎥 Переглянути відео",
                    callback_data="products_video"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="brands"
                )
            ]
        ]
    )

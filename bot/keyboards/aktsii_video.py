from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def aktsii_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎥 Переглянути відео",
                    callback_data="aktsii_video"
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

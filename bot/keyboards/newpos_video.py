from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def newpos_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎥 Переглянути відео",
                    callback_data="newpos_video"
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

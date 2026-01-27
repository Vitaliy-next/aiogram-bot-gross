from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def changeprise_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎥 Переглянути відео",
                    callback_data="changeprise_video"
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

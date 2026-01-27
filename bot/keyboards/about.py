from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def about_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📺 відео про компанію",
                    callback_data="about_video"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="back_to_start"
                )
            ]
        ]
    )

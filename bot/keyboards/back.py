from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def back_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="back_to_start"
                )
            ]
        ]
    )

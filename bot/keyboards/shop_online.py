from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def shop_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад до новінок, акцій та ін.",
                    callback_data="back_to_brands"
                )
            ]
        ]
    )

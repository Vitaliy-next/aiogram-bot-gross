from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def brand_back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="brands"
                )
            ]
        ]
    )

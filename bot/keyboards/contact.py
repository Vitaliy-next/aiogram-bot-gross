from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def contact_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✉️ Telegram",
                    url="https://t.me/Vitaliygross12"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📸 Наш сайт",
                    url="https://www.gross.ua"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📢 Наш канал",
                    url="https://t.me/gross_santechnika"
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

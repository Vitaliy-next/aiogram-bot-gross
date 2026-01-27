from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def cart_actions_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Додати ще товари",
                    callback_data="add_more"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💳 Оплатити",
                    callback_data="pay"
                ),
                InlineKeyboardButton(
                    text="⏳ Резерв 24h",
                    callback_data="reserve"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Скасувати",
                    callback_data="cancel"
                )
            ]
        ]
    )

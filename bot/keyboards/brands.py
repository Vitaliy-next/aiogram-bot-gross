from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def brands_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Новінки", callback_data="new_pos"),
                InlineKeyboardButton(text="Акції та пропозиції", callback_data="Aktsii"),
            ],
            [
                InlineKeyboardButton(text="Прихід товару", callback_data="prihod"),
                InlineKeyboardButton(text="Зміни цін", callback_data="change_prise"),
            ],
            [
                InlineKeyboardButton(text="Важливі події", callback_data="podii"),
                InlineKeyboardButton(text="Ассортимент ", callback_data="products"),
            ],

            [
                InlineKeyboardButton(text="Купуй online тут", callback_data="shop")
            ],


            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="back_to_start"
                )
            ],
        ]
    )

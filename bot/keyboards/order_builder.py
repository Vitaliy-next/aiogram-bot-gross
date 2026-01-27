from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def products_keyboard(products):
    builder = InlineKeyboardBuilder()

    for product in products:
        builder.button(
            text=product.product_name,
            callback_data=f"add:{product.product_id}"
        )

    builder.adjust(1)
    return builder.as_markup()
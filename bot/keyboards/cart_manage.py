from aiogram.utils.keyboard import InlineKeyboardBuilder

def cart_manage_keyboard(cart_products):
    builder = InlineKeyboardBuilder()

    for p in cart_products:
        builder.button(
            text=f"➖ {p.product_name}",
            callback_data=f"dec:{p.product_id}"
        )
        builder.button(
            text=f"➕ {p.product_name}",
            callback_data=f"inc:{p.product_id}"
        )

    builder.adjust(2)
    return builder.as_markup()

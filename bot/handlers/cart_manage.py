from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy import select

from bot.database import async_session
from bot.models import Cart, CartProduct, Product

router = Router()


@router.callback_query(lambda c: c.data.startswith("inc:"))
async def increase_product(callback: CallbackQuery):
    await change_quantity(callback, delta=1)


@router.callback_query(lambda c: c.data.startswith("dec:"))
async def decrease_product(callback: CallbackQuery):
    await change_quantity(callback, delta=-1)


async def change_quantity(callback: CallbackQuery, delta: int):
    tg_id = callback.from_user.id
    product_id = int(callback.data.split(":")[1])

    async with async_session() as session:
        cart = (await session.execute(
            select(Cart).where(Cart.tg_id == tg_id)
        )).scalar_one_or_none()

        if not cart:
            await callback.answer("❌ Кошик не знайдено", show_alert=True)
            return

        product = await session.get(Product, product_id)
        cart_product = (await session.execute(
            select(CartProduct).where(
                CartProduct.cart_id == cart.cart_id,
                CartProduct.product_id == product_id
            )
        )).scalar_one_or_none()

        if not cart_product:
            await callback.answer("❌ Товар не знайдено", show_alert=True)
            return

        # ➕
        if delta > 0:
            cart_product.quantity += 1
            cart_product.final_price += product.price
            cart.total_products += 1
            cart.total_price += product.price

        # ➖
        else:
            cart_product.quantity -= 1
            cart_product.final_price -= product.price
            cart.total_products -= 1
            cart.total_price -= product.price

            if cart_product.quantity <= 0:
                await session.delete(cart_product)

        await session.commit()

    await callback.answer("✅ Кошик оновлено")

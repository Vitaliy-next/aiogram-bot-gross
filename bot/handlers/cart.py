from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy import select

from bot.database import async_session
from bot.models import Cart, CartProduct, Product

from bot.keyboards.cart_manage import cart_manage_keyboard

#from bot.keyboards.cart_actions import cart_actions_menu




router = Router()


@router.callback_query(lambda c: c.data.startswith("add:"))
async def add_to_cart(callback: CallbackQuery):
    tg_id = callback.from_user.id
    product_id = int(callback.data.split(":")[1])

    async with async_session() as session:
        # 1️⃣ корзина
        result = await session.execute(
            select(Cart).where(Cart.tg_id == tg_id)
        )
        cart = result.scalar_one_or_none()

        if not cart:
            cart = Cart(
                tg_id=tg_id,
                total_price=0,
                total_products=0
            )
            session.add(cart)
            await session.flush()  # ⚠️ чтобы получить cart_id

        # 2️⃣ товар
        product = await session.get(Product, product_id)
        if not product:
            await callback.answer("❌ Товар не знайдено", show_alert=True)
            return

        # 3️⃣ товар в корзине?
        result = await session.execute(
            select(CartProduct).where(
                CartProduct.cart_id == cart.cart_id,
                CartProduct.product_id == product_id
            )
        )
        cart_product = result.scalar_one_or_none()

        if cart_product:
            cart_product.quantity += 1
            cart_product.final_price += product.price
        else:
            cart_product = CartProduct(
                cart_id=cart.cart_id,
                product_id=product.product_id,
                product_name=product.product_name,
                quantity=1,
                final_price=product.price
            )
            session.add(cart_product)

        # 4️⃣ пересчёт корзины
        cart.total_products += 1
        cart.total_price += product.price

        await session.commit()

        

    await callback.answer("✅ Додано в кошик")



# from aiogram import Router
# from aiogram.types import Message
# from aiogram.filters import Command
# from sqlalchemy import select

# from bot.database import async_session
# from bot.models import Cart, CartProduct

# from bot.keyboards.cart_manage import cart_manage_keyboard
# from bot.keyboards.cart_actions import cart_actions_menu

# router = Router()

# #🧩 ХЕНДЛЕР /cart (СЮДА ТВОЙ БЛОК)

# @router.message(Command("cart"))
# async def show_cart(message: Message):
#     tg_id = message.from_user.id

#     async with async_session() as session:
#         cart = await session.scalar(
#             select(Cart).where(Cart.tg_id == tg_id)
#         )

#         if not cart:
#             await message.answer("🛒 Кошик порожній")
#             return

#         result = await session.execute(
#             select(CartProduct).where(
#                 CartProduct.cart_id == cart.cart_id
#             )
#         )
#         products = result.scalars().all()

#     if not products:
#         await message.answer("🛒 Кошик порожній")
#         return

#     # 🧾 ТЕКСТ
#     text = "🛒 Ваш кошик:\n\n"
#     for p in products:
#         text += f"• {p.product_name} × {p.quantity} = {float(p.final_price)} грн\n"

#     text += f"\n💰 Разом: {float(cart.total_price)} грн"

#     # ⬇️ ВОТ СЮДА
#     await message.answer(
#         text,
#         reply_markup=cart_manage_keyboard(products)
#     )
#     await message.answer(
#         "Оберіть дію:",
#         reply_markup=cart_actions_menu()
#     )




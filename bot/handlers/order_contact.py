# from aiogram import Router
# from aiogram.types import Message
# from aiogram.fsm.context import FSMContext
# from sqlalchemy import select

# from bot.database import async_session
# from bot.models import Order
# from bot.handlers.order_states import OrderContactFSM

# router = Router()


# @router.message(OrderContactFSM.waiting_contact_phone)
# async def save_contact_phone(message: Message, state: FSMContext):
#     contact_phone = message.text.strip()

#     if not contact_phone.isdigit() or len(contact_phone) < 10:
#         await message.answer("❌ Введіть коректний номер телефону")
#         return

#     data = await state.get_data()
#     order_id = data["order_id"]

#     async with async_session() as session:
#         order = await session.scalar(
#             select(Order).where(Order.order_id == order_id)
#         )

#         if not order:
#             await message.answer("❌ Замовлення не знайдено")
#             await state.clear()
#             return

#         order.contact_phone = contact_phone
#         await session.commit()

#     await state.clear()

#     await message.answer(
#         "✅ Контактний номер збережено!\n"
#         "Наш менеджер зв’яжеться з вами 📲"
#     )



from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from bot.database import async_session
from bot.models import Order
from bot.handlers.order_states import OrderContactFSM

router = Router()

@router.message(OrderContactFSM.waiting_contact_phone)
async def process_contact_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    data = await state.get_data()
    order_id = data["order_id"]

    async with async_session() as session:
        order = await session.scalar(
            select(Order).where(Order.order_id == order_id)
        )

        if not order:
            await message.answer("❌ Замовлення не знайдено")
            return

        order.contact_phone = phone
        await session.commit()

    payment_link = "https://pay.pb.ua/ВАША_ПОСТОЯННАЯ_ССЫЛКА"

    await message.answer(
        f"✅ Контакт збережено\n\n"
        f"🧾 Замовлення №{order_id}\n"
        f"💰 Сума: {order.total_price} грн\n\n"
        f"💳 Для оплати перейдіть за посиланням:\n"
        f"{payment_link}\n\n"
        f"📌 У призначенні платежу укажіть:\n"
        f"Оплата за замовлення №{order_id}\n"
        f"Телефон: {phone}"
    )

    await state.clear()


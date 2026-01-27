
from aiogram import Router
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(lambda c: c.data == "add_more")
async def add_more_products(callback: CallbackQuery):
    await callback.message.answer(
        "🛒 Оберіть товар для додавання:",
    )
    # 👉 просто вызываем /order
    await callback.message.answer("/order")
    await callback.answer()


from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery):
    await callback.message.answer(
        "Привет! 👋\n\n"
        "Я — официальный бот Annacos Beauty.\n"
        "Здесь вы можете ознакомиться с брендами\n"
        "и связаться с нами для подбора ухода 💎",
        reply_markup=start_menu()
    )
    await callback.answer()

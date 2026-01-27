from aiogram import Router
from aiogram.types import CallbackQuery

from bot.keyboards.contact import contact_menu

router = Router()


@router.callback_query(lambda c: c.data == "contact")
async def contact_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        "💬 <b>Связаться с нами</b>\n\n"
        "Выберите удобный способ связи:",
        reply_markup=contact_menu()
    )
    await callback.answer()


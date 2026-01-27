from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from sqlalchemy import select

from bot.models import AnnaCos
from bot.database import async_session
from bot.handlers.clients_states import ClientsAccess
from bot.config import CLIENTS_PASSWORD

router = Router()




# ───────────────────────────────
#          /clients
# ───────────────────────────────
@router.message(Command("clients"))
async def clients_entry(message: Message, state: FSMContext):
    await message.answer("🔐 Введите пароль:")
    await state.set_state(ClientsAccess.waiting_password)


# ───────────────────────────────
#       Проверка пароля
# ───────────────────────────────
@router.message(ClientsAccess.waiting_password)
async def check_clients_password(message: Message, state: FSMContext):
    if message.text != CLIENTS_PASSWORD:
        await message.answer("❌ Неверный пароль.")
        await state.clear()
        return

    async with async_session() as session:
        result = await session.execute(select(AnnaCos))
        rows = result.scalars().all()

    if not rows:
        await message.answer("Таблица annacostest пустая.")
        await state.clear()
        return

    text = "📋 <b>Клиенты:</b>\n\n"
    for r in rows:
        text += (
            f"🆔 client_id: {r.client_id}\n"
            f"👤 Имя: {r.client_name}\n"
            f"📞 Телефон: {r.phone}\n"
            "──────────────\n"
        )

    await message.answer(text)
    await state.clear()


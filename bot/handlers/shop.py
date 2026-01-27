from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text

router = Router()

# этот handler сейчвс отключен работает через shop_online

@router.message(Text("🛒 Покупай маски"))
async def buy_masks(message: Message):
    await message.answer(
        "🛍 В наличии:\n"
        "1️⃣ Маска Atache — 3300 грн\n"
        "2️⃣ Маска Utsukusy — 5950 грн\n\n"
        "Скоро здесь будет корзина 😉"
    )

from aiogram import Router, F
from aiogram.types import Message

router = Router()

PASSWORD = ""

# простое хранилище доступа (на время жизни бота, но у меня работает через admin_router, а не через этот код)
authorized_users: set[int] = set()


@router.message(F.text == PASSWORD)
async def password_handler(message: Message):
    authorized_users.add(message.from_user.id)
    await message.answer("✅ Пароль вірний. Можеш надсилати фото або відео.")


@router.message(F.video | F.photo)
async def catch_media(message: Message):
    if message.from_user.id not in authorized_users:
        await message.answer("🔐 Введіть пароль для доступу")
        return

    if message.video:
        await message.answer(
            f"🎥 VIDEO file_id:\n<code>{message.video.file_id}</code>",
            parse_mode="HTML"
        )

    elif message.photo:
        await message.answer(
            f"🖼 PHOTO file_id:\n<code>{message.photo[-1].file_id}</code>",
            parse_mode="HTML"
        )







# from aiogram import Router, F
# from aiogram.types import Message

# router = Router()

# @router.message(F.video | F.photo)
# async def catch_media(message: Message):
#     if message.video:
#         await message.answer(
#             f"🎥 VIDEO file_id:\n<code>{message.video.file_id}</code>",
#             parse_mode="HTML"
#         )

#     elif message.photo:
#         await message.answer(
#             f"🖼 PHOTO file_id:\n<code>{message.photo[-1].file_id}</code>",
#             parse_mode="HTML"
#         )


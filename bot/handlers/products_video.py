from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy import select

from bot.database import async_session
from bot.models import Media

router = Router()   # 🔥 ВАЖНО




@router.callback_query(lambda c: c.data == "products_video") # обработка при нажатие на кнопку срабатыв это handler
async def show_products_video(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(Media).where(Media.code == "gross_collectors_video_3")
        )
        media = result.scalar_one_or_none()

    if not media:
        await callback.answer(
            "❌ Вибачте,відео асортименту ще у розробці",
            show_alert=True
        )
        return

    if media.media_type == "video":
        await callback.message.answer_video(
            media.file_id
        )
    elif media.media_type == "photo":
        await callback.message.answer_photo(
            media.file_id
        )

    await callback.answer()



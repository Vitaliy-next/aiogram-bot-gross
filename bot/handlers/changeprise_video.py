from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy import select

from bot.database import async_session
from bot.models import Media

router = Router()   # 🔥 ВАЖНО





@router.callback_query(lambda c: c.data == "changeprise_video") # обработка при нажатие на кнопку просмотреть видео в меню зміна цін 
async def show_changeprise_video(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(Media).where(Media.code == "gross_collectors_video_6")  
        )
        media = result.scalar_one_or_none()

    if not media:
        await callback.answer(
            "❌ Вибачаємось, але відео немає!",
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

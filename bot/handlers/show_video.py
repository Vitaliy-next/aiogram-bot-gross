
#from bot.keyboards.brands_detail import brand_back_menu
#from bot.keyboards.shop_online import shop_menu
from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy import select

from bot.database import async_session
from bot.models import Media

router = Router()   # 🔥 ВАЖНО




@router.callback_query(lambda c: c.data == "podii_video")
async def show_podii_video(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(Media).where(Media.code == "gross_collectors_video_1")
        )
        media = result.scalar_one_or_none()

    if not media:
        await callback.answer(
            "❌ Вибачте,відео подій  у розробці",
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

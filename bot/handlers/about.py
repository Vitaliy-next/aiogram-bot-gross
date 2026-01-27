from aiogram import Router
from aiogram.types import CallbackQuery

from bot.keyboards.about import about_menu

router = Router()


@router.callback_query(lambda c: c.data == "about")
async def about_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        text=(
            "ℹ️ <b>Про нас</b>\n\n"
            "GROSS — простір сучасної сантехніки 💎\n"  
            "Оптові рішення для бізнесу, якій довіряють.\n\n"
            "Тут — тільки актуальні новинки 💎\n" 
            "спеціальні пропозиції та найкращі умови співпраці"
            "👇  Відео про компанію GROSS"
            
            
        ),
        reply_markup=about_menu()
    )
    await callback.answer()
# ===== КНОПКА "ВИДЕО" =====
@router.callback_query(lambda c: c.data == "about_video")
async def about_video_handler(callback: CallbackQuery):
    await callback.message.answer_video(
        video="https://t.me/gross_santechnika/148"
    )
    await callback.answer()




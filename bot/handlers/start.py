from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    CallbackQuery
)
from aiogram.filters import Command
from sqlalchemy import text

from bot.database import async_session

router = Router()

# ───────────────────────────────
#        INLINE МЕНЮ (ОСНОВНОЕ)
# ───────────────────────────────
def start_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧴 Новинки,акції,продукція", callback_data="brands")],
            [InlineKeyboardButton(text="💬 Зв'язатися с нами", callback_data="contact")],
            [InlineKeyboardButton(text="ℹ️ Про компанію GROSS", callback_data="about")],
        ]
    )

# ───────────────────────────────
#    INLINE: ВОЙТИ БЕЗ РЕГИСТРАЦИИ
# ───────────────────────────────
def guest_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="➡️ Увійти без регістрации",
                callback_data="guest_login"
            )]
        ]
    )

# ───────────────────────────────
#      REPLY: ТОЛЬКО КОНТАКТ
# ───────────────────────────────
contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Поділитися контактом", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# ───────────────────────────────
#              /start
# ───────────────────────────────
@router.message(Command("start"))
async def start_cmd(message: Message):
     #print("🔥 START TRIGGERED", message.text)
    chat_id = message.chat.id
    name = message.from_user.first_name or "Telegram user"

    async with async_session() as session:
        result = await session.execute(
            text("SELECT client_id FROM annacostest WHERE tg_id = :tg"),
            {"tg": chat_id}
        )
        client = result.fetchone()

        # ❗ НОВЫЙ КЛИЕНТ
        if not client:
            await message.answer(
                "👋 Вітаю в інформаційном каналі компанії GROSS!\n\n"
                "Щоб продовжити, будь ласка, поділиться номером телефону 💎",
                reply_markup=contact_kb
            )

            await message.answer(
                "Також ви можете войти без регістрації:",
                reply_markup=guest_menu()
            )
            return

    # ✅ ЗАРЕГИСТРИРОВАННЫЙ КЛИЕНТ
    await message.answer(
        "Вітаю тебе друже! 👋\n\n"
        "Я — офіційний бот філії компаніі GROSS в м.Дніпро .\n"
        "Обирай швидко розділ для перегляду 💎",
        reply_markup=start_menu()
    )

# ───────────────────────────────
#      ОБРАБОТКА КОНТАКТА
# ───────────────────────────────
@router.message(F.contact)
async def contact_handler(message: Message):
    chat_id = message.chat.id
    phone = message.contact.phone_number
    name = message.from_user.first_name or "Telegram user"

    async with async_session() as session:
        await session.execute(
            text("""
                INSERT INTO annacostest (
                    tg_id,
                    client_name,
                    phone,
                    city,
                    products,
                    summ_sale,
                    activity,
                    additional_info,
                    period
                )
                VALUES (
                    :tg,
                    :name,
                    :phone,
                    NULL,
                    NULL,
                    0,
                    'new',
                    'Добавлен через Telegram',
                    NULL
                )
            """),
            {
                "tg": chat_id,
                "name": name,
                "phone": phone
            }
        )
        await session.commit()

    await message.answer(
        "✅ Дякую! Ви успішно зареєстровані 💎",
        reply_markup=ReplyKeyboardRemove()
    )

    await message.answer(
        "Оберіть розділ:",
        reply_markup=start_menu()
    )

# ───────────────────────────────
#      ГОСТЕВОЙ ВХОД (INLINE)
# ───────────────────────────────
@router.callback_query(F.data == "guest_login")
async def guest_login(callback: CallbackQuery):
    chat_id = callback.from_user.id
    name = callback.from_user.first_name or "Telegram user"

    # сохраняем гостя
    try:
        async with async_session() as session:
            await session.execute(
                text("""
                    INSERT INTO chat_id (tg_id, name)
                    VALUES (:tg, :name)
                    ON CONFLICT (tg_id) DO NOTHING
                """),
                {"tg": chat_id, "name": name}
            )
            await session.commit()
    except Exception as e:
        print("❌ DB ERROR (guest_login):", e)

    await callback.message.edit_text(
        "Ви зайшли без регістрації 👀\n\n"
        "Ви можете знайомитися з інформацію про новінки нашої компанії,\n"
        "Отримувати повідомлення .",
        reply_markup=start_menu()
    )

@router.callback_query(lambda c: c.data == "back_to_start")
async def back_to_start(callback: CallbackQuery):
    await callback.message.edit_text(
        "Вітаю! 👋\n\n"
        "Я — офіційний інформаційний бот філії м. Дніпро компанії GROSS .\n"
        "Можете ознакомиться з брендами та новінками нашої продукції\n"
        "та зв'язатися з нами для замовлення 💎",
        reply_markup=start_menu()
    )
    await callback.answer()

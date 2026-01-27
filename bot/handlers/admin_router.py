from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from sqlalchemy import text

from bot.database import async_session
from bot.handlers.admin_states import AdminLogin, AdminSQL, AdminMessage, GetPhone,InformState,StockState,PriseState,PodiiState,ProductState,NewproductState,CodeState
from bot.config import ADMIN_PASSWORD,PASSWORD,INFORM_PASSWORD,STOCK_PASSWORD,PRISE_PASSWORD,PODII_PASSWORD,PRODUCT_PASSWORD,NEWPRODUCT_PASSWORD,CODE_PASSWORD
from bot.models import InfoBlock
from bot.models import StockBlock
from bot.models import PriseBlock
from bot.models import PodiiBlock
from bot.models import ProductBlock
from bot.models import NewproductBlock

from sqlalchemy import select

router = Router()




ADMIN_IDS: set[int] = set()

# ───────────────────────────────
#           /admin
# ───────────────────────────────
@router.message(Command("admin"))
async def admin_entry(message: Message, state: FSMContext):
    await message.answer("🔐 Введите пароль администратора:")
    await state.set_state(AdminLogin.waiting_password)


@router.message(AdminLogin.waiting_password)
async def process_admin_password(message: Message, state: FSMContext):
    if message.text == ADMIN_PASSWORD:
        ADMIN_IDS.add(message.from_user.id)
        await message.answer("✅ Пароль верный.\nВведите SQL SELECT-запрос:")
        await state.set_state(AdminSQL.waiting_query)
    else:
        await message.answer("❌ Неверный пароль.")
        await state.clear()


# ───────────────────────────────
#        SQL SELECT
# ───────────────────────────────
@router.message(AdminSQL.waiting_query)
async def admin_sql_query(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return await message.answer("⛔ Нет доступа.")

    sql = message.text.strip().lower()

    # ❗ защита
    if not sql.startswith("select"):
        return await message.answer("❌ Разрешены только SELECT-запросы.")

    try:
        async with async_session() as session:
            result = await session.execute(text(message.text))
            rows = result.mappings().all()

        tg_ids = [r["tg_id"] for r in rows if r.get("tg_id")]

        await state.update_data(tg_ids=tg_ids)
        await message.answer(
            f"👥 Клиентов найдено: {len(tg_ids)}\n"
            f"Теперь отправьте текст сообщения."
        )
        await state.set_state(AdminMessage.waiting_text)

    except Exception as e:
        await message.answer(f"❌ SQL ошибка:\n{e}")


# ───────────────────────────────
#        Текст
# ───────────────────────────────
@router.message(AdminMessage.waiting_text)
async def send_notifications(message: Message, state: FSMContext):
    bot = message.bot
    data = await state.get_data()
    tg_ids = data.get("tg_ids", [])

    for chat_id in tg_ids:
        try:
            await bot.send_message(chat_id, message.text)
        except:
            pass

    await message.answer("📨 Текст отправлен.\nТеперь отправьте фото или видео.")
    await state.set_state(AdminMessage.waiting_media)


# ───────────────────────────────
#        Медиа
# ───────────────────────────────
@router.message(AdminMessage.waiting_media, F.photo | F.video)
async def send_media(message: Message, state: FSMContext):
    bot = message.bot
    data = await state.get_data()
    tg_ids = data.get("tg_ids", [])

    file_id = (
        message.photo[-1].file_id
        if message.photo
        else message.video.file_id
    )

    for chat_id in tg_ids:
        try:
            if message.photo:
                await bot.send_photo(chat_id, file_id)
            else:
                await bot.send_video(chat_id, file_id)
        except:
            pass

    await message.answer("✅ Медиа отправлено.")
    await state.clear()


# ───────────────────────────────
#      Получение телефона
# ───────────────────────────────
phone_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📱 Отправить телефон", request_contact=True)]],
    resize_keyboard=True
)

@router.message(Command("phone"))
async def request_phone(message: Message, state: FSMContext):
    await message.answer("Отправьте телефон:", reply_markup=phone_kb)
    await state.set_state(GetPhone.waiting_for_phone)




@router.message(GetPhone.waiting_for_phone)
async def phone_handler(message: Message, state: FSMContext):
    phone = message.contact.phone_number if message.contact else message.text
    chat_id = message.chat.id
    client_name = message.from_user.first_name or "Telegram user"

    async with async_session() as session:
        # 1️⃣ проверяем, есть ли такой телефон
        result = await session.execute(
            text("SELECT client_id FROM annacostest WHERE phone = :phone"),
            {"phone": phone}
        )
        client = result.fetchone()

        if client:
            # 2️⃣ если есть — обновляем tg_id
            await session.execute(
                text("""
                    UPDATE annacostest
                    SET tg_id = :tg
                    WHERE phone = :phone
                """),
                {
                    "tg": chat_id,
                    "phone": phone
                }
            )

            await message.answer("✅ Телефон привязан к существующему клиенту.")

        else:
            # 3️⃣ если нет — создаём нового клиента
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
                    "name": client_name,
                    "phone": phone
                }
            )

            await message.answer(
                "✅ Вы зарегистрированы!\n"
                "Мы сохранили ваш контакт 💎"
            )

        await session.commit()

    await state.clear()



 # блок для ввода видео в новинки И НЕ ТОЛЬКО С ЭТИМ БЛОКОМ КОНФЛИКТОВ НЕТ
 # простое хранилище доступа (на время жизни бота) очень важно
authorized_users: set[int] = set()
 # первый блок для ввода video в новинки

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
# # Немного хотел изменить верхний блок с добавлением видео через команду 
# #✅  исправление (БЕЗ FSM) ХОТЕЛ НО ВЫШЕЛ КОНФЛИКТ HANDLERS ПОЭТОМУ ОСТАВИЛ ВЫШЕ КАК БЫЛО 



# блок для редактирования информации прямо через бота, c этого блока заношу пароли в верт

#INFORM_PASSWORD = " "



@router.message(Command("inform"))
async def inform_start(message: Message, state: FSMContext):
    await state.set_state(InformState.password)
    await message.answer("🔐 Введіть пароль")

# проверка пароля

@router.message(InformState.password)
async def inform_password(message: Message, state: FSMContext):
    if message.text != INFORM_PASSWORD:
        await state.clear()
        await message.answer("❌ Невірний пароль")
        return

    await state.set_state(InformState.text)
    await message.answer("✍️ Введіть текст для блоку «Акції»")





# ВОТ ЭТОТ БЛОК — СЮДА





@router.message(InformState.text)
async def inform_save(message: Message, state: FSMContext):
    async with async_session() as session:
        result = await session.execute(
            select(InfoBlock).where(InfoBlock.code == "Aktsii")
        )
        block = result.scalar_one_or_none()

        if block:
            block.text = message.text
        else:
            block = InfoBlock(code="Aktsii", text=message.text)
            session.add(block)

        await session.commit()

    await state.clear()
    await message.answer("✅ Інформацію оновлено")


# блок для редактирования информации прямо через бота для кнопки прихід товару

#STOCK_PASSWORD = "  "



@router.message(Command("stock"))
async def stock_start(message: Message, state: FSMContext):
    await state.set_state(StockState.password)
    await message.answer("🔐 Введіть пароль")

# проверка пароля

@router.message(StockState.password)
async def stock_password(message: Message, state: FSMContext):
    if message.text != STOCK_PASSWORD:
        await state.clear()
        await message.answer("❌ Невірний пароль")
        return

    await state.set_state(StockState.text)
    await message.answer("✍️ Введіть текст для блоку «Прихід товару»")





# ВОТ ЭТОТ БЛОК — СЮДА раобраться еще )))))





@router.message(StockState.text)
async def stock_save(message: Message, state: FSMContext):
    async with async_session() as session:
        result = await session.execute(
            select(StockBlock).where(StockBlock.code == "Prihod")
        )
        block = result.scalar_one_or_none()

        if block:
            block.text = message.text
        else:
            block = StockBlock(code="Prihod", text=message.text)
            session.add(block)

        await session.commit()

    await state.clear()
    await message.answer("✅ Інформацію оновлено")




# блок для редактирования меню зміни цін  прямо через бота

#PRISE_PASSWORD = " "



@router.message(Command("prise"))
async def prise_start(message: Message, state: FSMContext):
    await state.set_state(PriseState.password)
    await message.answer("🔐 Введіть пароль")

# проверка пароля

@router.message(PriseState.password)
async def prise_password(message: Message, state: FSMContext):
    if message.text != PRISE_PASSWORD:
        await state.clear()
        await message.answer("❌ Невірний пароль")
        return

    await state.set_state(PriseState.text)
    await message.answer("✍️ Введіть текст для блоку «Зміни цін»")





# ВОТ ЭТОТ БЛОК — СЮДА





@router.message(PriseState.text)
async def prise_save(message: Message, state: FSMContext):
    async with async_session() as session:
        result = await session.execute(
            select(PriseBlock).where(PriseBlock.code == "Prise")
        )
        block = result.scalar_one_or_none()

        if block:
            block.text = message.text
        else:
            block = PriseBlock(code="Prise", text=message.text)
            session.add(block)

        await session.commit()

    await state.clear()
    await message.answer("✅ Інформацію оновлено")



# блок для редактирования меню подіі прямо через бота

#PODII_PASSWORD = " "



@router.message(Command("podii"))
async def prodii_start(message: Message, state: FSMContext):
    await state.set_state(PodiiState.password)
    await message.answer("🔐 Введіть пароль")

# проверка пароля

@router.message(PodiiState.password)
async def podii_password(message: Message, state: FSMContext):
    if message.text != PODII_PASSWORD:
        await state.clear()
        await message.answer("❌ Невірний пароль")
        return

    await state.set_state(PodiiState.text)
    await message.answer("✍️ Введіть текст для блоку «Подіі»")


# ВОТ ЭТОТ БЛОК — СЮДА состояние проверяет обновлене информации


@router.message(PodiiState.text)
async def podii_save(message: Message, state: FSMContext):
    async with async_session() as session:
        result = await session.execute(
            select(PodiiBlock).where(PodiiBlock.code == "Podii")
        )
        block = result.scalar_one_or_none()

        if block:
            block.text = message.text
        else:
            block = PodiiBlock(code="Podii", text=message.text)
            session.add(block)

        await session.commit()

    await state.clear()
    await message.answer("✅ Інформацію оновлено")



# блок для редактирования меню ассортимент прямо через бота

#PRODUCT_PASSWORD = "  "



@router.message(Command("prod"))
async def prod_start(message: Message, state: FSMContext):
    await state.set_state(ProductState.password)
    await message.answer("🔐 Введіть пароль")

# проверка пароля

@router.message(ProductState.password)
async def prod_password(message: Message, state: FSMContext):
    if message.text != PRODUCT_PASSWORD:
        await state.clear()
        await message.answer("❌ Невірний пароль")
        return

    await state.set_state(ProductState.text)
    await message.answer("✍️ Введіть текст для блоку «Ассортимент»")


# ВОТ ЭТОТ БЛОК — СЮДА состояние проверяет обновлене информации


@router.message(ProductState.text)
async def prod_save(message: Message, state: FSMContext):
    async with async_session() as session:
        result = await session.execute(
            select(ProductBlock).where(ProductBlock.code == "Products")
        )
        block = result.scalar_one_or_none()

        if block:
            block.text = message.text
        else:
            block = ProductBlock(code="Products", text=message.text)
            session.add(block)

        await session.commit()

    await state.clear()
    await message.answer("✅ Інформацію оновлено")



# блок для редактирования меню новинок прямо через бота

#NEWPRODUCT_PASSWORD = ""



@router.message(Command("newprod"))
async def newprod_start(message: Message, state: FSMContext):
    await state.set_state(NewproductState.password)
    await message.answer("🔐 Введіть пароль")

# проверка пароля

@router.message(NewproductState.password)
async def newprod_password(message: Message, state: FSMContext):
    if message.text != NEWPRODUCT_PASSWORD:
        await state.clear()
        await message.answer("❌ Невірний пароль")
        return

    await state.set_state(NewproductState.text)
    await message.answer("✍️ Введіть текст для блоку «Новінки»")


# ВОТ ЭТОТ БЛОК — СЮДА состояние проверяет обновлене информации


@router.message(NewproductState.text)
async def newprod_save(message: Message, state: FSMContext):
    async with async_session() as session:
        result = await session.execute(
            select(NewproductBlock).where(NewproductBlock.code == "Newproducts")
        )
        block = result.scalar_one_or_none()

        if block:
            block.text = message.text
        else:
            block = NewproductBlock(code="Newproducts", text=message.text) # изменил code
            session.add(block)                                          

        await session.commit()

    await state.clear()
    await message.answer("✅ Інформацію оновлено")


#2️⃣ admin_router.py — безопасная версия /code

#CODE_PASSWORD = " "


@router.message(Command("code"))
async def code_start(message: Message, state: FSMContext):
    await state.set_state(CodeState.password)
    await message.answer("🔐 Введіть пароль")

#🔑 Проверка пароля
@router.message(CodeState.password)
async def code_password(message: Message, state: FSMContext):
    if message.text != CODE_PASSWORD:
        await state.clear()
        await message.answer("❌ Невірний пароль")
        return

    await state.set_state(CodeState.sql)
    await message.answer(
        "✍️ Вставте SQL-запит\n\n"
        "✅ Дозволено:\n"
        "• INSERT INTO media\n"
        "• UPDATE media"
    )

#🧠 Выполнение SQL (ТОЛЬКО media)
@router.message(CodeState.sql)
async def code_execute_sql(message: Message, state: FSMContext):
    sql = message.text.strip()
    sql_l = sql.lower()

    # жёсткая проверка
    allowed = (
        sql_l.startswith("insert into media")
        or sql_l.startswith("update media")
    )

    if not allowed:
        await message.answer(
            "❌ Заборонено\n\n"
            "Дозволено тільки:\n"
            "INSERT INTO media\n"
            "UPDATE media"
        )
        return

    try:
        async with async_session() as session:
            await session.execute(text(sql))
            await session.commit()

        await message.answer("✅ Дані в media оновлено")

    except Exception as e:
        await message.answer(
            f"❌ Помилка SQL:\n<code>{e}</code>",
            parse_mode="HTML"
        )

    await state.clear()






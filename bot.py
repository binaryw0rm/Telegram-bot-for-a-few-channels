import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
MANAGER_IDS_RAW = os.getenv("MANAGER_IDS", "")

if not API_TOKEN or not MANAGER_IDS_RAW:
    print("ОШИБКА: Проверь .env — BOT_TOKEN и MANAGER_IDS должны быть заполнены!")
    exit(1)

try:
    MANAGER_IDS = [int(uid.strip()) for uid in MANAGER_IDS_RAW.split(",") if uid.strip()]
except ValueError:
    print("ОШИБКА: MANAGER_IDS содержит не числа!")
    exit(1)

print(f"Бот запущен. Менеджеры: {MANAGER_IDS}")

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Клавиатура
menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Оставить заявку")],
    [KeyboardButton(text="Связаться с менеджером")]
], resize_keyboard=True)

# Словарь: откуда пришёл пользователь (user_id → название отдела)
user_department = {}

# Deep linking: определяем отдел при старте
@dp.message(CommandStart(deep_link=True))
async def start_deep(message: types.Message):
    args = message.text.split()
    if len(args) > 1:
        payload = args[1]
        dept_map = {
            "sales": "Отдел продаж",
            "projects": "Отдел проектов",
            "service": "Отдел сервиса",
        }
        dept = dept_map.get(payload, "нашем канале")
    else:
        dept = "нашем канале"

    # ЗАПОМИНАЕМ ОТДЕЛ ДЛЯ ЭТОГО ПОЛЬЗОВАТЕЛЯ
    user_department[message.from_user.id] = dept

    await message.answer(
        f"Здравствуйте!\n\n"
        f"Вы пришли из канала <b>«{dept}»</b>\n\n"
        f"Чем помочь?",
        reply_markup=menu
    )

@dp.message(CommandStart())
async def start_simple(message: types.Message):
    await message.answer("Здравствуйте!\n\nЧем могу помочь?", reply_markup=menu)

@dp.message(F.text == "Оставить заявку")
async def leave_request(message: types.Message):
    user_department[message.from_user.id] = user_department.get(message.from_user.id, "Неизвестный канал")
    waiting_for_request.add(message.from_user.id)
    await message.answer("Напишите, что вам нужно + контакт (телефон/Telegram).\n\nСвяжемся в течение 15–30 минут")

@dp.message(F.text == "Связаться с менеджером")
async def live_chat(message: types.Message):
    dept = user_department.get(message.from_user.id, "Личка")
    text = (
        f"Запрос живого общения\n\n"
        f"Отдел: <b>{dept}</b>\n"
        f"От: {message.from_user.first_name} (@{message.from_user.username or 'нет'})\n"
        f"ID: {message.from_user.id}"
    )
    for mgr in MANAGER_IDS:
        await safe_send(mgr, text)
    await message.answer("Менеджер уже в пути!")

# Множество пользователей, которые сейчас пишут заявку
waiting_for_request = set()

async def safe_send(user_id: int, text: str):
    try:
        await bot.send_message(user_id, text, disable_web_page_preview=True)
    except Exception as e:
        print(f"Не удалось отправить {user_id}: {e}")

@dp.message()
async def handle_text(message: types.Message):
    if message.from_user.id not in waiting_for_request:
        await message.answer("Выберите действие:", reply_markup=menu)
        return

    # БЕРЁМ СОХРАНЁННЫЙ ОТДЕЛ ИЗ ПАМЯТИ
    dept = user_department.get(message.from_user.id, "Неизвестный канал")

    text_for_managers = (
        f"Новая заявка из <b>{dept}</b>\n\n"
        f"От: {message.from_user.first_name} "
        f"(@{message.from_user.username or 'нет username'})\n"
        f"ID: {message.from_user.id}\n\n"
        f"{message.text}"
    )

    for mgr in MANAGER_IDS:
        await safe_send(mgr, text_for_managers)

    await message.answer("Спасибо! Заявка принята, скоро свяжемся")
    waiting_for_request.discard(message.from_user.id)

async def main():
    print("Бот запущен и работает 24/7")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
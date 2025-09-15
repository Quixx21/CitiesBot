from aiogram import Dispatcher, types
from aiogram.filters import Command

from settings.config import *
from handlers import city, game, information, stats
from keyboards.keyboards import main_menu
from settings.logger import *

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

if ADMIN_CHAT_ID:
    tgh = TelegramLogHandler(bot, ADMIN_CHAT_ID, level=logging.WARNING)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    tgh.setFormatter(formatter)
    logger.addHandler(tgh)


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    text = """
👋 Привет! Я бот для игры в <b>«Города»</b> 🌍

🎮 Ты можешь:
- Играть 1 на 1 против другого игрока
- Проверять города по первой букве
- Смотреть свою статистику (победы, поражения, рекорды)

📌 Как играть:
1. Нажми кнопку <b>«Играть в города»</b>.
2. Я подберу соперника.
3. Ходите по очереди: называйте города, каждый следующий на последнюю букву предыдущего.
4. У тебя есть 60 секунд ⏳, иначе соперник победит.

Нажми кнопку в меню, чтобы начать!
"""
    user = message.from_user
    logger.info(f"User {user.id} ({user.username}) started bot")
    await message.answer(text, parse_mode="HTML", reply_markup=main_menu)


dp.include_router(city.router)
dp.include_router(game.router)
dp.include_router(stats.router)
dp.include_router(information.router)


async def main():
    logger.info("Starting bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

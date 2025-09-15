from aiogram import F, Router, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from services.game_manager import get_state, reset_state
from services.stats_manager import get_user_stats

router = Router()


@router.message(F.text == "📊 Статистика")
async def stats_handler(message: types.Message):
    user_id = message.from_user.id
    stats = get_user_stats(user_id)

    text = (
        f"📊 Твоя статистика:\n"
        f"🏆 Побед: {stats['wins']}\n"
        f"💀 Поражений: {stats['losses']}\n"
        f"📈 Макс. городов за игру: {stats['max_cities']}\n\n"
        f"Хочешь получить JSON-файл со своей статистикой?"
    )

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📥 Да, отправь JSON")],
            [KeyboardButton(text="↩️ Назад в меню")],
        ],
        resize_keyboard=True,
    )

    await message.answer(text, reply_markup=keyboard)


@router.message(lambda msg: msg.text == "📥 Да, отправь JSON")
async def send_stats_file(message: types.Message):
    user_id = message.from_user.id
    from aiogram.types import FSInputFile

    file = FSInputFile("data/stats.json")
    await message.answer_document(file, caption="📥 Вот твоя статистика в JSON")


@router.message(F.text == "↩️ Назад в меню")
async def back_to_menu(message: types.Message):
    user_id = message.from_user.id
    if get_state(user_id) == "game":
        await message.answer("🎮 Ты сейчас в игре! Дождись окончания партии ⏳")
        return
    reset_state(user_id)
    from keyboards.keyboards import main_menu

    await message.answer("🔙 Главное меню", reply_markup=main_menu)

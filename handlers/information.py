from aiogram import Router, types

router = Router()


@router.message(lambda msg: msg.text == "ℹ️ Помощь")
async def help_handler(message: types.Message):
    text = (
        "ℹ️ <b>Справка</b>\n\n"
        "🔍 <b>Найти город по букве</b> — вводишь букву, бот покажет 20 рандомных городов у которых население больше чем 200 тыс на вашу букву.\n"
        "🎮 <b>Играть в города</b> — бот подбирает соперника для игры 1 на 1. Нельзя использовать кнопку 'Найти город' во время поиска или игры\n"
        "📊 <b>Статистика</b> — смотришь свои победы/поражения. Отправка файла JSON статистики\n"
        "<b>Автор</b> @twinglxck"
    )
    await message.answer(text, parse_mode="HTML")

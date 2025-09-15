from aiogram import Router, types

from services.city_api import find_cities_by_letter

router = Router()


@router.message(lambda msg: msg.text == "🔍 Найти город по букве")
async def city_by_letter_start(message: types.Message):
    await message.answer("✍️ Введи букву, и я подберу города.")


@router.message(lambda msg: len(msg.text) == 1 and msg.text.isalpha())
async def city_by_letter_result(message: types.Message):
    letter = message.text.strip()
    cities = find_cities_by_letter(letter)

    if not cities:
        await message.answer(f"❌ Нет городов на букву {letter.upper()}")
        return

    result = "🏙 Найденные города:\n" + "\n".join(f"- {c}" for c in cities)
    await message.answer(result)

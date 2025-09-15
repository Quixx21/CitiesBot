from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔍 Найти город по букве")],
        [KeyboardButton(text="🎮 Играть в города")],
        [KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="ℹ️ Помощь")],
    ],
    resize_keyboard=True,
)
search_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Отмена поиска")]], resize_keyboard=True
)
game_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🏳️ Сдаться")]], resize_keyboard=True
)

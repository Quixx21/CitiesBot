from aiogram import F, Router, types

from keyboards.keyboards import game_menu, main_menu, search_menu
from settings.logger import *
from services.city_api import city_exists
from services.game_manager import (
    create_game,
    games,
    get_opponent,
    get_state,
    reset_state,
    set_state,
)
from services.stats_manager import update_stats

router = Router()
waiting_player = None


async def start_timer(game_id, player_id, bot):
    await asyncio.sleep(60)
    if game_id in games and games[game_id]["turn"] == player_id:
        state = games[game_id]
        opponent = get_opponent(game_id, player_id)
        await bot.send_message(player_id, "⏳ Время вышло! Ты проиграл.")
        await bot.send_message(opponent, "🏆 Соперник не ответил, ты победил!")
        cities_count_player = len(state["used"])
        update_stats(player_id, "loss", cities_count_player)
        update_stats(opponent, "win", cities_count_player)
        reset_state(player_id)
        reset_state(opponent)
        del games[game_id]


@router.message(F.text == "🎮 Играть в города")
async def find_player(message: types.Message):
    global waiting_player
    user_id = message.from_user.id
    logger.info(f"User {user_id} clicked 'Play'")
    if get_state(user_id) == "search":
        await message.answer("⏳ Ты уже ищешь соперника...")
        return
    if get_state(user_id) == "game":
        await message.answer("🎮 Ты уже в игре!")
        return

    if waiting_player is None:
        waiting_player = user_id
        set_state(user_id, "search")
        await message.answer("🔎 Ищу соперника...", reply_markup=search_menu)

    else:
        opponent = waiting_player
        waiting_player = None
        game_id = create_game(user_id, opponent)

        set_state(user_id, "game")
        set_state(opponent, "game")

        await message.answer(
            "🎮 Нашёлся соперник! Ты ходишь первым.", reply_markup=game_menu
        )
        await message.bot.send_message(
            opponent, "🎮 Нашёлся соперник! Жди хода оппонента.", reply_markup=game_menu
        )

        games[game_id]["timer"] = asyncio.create_task(
            start_timer(game_id, user_id, message.bot)
        )


@router.message(F.text == "❌ Отмена поиска")
async def cancel_search(message: types.Message):
    global waiting_player
    user_id = message.from_user.id

    if get_state(user_id) != "search":
        await message.answer("❌ Ты сейчас не ищешь соперника.", reply_markup=main_menu)
        return

    if waiting_player == user_id:
        waiting_player = None

    reset_state(user_id)
    await message.answer("↩️ Поиск отменён. Главное меню:", reply_markup=main_menu)


@router.message(F.text == "🏳️ Сдаться")
async def surrender(message: types.Message):
    user_id = message.from_user.id
    game_id = None

    for gid, state in games.items():
        if user_id in state["players"]:
            game_id = gid
            break

    if not game_id:
        await message.answer("❌ Ты не в игре.", reply_markup=main_menu)
        return

    state = games[game_id]
    opponent = get_opponent(game_id, user_id)

    await message.answer("🏳️ Ты сдался. Поражение записано.", reply_markup=main_menu)
    await message.bot.send_message(
        opponent, "🏆 Соперник сдался. Победа за тобой!", reply_markup=main_menu
    )

    cities_count = len(state["used"])
    update_stats(user_id, "loss", cities_count)
    update_stats(opponent, "win", cities_count)

    reset_state(user_id)
    reset_state(opponent)
    del games[game_id]


@router.message(F.text.regexp(r"^[А-Яа-яЁёA-Za-z\- ]+$"))
async def handle_city(message: types.Message):
    user_id = message.from_user.id
    text = message.text.strip()
    logger.info(f"User {user_id} tried city: {text}")
    # find a player
    game_id = None
    for gid, state in games.items():
        if user_id in state["players"]:
            game_id = gid
            break

    if not game_id:
        return

    state = games[game_id]

    if state["turn"] != user_id:
        await message.answer("Сейчас не твой ход!")
        return

    city = city_exists(text)
    if not city:
        await message.answer("❌ Такого города нет в базе!")
        return
    if text.lower() in state["used"]:
        await message.answer("⚠️ Этот город уже использован!")
        return
    if state["last_letter"] and not text.lower().startswith(state["last_letter"]):
        await message.answer(
            f"❌ Нужно назвать город на букву {state['last_letter'].upper()}"
        )
        return
    state["used"].add(text.lower())
    opponent = get_opponent(game_id, user_id)
    last_letter = text[-1].lower()
    while last_letter in ["ь", "ъ", "ы", "й"]:
        last_letter = text[-2].lower()
    state["last_letter"] = last_letter
    state["turn"] = opponent
    if state["timer"]:
        state["timer"].cancel()
    await message.answer(f"✅ Принято: {text}. Ход передан сопернику!")
    await message.bot.send_message(
        opponent,
        f"Противник назвал {text}. Твой ход! Назови город на букву {last_letter.upper()}",
    )
    state["timer"] = asyncio.create_task(start_timer(game_id, opponent, message.bot))

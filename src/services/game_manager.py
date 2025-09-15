import asyncio

games = {}
waiting_player = None
game_counter = 0
player_states = {}


def set_state(user_id, state):
    player_states[user_id] = state


def get_state(user_id):
    return player_states.get(user_id, "menu")


def reset_state(user_id):
    player_states[user_id] = "menu"


def create_game(player1, player2):
    global game_counter
    game_counter += 1
    game_id = game_counter
    games[game_id] = {
        "players": [player1, player2],
        "turn": player1,
        "used": set(),
        "last_letter": None,
        "timer": None,
    }
    return game_id


def get_opponent(game_id, player_id):
    p1, p2 = games[game_id]["players"]
    return p2 if player_id == p1 else p1

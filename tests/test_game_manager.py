import pytest
from services.game_manager import (
    create_game,
    get_opponent,
    set_state,
    get_state,
    reset_state,
    games,
)


def test_create_game_and_players():
    gid = create_game(101, 202)
    assert gid in games
    assert games[gid]["players"] == [101, 202]
    assert games[gid]["turn"] == 101


def test_get_opponent():
    gid = create_game(1, 2)
    assert get_opponent(gid, 1) == 2
    assert get_opponent(gid, 2) == 1


def test_states_flow():
    uid = 555
    assert get_state(uid) == "menu"
    set_state(uid, "search")
    assert get_state(uid) == "search"
    set_state(uid, "game")
    assert get_state(uid) == "game"
    reset_state(uid)
    assert get_state(uid) == "menu"

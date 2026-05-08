import random
from constants import (
    BOARD_WIDTH, BOARD_HEIGHT,
    STATUS_RUNNING, STATUS_GAMEOVER,
    SCORE_PER_FOOD,
    EVENT_NORMAL, EVENT_ATE_FOOD, EVENT_WALL_HIT, EVENT_SELF_HIT,
)
from snake import get_head, check_self_collision


def create_game_state(snake_body: list) -> dict:
    """
    Membuat game state awal yang siap dipakai game_loop().

    IS  snake_body — body ular awal; hasil dari create_snake() di snake.py
    FS  Return dict game state lengkap: score, status, grew, food
    """
    state = {
        'score': 0,
        'status': STATUS_RUNNING,
        'grew': False,
        'food': None,
    }
    state['food'] = generate_food(snake_body)
    return state


def generate_food(snake_body: list) -> tuple:
    """
    Mencari posisi food secara brute-force yang tidak menimpa body ular.

    IS  snake_body — posisi body ular saat ini
    FS  Return tuple (x, y) posisi food yang aman
    """
    while True:
        x = random.randint(0, BOARD_WIDTH - 1)
        y = random.randint(0, BOARD_HEIGHT - 1)
        candidate = (x, y)
        is_safe = True
        for segment in snake_body:
            if candidate == segment:
                is_safe = False
                break
        if is_safe:
            return candidate


def update_state(state: dict, snake_body: list) -> str:
    """
    Memperbarui game state berdasarkan posisi ular saat ini.

    IS  state      — game state saat ini (diupdate in-place)
        snake_body — body ular setelah move_snake(); dari game_loop()
    FS  Return string event: EVENT_NORMAL / EVENT_ATE_FOOD /
                             EVENT_WALL_HIT / EVENT_SELF_HIT
    """
    head = get_head(snake_body)

    # Cek wall hit: kepala di luar batas board
    hx, hy = head
    if hx < 0 or hx >= BOARD_WIDTH or hy < 0 or hy >= BOARD_HEIGHT:
        state['status'] = STATUS_GAMEOVER
        state['grew'] = False
        return EVENT_WALL_HIT

    # Cek self hit: kepala menabrak badan sendiri
    if check_self_collision(snake_body):
        state['status'] = STATUS_GAMEOVER
        state['grew'] = False
        return EVENT_SELF_HIT

    # Cek food: kepala berada di posisi food
    if head == state['food']:
        state['score'] += SCORE_PER_FOOD
        state['grew'] = True
        state['food'] = generate_food(snake_body)
        return EVENT_ATE_FOOD

    # Default: tidak ada kejadian khusus
    state['grew'] = False
    return EVENT_NORMAL


def is_game_over(state: dict) -> bool:
    """
    Mengecek apakah game sudah berakhir.

    IS  state — game state saat ini
    FS  Return True jika status == STATUS_GAMEOVER, False jika masih berjalan
    """
    return state['status'] == STATUS_GAMEOVER

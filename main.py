import curses
import time
import sys

from constants import (
    BOARD_WIDTH, BOARD_HEIGHT,
    RIGHT, TICK_RATE,
    STATUS_RUNNING, STATUS_PAUSED, STATUS_GAMEOVER,
    EVENT_NORMAL, EVENT_ATE_FOOD, EVENT_WALL_HIT, EVENT_SELF_HIT,
    KEY_QUIT, KEY_PAUSE
)
from snake   import create_snake, move_snake, get_head, get_length
from board   import create_game_state, update_state, is_game_over
from display import init_display, render, get_input
from storage import save_score, load_top_scores, format_leaderboard


# BAGIAN 1 - Menu utama
def get_username():
    """
    Minta input nama user dari terminal.
    Validasi: tidak boleh kosong, tidak lebih dari 15 karakter.

    Return:
        str: nama user yang valid
    """
    while True:
        name = input("Masukkan nama kamu: ").strip()
        if len(name) == 0:
            print("  Nama tidak boleh kosong.")
        elif len(name) > 15:
            print("  Nama terlalu panjang (maks 15 karakter).")
        elif ',' in name:
            print("  Nama tidak boleh mengandung koma.")
        else:
            return name


def show_main_menu():
    """
    Tampilkan menu utama di terminal dan minta pilihan.

    Return:
        str: '1' (Classic), '2' (Leaderboard), '3' (Keluar)
             atau tambahkan '4' untuk Battle Mode nanti
    """
    print("\n" + "=" * 35)
    print("         SNAKE GAME")
    print("=" * 35)
    print("  1. Main (Classic Mode)")
    print("  2. Lihat Leaderboard")
    print("  3. Keluar")
    print("=" * 35)

    valid_choices = ['1', '2', '3']
    while True:
        choice = input("Pilihan: ").strip()
        if choice in valid_choices:
            return choice
        print("  Pilihan tidak valid. Coba lagi.")


def show_leaderboard_screen(mode="classic"):
    """
    Tampilkan leaderboard di terminal (bukan curses).
    """
    print("\n" + "=" * 45)
    print(f"  LEADERBOARD - {mode.upper()}")
    print("=" * 45)

    scores = load_top_scores(n=10, mode=mode)
    lines  = format_leaderboard(scores)
    for line in lines:
        print(line)

    print("=" * 45)
    input("\nTekan Enter untuk kembali ke menu...")


# BAGIAN 2 - Game loop (berjalan di dalam curses)
def game_loop(stdscr, username):
    """
    Loop utama game Classic Mode.
    Dipanggil oleh curses.wrapper() sehingga berjalan di mode curses.

    Parameter:
        stdscr   : objek screen dari curses (otomatis dari wrapper)
        username : str - nama pemain

    Alur satu tick:
        1. Baca input -> dapat direction baru
        2. Gerakkan ular (move_snake)
        3. Update state (cek food, wall, collision)
        4. Render ke layar
        5. Tunggu TICK_RATE detik
        6. Ulangi sampai game over atau user quit
    """
    # --- Setup awal ---
    init_display(stdscr)

    start_x = BOARD_WIDTH  // 2
    start_y = BOARD_HEIGHT // 2
    body     = create_snake(start_x, start_y)
    state    = create_game_state(body)
    direction = RIGHT
    running   = True

    # --- Main loop ---
    while running:

        # 1: Baca input keyboard
        new_direction = get_input(stdscr, direction)

        # Cek kalau user quit (get_input return None)
        if new_direction is None:
            running = False
            break

        direction = new_direction

        # 2: Gerakkan ular
        # grew dari state menentukan apakah ular bertambah panjang
        body = move_snake(body, direction, grew=state['grew'])

        # 3: Update state (cek collision, makan food, dll)
        event = update_state(state, body)

        # 4: Render frame
        render(stdscr, body, state)

        # 5: Cek game over
        if is_game_over(state):
            # Tunggu input quit dari user
            stdscr.nodelay(False)  # switch ke blocking input
            while True:
                try:
                    key = stdscr.getkey()
                    if key in KEY_QUIT:
                        break
                except curses.error:
                    pass
            running = False
            break

        # 6: Tunggu sebelum tick berikutnya
        time.sleep(TICK_RATE)

    return state['score']

# BAGIAN 3 - Entry point
def main():
    """
    Entry point utama. Loop menu sampai user pilih keluar.
    """
    print("\nSelamat datang di Snake Game!")
    username = get_username()
    print(f"\nHalo, {username}!")

    while True:
        choice = show_main_menu()

        if choice == '1':
            # Jalankan game classic dengan curses.wrapper
            # wrapper otomatis handle init/cleanup curses
            final_score = curses.wrapper(game_loop, username)

            # Setelah selesai, tampilkan skor dan simpan
            print(f"\nGame selesai! Skor kamu: {final_score}")
            save_score(username, final_score, mode="classic")
            print("Skor tersimpan!")
            input("Tekan Enter untuk kembali ke menu...")

        elif choice == '2':
            show_leaderboard_screen(mode="classic")

        elif choice == '3':
            print("\nSampai jumpa!")
            sys.exit(0)

# Jalankan program
if __name__ == "__main__":
    main()

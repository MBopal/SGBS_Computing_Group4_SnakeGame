from constants import RIGHT


def create_snake(start_x: int, start_y: int) -> list[tuple]:
    """
    Membuat ular baru dengan panjang 3 segment, menghadap ke kanan.

    IS      start_x — kolom posisi kepala awal; dari BOARD_WIDTH // 2 di main.py
            start_y — baris posisi kepala awal; dari BOARD_HEIGHT // 2 di main.py

    FS      Return list of tuple panjang 3, ular menghadap ke kanan
    """
    body = []
    body.append((start_x,     start_y))
    body.append((start_x - 1, start_y))
    body.append((start_x - 2, start_y)) 
    return body


def move_snake(body: list, direction: tuple, grew: bool) -> list[tuple]:
    """
    Menggerakkan ular satu langkah ke arah yang diberikan.

    IS      body      — posisi ular saat ini
            direction — tuple (dx, dy) arah gerak
            grew      — True jika ular baru makan food (ekor tidak di-pop)

    FS      Return list body ular yang sudah digeser satu langkah
    """
    old_head = body[0]
    dx, dy   = direction
    new_head = (old_head[0] + dx, old_head[1] + dy)

    body.insert(0, new_head)

    if not grew:
        body.pop()

    return body


def check_self_collision(body: list) -> bool:
    """
    Mengecek apakah kepala ular menabrak badannya sendiri (Linear Search).

    IS      body — posisi ular setelah bergerak

    FS      Return True  jika kepala menabrak badan sendiri
            Return False jika posisi kepala aman
    """
    head = body[0]
    for segment in body[1:]:
        if segment == head:
            return True
    return False


def get_head(body: list) -> tuple:
    """
    Mengembalikan posisi kepala ular.

    IS      body — posisi ular saat ini

    FS      Return tuple (x, y) posisi kepala
    """
    return body[0]


def get_length(body: list) -> int:
    """
    Mengembalikan panjang ular saat ini.

    IS      body — posisi ular saat ini

    FS      Return int jumlah segment ular
    """
    return len(body)
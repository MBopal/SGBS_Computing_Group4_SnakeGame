# Ukuran Board
BOARD_WIDTH  = 30   # jumlah kolom
BOARD_HEIGHT = 20   # jumlah baris

# Arah gerak (x, y) 
UP    = ( 0, -1)
DOWN  = ( 0,  1)
LEFT  = (-1,  0)
RIGHT = ( 1,  0)

# Key mapping dari keyboard 
KEY_UP    = ['w', 'W']
KEY_DOWN  = ['s', 'S']
KEY_LEFT  = ['a', 'A']
KEY_RIGHT = ['d', 'D']
KEY_QUIT  = ['q', 'Q']
KEY_PAUSE = ['p', 'P']

# Tick rate (detik per frame)
TICK_RATE = 0.5  

# Skor
SCORE_PER_FOOD = 10

# File storage
SCORES_FILE = "scores.csv"

# Tampilan karakter 
CHAR_HEAD  = '@' # kepala ular
CHAR_BODY  = '#' # badan ular
CHAR_FOOD  = '*' # apel
CHAR_EMPTY = ' ' # ruang kosong
CHAR_WALL  = '+' # tembok

# Status game 
STATUS_RUNNING  = "RUNNING"
STATUS_PAUSED   = "PAUSED"
STATUS_GAMEOVER = "GAMEOVER"

# Event dari move_snake 
EVENT_NORMAL    = "NORMAL"    # gerak biasa
EVENT_ATE_FOOD  = "ATE_FOOD"  # kepala ketemu food
EVENT_WALL_HIT  = "WALL_HIT"  # nabrak tembok
EVENT_SELF_HIT  = "SELF_HIT"  # nabrak badan sendiri

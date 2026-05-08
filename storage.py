import csv
import os
from datetime import datetime

from constants import SCORES_FILE


# ── save_score ────────────────────────────────────────────────────────────────

def save_score(username: str, score: int, mode: str) -> None:
    """
    Simpan satu entri skor ke SCORES_FILE (scores.csv).

    IS      username — nama pemain; dari get_username() main.py
            score    — skor akhir; dari state['score'] setelah game loop selesai
            mode     — 'classic' atau 'battle'; dari game_loop() main.py

    Side effect: satu baris baru ditambahkan ke scores.csv.
                 File dibuat otomatis dengan header jika belum ada.
    """
    timestamp   = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    file_exists = os.path.exists(SCORES_FILE)

    with open(SCORES_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['username', 'score', 'mode', 'timestamp'])
        writer.writerow([username, score, mode, timestamp])


# ── load_top_scores ───────────────────────────────────────────────────────────

def load_top_scores(n: int = 10, mode: str = 'classic') -> list[dict]:
    """
    Muat n skor tertinggi untuk mode tertentu dari SCORES_FILE.

    IS      n    — jumlah maksimal entry yang dikembalikan; default 10
            mode — filter mode 'classic' atau 'battle'; dari caller main.py

    Return  list of dict, maksimal n entry, terurut dari skor tertinggi.
            Return [] jika file tidak ada atau tidak ada entry yang cocok.
    """
    if not os.path.exists(SCORES_FILE):
        return []

    scores = []
    with open(SCORES_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['mode'] == mode:
                scores.append({
                    'username' : row['username'],
                    'score'    : int(row['score']),
                    'mode'     : row['mode'],
                    'timestamp': row['timestamp'],
                })

    scores.sort(key=lambda x: x['score'], reverse=True)
    return scores[:n]


# ── find_user ─────────────────────────────────────────────────────────────────

def find_user(username: str) -> dict | None:
    """
    Cari entri skor tertinggi untuk username tertentu (Linear Search).

    IS      username — nama yang dicari; dari caller main.py

    Return  dict entry skor tertinggi untuk username tersebut.
            Return None jika username tidak ditemukan di file.
    """
    if not os.path.exists(SCORES_FILE):
        return None

    best_entry = None
    with open(SCORES_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['username'] == username:
                row['score'] = int(row['score'])
                if best_entry is None or row['score'] > best_entry['score']:
                    best_entry = row

    return best_entry


# ── format_leaderboard ────────────────────────────────────────────────────────

def format_leaderboard(scores: list[dict]) -> list[str]:
    """
    Format list of dict skor menjadi list of str siap di-print ke terminal.

    IS      scores — list of dict hasil load_top_scores(); sudah terurut descending

    Return  list of str, siap di-print baris per baris ke terminal.
    """
    lines = []
    lines.append("Rank  Name           Score     Date")
    lines.append('-' * 45)

    if not scores:
        lines.append("  (belum ada data)")
    else:
        for rank, entry in enumerate(scores, start=1):
            line = (
                f"{rank:<6}"
                f"{entry['username']:<15}"
                f"{entry['score']:<10}"
                f"{entry['timestamp']}"
            )
            lines.append(line)

    return lines

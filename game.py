import random
import threading

ROUNDS = 10
GUESS_TIME = 10

guesses = {}       # {name: guess}
points = {}        # {name: total_points}
names = {}         # {conn: name}
lock = threading.Lock()
clients = []
guess_event = threading.Event()

def broadcast(message):
    for conn in clients:
        try:
            conn.send(message.encode('utf-8'))
        except:
            pass

def add_client(conn, name):
    with lock:
        clients.append(conn)
        names[conn] = name
        points[name] = 0  # initialise by name not conn

def remove_client(conn):
    with lock:
        if conn in clients:
            clients.remove(conn)
        name = names.pop(conn, None)
        if name and name in guesses:
            del guesses[name]
        # note: don't delete from points so tally survives reconnects

def submit_guess(conn, value):
    with lock:
        name = names.get(conn)
        if name:
            guesses[name] = value
            all_guessed = len(guesses) == len(clients)

    if all_guessed:
        guess_event.set()

def calculate_points(secret):
    with lock:
        results = sorted(guesses.items(), key=lambda x: abs(x[1] - secret))

    round_summary = f"\nThe number was {secret}!\n"
    for rank, (name, guess) in enumerate(results):
        distance = abs(guess - secret)
        earned = max(0, 100 - distance * 2)
        with lock:
            points[name] += earned
        round_summary += f"  #{rank+1} {name} guessed {guess} (off by {distance}) — +{earned} pts\n"

    broadcast(round_summary)

def display_scoreboard(title="--- SCOREBOARD ---"):
    with lock:
        sorted_scores = sorted(points.items(), key=lambda x: x[1], reverse=True)

    board = f"\n{title}\n"
    for rank, (name, score) in enumerate(sorted_scores):
        board += f"  #{rank+1} {name} — {score} pts\n"
    board += "------------------\n"
    broadcast(board)

def disconnect_all():
    display_scoreboard("--- FINAL SCORES ---")
    broadcast("Game over! Disconnecting...\n")
    with lock:
        for conn in clients:
            try:
                conn.close()
            except:
                pass
        clients.clear()
        guesses.clear()
        names.clear()
        points.clear()  # wipe for next game

def play_game():
    for round_num in range(1, ROUNDS + 1):
        secret = random.randint(1, 100)
        print(f"Round {round_num}: secret is {secret}")

        with lock:
            guesses.clear()

        guess_event.clear()

        broadcast(f"\n=== ROUND {round_num}/{ROUNDS} ===\nYou have {GUESS_TIME} seconds! Guess a number between 1 and 100: ")

        guess_event.wait(timeout=GUESS_TIME)

        with lock:
            missing = [names[conn] for conn in clients if names[conn] not in guesses]

        if missing:
            broadcast(f"{', '.join(missing)} didn't guess in time — 0 pts!\n")

        calculate_points(secret)
        display_scoreboard(f"--- SCORES AFTER ROUND {round_num} ---")

def game_loop(num_players):
    while True:
        print(f"Waiting for {num_players} players...")

        while len(clients) < num_players:
            pass

        broadcast(f"All players connected! Starting {ROUNDS} rounds!\n")

        play_game()

        disconnect_all()

        print("All players disconnected. Waiting for new game...\n")
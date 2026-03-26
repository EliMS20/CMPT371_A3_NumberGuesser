import random
import threading

ROUNDS = 10
GUESS_TIME = 10

guesses = {}
lock = threading.Lock()
clients = []
guess_event = threading.Event()

def broadcast(message):
    for conn in clients:
        try:
            conn.send(message.encode('utf-8'))
        except:
            pass

def add_client(conn):
    with lock:
        clients.append(conn)

def remove_client(conn):
    with lock:
        if conn in clients:
            clients.remove(conn)
        if conn in guesses:
            del guesses[conn]

def submit_guess(conn, value):
    with lock:
        guesses[conn] = value
        all_guessed = len(guesses) == len(clients)

    if all_guessed:
        guess_event.set()

def disconnect_all():
    broadcast("Game over! Disconnecting...\n")
    with lock:
        for conn in clients:
            try:
                conn.close()
            except:
                pass
        clients.clear()
        guesses.clear()

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
            missing = [conn for conn in clients if conn not in guesses]

        if missing:
            broadcast(f"{len(missing)} player(s) didn't guess in time — they get 0 points!\n")

        broadcast(f"\nThe number was {secret}!\n")

        with lock:
            results = sorted(guesses.items(), key=lambda x: abs(x[1] - secret))

        for rank, (conn, guess) in enumerate(results):
            distance = abs(guess - secret)
            broadcast(f"  #{rank+1} guessed {guess} (off by {distance})\n")

def game_loop(num_players):
    while True:  # outer loop — keeps server alive across games
        print(f"Waiting for {num_players} players...")

        while len(clients) < num_players:
            pass

        broadcast(f"All players connected! Starting {ROUNDS} rounds!\n")

        play_game()

        disconnect_all()

        print("All players disconnected. Waiting for new game...\n")
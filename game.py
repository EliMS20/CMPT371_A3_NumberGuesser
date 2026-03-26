import random
import threading

ROUNDS = 10

guesses = {}
lock = threading.Lock()
clients = []

def broadcast(message):
    for conn in clients:
        conn.send(message.encode('utf-8'))

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

def game_loop(num_players):
    print(f"Waiting for {num_players} players...")
    while len(clients) < num_players:
        pass

    broadcast(f"All players connected! Starting {ROUNDS} rounds!\n")

    for round_num in range(1, ROUNDS + 1):
        secret = random.randint(1, 100)
        print(f"Round {round_num}: secret is {secret}")

        with lock:
            guesses.clear()

        broadcast(f"\n=== ROUND {round_num}/{ROUNDS} ===\nGuess a number between 1 and 100: ")

        while len(guesses) < len(clients):
            pass

        broadcast(f"\nThe number was {secret}!\n")

        with lock:
            results = sorted(guesses.items(), key=lambda x: abs(x[1] - secret))

        for rank, (conn, guess) in enumerate(results):
            distance = abs(guess - secret)
            broadcast(f"  #{rank+1} guessed {guess} (off by {distance})\n")

    broadcast("\nGame over! Thanks for playing!\n")
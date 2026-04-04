import random
import threading
import time

# GAME SETTINGS
# Number of rounds and time allowed per round
ROUNDS = 3
GUESS_TIME = 10

# GAME DATA
# Stores guesses, scores, and player info
guesses = {}
points = {}
names = {}

# THREAD SAFETY
# Lock for safe access to shared data
lock = threading.Lock()

# List of connected clients
clients = []

# Event to signal when all guesses are submitted
guess_event = threading.Event()

# BROADCAST FUNCTION
# Sends a message to all connected clients
def broadcast(message):
    for conn in clients:
        try:
            conn.send(message.encode('utf-8'))
        except:
            pass

# NAME CHECK
# Returns True if a username is already taken (usernames must be unique)
def is_name_taken(name):
    with lock:
        return name in names.values()

# ADD CLIENT
# Registers a new client and initializes their score
def add_client(conn, name):
    with lock:
        clients.append(conn)
        names[conn] = name
        points[name] = 0

# REMOVE CLIENT
# Removes client and cleans up their data
def remove_client(conn):
    with lock:
        if conn in clients:
            clients.remove(conn)
        name = names.pop(conn, None)
        if name and name in guesses:
            del guesses[name]

# SUBMIT GUESS
# Stores a player's guess and checks if all players have guessed
def submit_guess(conn, value):
    with lock:
        name = names.get(conn)
        if name:
            guesses[name] = value
            all_guessed = len(guesses) == len(clients)

    # If all players guessed, trigger event
    if all_guessed:
        guess_event.set()

# POINT CALCULATION
# Calculates scores based on distance from the secret number
def calculate_points(secret):
    with lock:
        # Sort guesses by closeness to the secret number
        results = sorted(guesses.items(), key=lambda x: abs(x[1] - secret))

    round_summary = f"\nThe number was {secret}!\n"

    for rank, (name, guess) in enumerate(results):
        distance = abs(guess - secret)

        # Points decrease as distance increases
        earned = max(0, 100 - distance * 2)

        with lock:
            points[name] += earned

        round_summary += f"  #{rank+1} {name} guessed {guess} (off by {distance}) — +{earned} pts\n"

    broadcast(round_summary)

# SCOREBOARD DISPLAY
# Shows players ranked by score
def display_scoreboard(title="--- SCOREBOARD ---"):
    with lock:
        sorted_scores = sorted(points.items(), key=lambda x: x[1], reverse=True)

    board = f"\n{title}\n"

    for rank, (name, score) in enumerate(sorted_scores):
        board += f"  #{rank+1} {name} — {score} pts\n"

    board += "------------------\n"
    broadcast(board)

# DISCONNECT ALL
# Ends the game and clears all data
def disconnect_all():
    # Show final scores before closing connections
    display_scoreboard("--- FINAL SCORES ---")

    broadcast("GAME_OVER_BYE")

    # Small delay to allow clients to receive message
    time.sleep(1)

    with lock:
        for conn in clients:
            try:
                conn.close()
            except:
                pass

        # Reset all game state
        clients.clear()
        guesses.clear()
        names.clear()
        points.clear()

# MAIN GAME LOGIC
# Runs all rounds of the game
def play_game():
    for round_num in range(1, ROUNDS + 1):
        # Generate random number for this round
        secret = random.randint(1, 100)
        print(f"Round {round_num}: secret is {secret}")

        # Clear previous guesses
        with lock:
            guesses.clear()

        # Reset guess event
        guess_event.clear()

        # Notify players to start guessing
        broadcast(f"\n=== ROUND {round_num}/{ROUNDS} ===\nYou have {GUESS_TIME} seconds! Guess a number between 1 and 100: ")

        # Wait for all guesses or timeout
        guess_event.wait(timeout=GUESS_TIME)

        # Identify players who did not guess
        with lock:
            missing = [names[conn] for conn in clients if names[conn] not in guesses]

        if missing:
            broadcast(f"{', '.join(missing)} didn't guess in time — 0 pts!\n")

        # Calculate scores and display results
        calculate_points(secret)
        display_scoreboard(f"--- SCORES AFTER ROUND {round_num} ---")

# GAME LOOP
# Waits for enough players, runs game, then resets
def game_loop(num_players):
    while True:
        print(f"Waiting for {num_players} players...")

        # Wait until required number of players connect
        while len(clients) < num_players:
            time.sleep(0.1)

        # Start game
        broadcast(f"All players connected! Starting {ROUNDS} rounds!\n")

        play_game()

        # End game and reset
        disconnect_all()

        print("Game finished. Waiting for new players...\n")
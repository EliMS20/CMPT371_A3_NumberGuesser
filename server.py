import socket
import threading
import game

# SERVER CONFIGURATION
# Defines IP address and port for the server
# 127.0.0.1 means local machine only
HOST = '127.0.0.1'
PORT = 5050

# Number of players required to start the game
NUM_PLAYERS = 2


# CLIENT HANDLER
# Handles communication with one client
# Each client runs in its own thread
def handle_client(conn, addr):
    '''
    Manages client interaction
    - Handles username setup
    - Processes guesses
    - Cleans up on disconnect
    '''

    try:
        # MAIN CLIENT LOOP
        # Continuously receives and processes client messages
        while True:
            data = conn.recv(1024).decode('utf-8').strip()

            # No data means client disconnected
            if not data:
                break
            
            # CONNECTION SETUP
            # Client sends "CONNECT:<name>" to register
            if data.startswith("CONNECT"):
                name = data.split(":")[1] if ":" in data else "Unknown"

                # Ensure username is unique
                while game.is_name_taken(name):
                    conn.send("NAME_TAKEN".encode('utf-8'))
                    data = conn.recv(1024).decode('utf-8').strip()
                    name = data.split(":")[1] if ":" in data else "Unknown"

                game.add_client(conn, name)
                conn.send("NAME_OK".encode('utf-8'))
                print(f"{name} ({addr}) connected, total clients: {len(game.clients)}")

            # DISCONNECT HANDLING
            # Client requests to disconnect
            elif data == "DISCONNECT":
                break

            # GAME INPUT PROCESSING
            # Treat input as a guess
            else:
                try:
                    game.submit_guess(conn, int(data))
                except ValueError:
                    # Invalid input handling
                    conn.send("Please send a valid number!\n".encode('utf-8'))

    except:
        # Prevent crash on unexpected errors
        pass

    finally:
        # CLEANUP
        # Remove client and close connection
        print(f"Client {name} ({addr}) disconnected")
        game.remove_client(conn)
        conn.close()


# SERVER STARTUP
# Sets up server and accepts connections
def start_server():
    # Create TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind to host and port
    server.bind((HOST, PORT))

    # Start listening
    server.listen()

    # Prevent accept from blocking forever
    server.settimeout(0.1)

    print(f"Server listening on {HOST}:{PORT}")

    # GAME LOOP THREAD
    # Runs game logic separately
    game_thread = threading.Thread(target=game.game_loop, args=(NUM_PLAYERS,))
    game_thread.daemon = True
    game_thread.start()

    try:
        # CONNECTION LOOP
        # Accepts clients and assigns threads
        while True:
            try:
                conn, addr = server.accept()

                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.daemon = True
                thread.start()

            except socket.timeout:
                continue

    except KeyboardInterrupt:
        # Shutdown on manual stop
        print("Shutting down server")

    finally:
        # Close server socket
        server.close()


# ENTRY POINT
# Runs server when file is executed
if __name__ == "__main__":
    start_server()
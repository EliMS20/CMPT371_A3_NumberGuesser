import socket
import threading
import game

# SERVER IP AND PORT NUMBER
HOST = '127.0.0.1'
PORT = 5050

# NUMBER OF EXPECTED PLAYERS FOR GAME
NUM_PLAYERS = 2

# CLIENT HANDLER
def handle_client(conn, addr):
    '''
    handle_client(conn, addr) manages client inputs
        Specifically, it handles the client's guess and applies the 
            necessary game logic to it.
    
    arguments:
        conn: A socket object that represents the connection between the server 
            and a specific client.
        addr: A tuple, (IP, port), which represents the client's network address.
    '''

    # The main client loop 
    try:
        
        # Continuously runs until a specific client disconnects or if the game ends.
        while True:
            data = conn.recv(1024).decode('utf-8').strip()
            if not data:
                break
            
            if data.startswith("CONNECT"):
                name = data.split(":")[1] if ":" in data else "Unknown"

                # Keep asking until a unique name is given
                while game.is_name_taken(name):
                    conn.send("NAME_TAKEN".encode('utf-8'))
                    data = conn.recv(1024).decode('utf-8').strip()
                    name = data.split(":")[1] if ":" in data else "Unknown"

                game.add_client(conn, name)
                conn.send("NAME_OK".encode('utf-8'))
                print(f"{name} ({addr}) connected, total clients: {len(game.clients)}")

            elif data == "DISCONNECT":
                break

            else:
                try:
                    game.submit_guess(conn, int(data))
                except ValueError:
                    conn.send("Please send a valid number!\n".encode('utf-8'))

    except:
        pass

    finally:
        print(f"Client {name} ({addr}) disconnected")  # use addr, always defined
        game.remove_client(conn)
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    server.settimeout(0.1)

    print(f"Server listening on {HOST}:{PORT}")

    game_thread = threading.Thread(target=game.game_loop, args=(NUM_PLAYERS,))
    game_thread.daemon = True
    game_thread.start()

    try:
        while True:
            try:
                conn, addr = server.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.daemon = True
                thread.start()
            except socket.timeout:
                continue

    except KeyboardInterrupt:
        print("Shutting down server")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
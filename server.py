import socket
import threading
import game

HOST = '127.0.0.1'
PORT = 5050
NUM_PLAYERS = 2

def handle_client(conn, addr):
    print(f"New connection from {addr}")

    try:
        while True:
            data = conn.recv(1024).decode('utf-8').strip()
            if not data:
                break

            if data == "CONNECT":
                game.add_client(conn)
                print(f"Client connected, total clients: {len(game.clients)}")
            else:
                try:
                    game.submit_guess(conn, int(data))
                except ValueError:
                    conn.send("Please send a valid number!\n".encode('utf-8'))

    except:
        pass
    finally:
        print(f"Client {addr} disconnected")
        game.remove_client(conn)
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    server.settimeout(1)

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
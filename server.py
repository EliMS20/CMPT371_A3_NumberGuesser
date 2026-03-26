import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 5050

clients = []

def handle_client(conn, addr):
    print(f"New connection from {addr}")

    try:
        while True:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            if "CONNECT" in data:
                clients.append(conn)
                print(f"Client connected, total clients: {len(clients)}")

    except:
        pass
    finally:
        print(f"Client {addr} disconnected")
        conn.close()
        if conn in clients:
            clients.remove(conn)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    server.settimeout(1)

    print(f"Server is listening on {HOST}:{PORT}")

    runServer = True

    try:
        while runServer:
            try:
                conn, addr = server.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.start()

            except socket.timeout:
                continue

    except KeyboardInterrupt:
        print("Shutting down server")
        runServer = False

    finally:
        server.close()

if __name__ == "__main__":
    start_server()
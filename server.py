import socket
import threading
import json

HOST = '127.0.0.1'
PORT = 5050

clients = []

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server is listening on {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server.accept()
            data  = conn.recv(1024).decode('utf-8')

            if "CONNECT" in data:
                clients.append(conn)
                print(f"Client connected, total clients: {len(clients)}")
            
    except KeyboardInterrupt:
        print("Shutting down server")
    finally:
        server.close()

if __name__ == "main":
    pass
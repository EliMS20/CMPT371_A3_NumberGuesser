import socket
import threading
import os

stop_event = threading.Event()

def receive(client):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg:
                print(f"\nServer: {msg}")
            else:
                print("\nServer disconnected. Press Enter to exit.")
                stop_event.set()
                client.close()
                os._exit(0)  # force kill the whole program including blocked input()
        except:
            print("\nLost connection to server. Press Enter to exit.")
            stop_event.set()
            os._exit(0)
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('127.0.0.1', 5050))
    except ConnectionRefusedError:
        print("Could not connect to server.")
        return

    thread = threading.Thread(target=receive, args=(client,))
    thread.daemon = True
    thread.start()

    name = input("Enter your name: ")
    client.send(f"CONNECT:{name}".encode('utf-8'))

    try:
        while not stop_event.is_set():
            msg = input()
            if msg and not stop_event.is_set():
                client.send(msg.encode('utf-8'))

    except KeyboardInterrupt:
        print("\nDisconnecting from server...")
        try:
            client.send("DISCONNECT".encode('utf-8'))
        except:
            pass

    finally:
        client.close()
        print("Disconnected.")

if __name__ == "__main__":
    main()
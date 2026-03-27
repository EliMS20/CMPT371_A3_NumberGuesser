import socket
import threading
import os

stop_event = threading.Event()

def receive(client):
    while not stop_event.is_set():
        try:
            data = client.recv(4096)
            if not data:
                if not stop_event.is_set():
                    print("\nServer disconnected.")
                    stop_event.set()
                    os._exit(0)
                break

            msg = data.decode('utf-8')

            if "GAME_OVER_BYE" in msg:
                clean_msg = msg.replace("GAME_OVER_BYE", "").strip()
                if clean_msg:
                    print(f"\n{clean_msg}")
                print("\nGame over! Thanks for playing.")
                stop_event.set()
                os._exit(0)
                break

            print(f"\n{msg}")

        except:
            if not stop_event.is_set():
                print("\nLost connection to server.")
                stop_event.set()
                os._exit(0)
            break

    client.close()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('127.0.0.1', 5050))
    except ConnectionRefusedError:
        print("Could not connect to server.")
        return

    # Name handshake BEFORE starting receive thread so it can't intercept the response
    while True:
        name = input("Enter your name: ")
        client.send(f"CONNECT:{name}".encode('utf-8'))
        response = client.recv(1024).decode('utf-8').strip()

        if response == "NAME_OK":
            print(f"Joined as {name}! Waiting for game to start...")
            break
        elif response == "NAME_TAKEN":
            print(f"Name '{name}' is already taken, try another.")

    # Only start receive thread once name is accepted
    thread = threading.Thread(target=receive, args=(client,))
    thread.daemon = True
    thread.start()

    try:
        while not stop_event.is_set():
            msg = input()
            if stop_event.is_set():
                break
            if msg:
                client.send(msg.encode('utf-8'))
    except KeyboardInterrupt:
        stop_event.set()
        try:
            client.send("DISCONNECT".encode('utf-8'))
            print("\nDisconnecting...")
        except:
            pass
    finally:
        client.close()
        print("Disconnected.")

if __name__ == "__main__":
    main()
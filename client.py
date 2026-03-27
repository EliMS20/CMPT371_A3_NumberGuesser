import socket
import threading
import os

stop_event = threading.Event()
# Wait to receive a message from the server, and upon receiving, do actions
def receive(client):
    while not stop_event.is_set():
        try:
            data = client.recv(4096)
            if not data:
                if not stop_event.is_set():
                    print("\nServer disconnect")
                    stop_event.set()
                    os._exit(0)
                break

            msg = data.decode('utf-8')
            # Check if game is over, and whether should
            if "GAME_OVER_BYE" in msg:
                clean_msg = msg.replace("GAME_OVER_BYE", "").strip()
                if clean_msg:
                    print(f"\n{clean_msg}")
                print("\nGAME OVER")
                stop_event.set()
                os._exit(0)
                break

            print(f"\n{msg}")

        except:
            if not stop_event.is_set():
                print("\nNo Connection to Server")
                stop_event.set()
                os._exit(0)
            break

    client.close()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('127.0.0.1', 5050))
    except ConnectionRefusedError:
        print("Could not connect to server")
        return

    while True:
        name = input("Enter name: ")
        client.send(f"CONNECT:{name}".encode('utf-8'))
        response = client.recv(1024).decode('utf-8').strip()

        if response == "NAME_OK":
            client_ip, client_port = client.getsockname()
            print(f"Connected from IP: {client_ip}, Port: {client_port}")
            print(f"Hello {name}! Waiting for other players. Game will start soon.")
            break
        elif response == "NAME_TAKEN":
            print(f"Name '{name}' Has been taken, input another: ")

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
        except:
            pass
    finally:
        client.close()
        print("Disconnected")

if __name__ == "__main__":
    main()
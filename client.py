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
                clean_msg = msg.replace("GAME_OVER_BYE", "")
                if clean_msg.strip():
                    print(f"\n{clean_msg}")
                
                print("\nThe game has ended. Final scores received.")
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

    thread = threading.Thread(target=receive, args=(client,))
    thread.daemon = True
    thread.start()

    name = input("Enter your name: ")
    client.send(f"CONNECT:{name}".encode('utf-8'))

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
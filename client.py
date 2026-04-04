import socket
import threading
import os

# THREAD CONTROL
# Event used to stop all client activity safely
stop_event = threading.Event()

# RECEIVE FUNCTION
# Listens for messages from the server and handles them
def receive(client):
    while not stop_event.is_set():
        try:
            # Receive data from server
            data = client.recv(4096)

            # Server disconnected
            if not data:
                if not stop_event.is_set():
                    print("\nServer disconnect")
                    stop_event.set()
                    os._exit(0)
                break

            msg = data.decode('utf-8')

            # GAME OVER HANDLING
            # Special message sent by server to end game
            if "GAME_OVER_BYE" in msg:
                clean_msg = msg.replace("GAME_OVER_BYE", "").strip()

                if clean_msg:
                    print(f"\n{clean_msg}")

                print("\nGAME OVER")
                stop_event.set()
                os._exit(0)
                break

            # Display normal server messages
            print(f"\n{msg}")

        except:
            # Connection error handling
            if not stop_event.is_set():
                print("\nNo Connection to Server")
                stop_event.set()
                os._exit(0)
            break

    # Close socket when loop ends
    client.close()

# MAIN CLIENT FUNCTION
# Connects to server and manages user input
def main():
    # Create TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Attempt to connect to server
    try:
        client.connect(('127.0.0.1', 5050))
    except ConnectionRefusedError:
        print("Could not connect to server")
        return

    # NAME SETUP
    # Keep asking until a valid unique name is accepted
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

    # RECEIVE THREAD
    # Runs in background to listen for server messages
    thread = threading.Thread(target=receive, args=(client,))
    thread.daemon = True
    thread.start()

    try:
        # USER INPUT LOOP
        # Sends messages (guesses) to server
        while not stop_event.is_set():
            msg = input()

            if stop_event.is_set():
                break

            if msg:
                client.send(msg.encode('utf-8'))

    except KeyboardInterrupt:
        # Handle manual exit (Ctrl+C)
        stop_event.set()
        try:
            client.send("DISCONNECT".encode('utf-8'))
        except:
            pass

    finally:
        # Cleanup on exit
        client.close()
        print("Disconnected")

# ENTRY POINT
# Runs client when file is executed
if __name__ == "__main__":
    main()
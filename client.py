import socket
import threading

def receive(client):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg:
                print(f"\nServer: {msg}")
        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))

    thread = threading.Thread(target=receive, args=(client,))
    thread.daemon = True
    thread.start()

    while True:
        msg = input()
        if msg:
            client.send(msg.encode('utf-8'))

if __name__ == "__main__":
    main()
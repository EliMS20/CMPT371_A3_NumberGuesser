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
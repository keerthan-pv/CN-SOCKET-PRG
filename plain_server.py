import socket
import threading

def handle_client(client_sock, addr):
    print(f"[Plain] Connection from {addr}")
    data = client_sock.recv(1024).decode().strip()
    print(f"[Plain] Client says: {data}")
    client_sock.send(f"Plain Server received: {data}".encode())
    client_sock.close()

def start_plain_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8888))
    server_socket.listen(5)
    print("Plain Server is running on port 8888...")

    while True:
        client_sock, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_sock, addr)).start()

if __name__ == "__main__":
    start_plain_server()

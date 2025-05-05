# proxy_server.py
import socket
import ssl
import threading

AUTH_TOKEN = 'secret123'

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

def handle_client(client_sock, addr):
    try:
        ssl_client = context.wrap_socket(client_sock, server_side=True)
        data = ssl_client.recv(1024).decode().strip()
        if data != AUTH_TOKEN:
            ssl_client.send(b"Access denied")
            return
        
        ssl_client.send(b"Authorized. Please send your message:")
        message = ssl_client.recv(1024).decode().strip()
        print(f"[Proxy] Client says: {message}")
        ssl_client.send(f"Proxy Server received: {message}".encode())

    except ssl.SSLError as e:
        print(f"[Proxy] SSL error with {addr}:", e)
    finally:
        ssl_client.close()

def start_proxy_server():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind(('0.0.0.0', 8443))
    proxy_socket.listen(5)
    print("Secure Proxy Firewall Server is running on port 8443...")

    while True:
        client_sock, addr = proxy_socket.accept()
        threading.Thread(target=handle_client, args=(client_sock, addr)).start()

if __name__ == "__main__":
    start_proxy_server()

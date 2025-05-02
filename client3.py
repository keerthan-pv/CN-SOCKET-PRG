import socket
import ssl

USE_PROXY_SERVER = False
SERVER_ADDRESS = ('127.0.0.3', 8443) if USE_PROXY_SERVER else ('127.0.0.3', 8888)

if USE_PROXY_SERVER:
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.create_connection(SERVER_ADDRESS) as sock:
        with context.wrap_socket(sock, server_hostname='localhost') as ssock:
            # Ask user for password input
            password = input("Enter password: ")
            ssock.sendall(password.encode())  # Send entered password

            auth_response = ssock.recv(1024)
            decoded_response = auth_response.decode()

            if decoded_response.lower().startswith("access denied"):
                print("Incorrect password. You are blocked.")
            else:
                print("Connection established.")
                message = input("Enter your message: ")
                ssock.sendall(message.encode())
                response = ssock.recv(1024)
                print("Server response:", response.decode())
else:
    with socket.create_connection(SERVER_ADDRESS) as sock:
        sock.sendall(b"Hello from Plain Client3!")
        response = sock.recv(1024)
        print("Server response:", response.decode())

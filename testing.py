import socket

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.listen(1)

print(f'Listening on port = {SERVER_PORT}')


while True:

    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()
    print(request)

    clientheaders = request.split('\n')

    filename = clientheaders[0].split()[1]

    if filename == '/':
        with open('index.html', 'r') as file:
            content = file.read()

    if filename == '/ayush':
        with open('ayush.html', 'r') as file:
            content = file.read()

    body = content.encode('utf-8')

    headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )

    encoded_headers = headers.encode('utf-8')

    client_connection.sendall(encoded_headers + body)
    client_connection.close()


server_socket.close()

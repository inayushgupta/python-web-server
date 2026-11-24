import socket

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.listen(1)

print(f'Listening on port = {SERVER_PORT}')


while True:

    RESP = 200
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()
    print(request)

    clientheaders = request.split('\n')

    filename = clientheaders[0].split()[1]
    if filename == '/':
        filename = 'index.html'
    else:
        filename = filename[1:]
        print(filename)

    # try opening the file
    try:
        with open(filename+".html") as file:
            content = file.read()
    except FileNotFoundError:
        with open('404.html') as file:
            content = file.read()
        RESP = 404


    body = content.encode('utf-8')

    headers = (
        f"HTTP/1.1 {RESP} {'Not Found' if RESP == 404 else 'OK'}\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )

    encoded_headers = headers.encode('utf-8')

    client_connection.sendall(encoded_headers + body)
    client_connection.close()


server_socket.close()

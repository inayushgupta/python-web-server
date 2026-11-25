import socket
import threading

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)

HEADER = 64
FORMAT = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def get_complete_message(conn, total):
    
    chunks = []
    got = 0

    while got < total:

        chunk = conn.recv(total-got)
        
        if not chunk:
            return None
        
        chunks.append(chunk)
        got += len(chunk) 
        
    return b''.join(chunks)

def send_message(conn, message):

    encoded_message = message.encode(FORMAT)
    size = len(encoded_message)
    header = str(size).encode(FORMAT)
    header += b' ' * (HEADER - len(header))

    conn.sendall(header + encoded_message)
        
def receive(conn):

    while True:
        message_size = get_complete_message(conn, HEADER)

        if message_size is None:
            break

        message_size = int(message_size.decode(FORMAT).strip())
        message = get_complete_message(conn, message_size)

        if message is None:
            break

        message = message.decode(FORMAT).strip()
        print(message)

client.connect(ADDR)
conn = client
threading.Thread(target=receive, args=(conn, )).start()

while True:
    text = input('> ')
    send_message(conn, text)










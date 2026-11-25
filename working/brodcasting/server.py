import socket
import threading

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)

HEADER = 64
FORMAT = 'utf-8'
LIST_LOCK = threading.Lock()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

server.listen()

# stores data of active users connected to server
active_connections = []

# sends the message to every connected clients
# except for the one that is sending the message

def send_message(conn, message):

    encoded_message = message.encode(FORMAT)
    size = len(encoded_message)
    header = str(size).encode(FORMAT)
    header += b' ' * (HEADER - len(header))

    conn.sendall(header + encoded_message)



def broadcast_message(message, sender_addr):

    with LIST_LOCK:
        for conn, addr in active_connections:
            
            if addr == sender_addr:
                continue
            try:
                send_message(conn, message)
            except OSError:
                pass
            

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

def instance(conn, addr):

    while True:
        
        message_size = get_complete_message(conn, HEADER)
        if message_size is None:
            break

        message_size = int(message_size.decode(FORMAT).strip())

        message = get_complete_message(conn, message_size)
        if not message:
            break

        message = message.decode(FORMAT).strip()
        if message == 'dis':
            break

        broadcast_message(message, addr)
        
    print(f"connection closed for {addr}")

    with LIST_LOCK:
        if (conn, addr) in active_connections:
            active_connections.remove((conn, addr))

    conn.close()

def start():
    
    while True:
        conn, addr = server.accept()
        new_thread = threading.Thread(target=instance, args=(conn, addr))
        
        with LIST_LOCK:
            active_connections.append((conn, addr))
        
        new_thread.start()

start()



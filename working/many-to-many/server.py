import socket
import threading

def logger(instance, message):
    print(f"[{instance.upper()}]:[{message}]")

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 7654
FORMAT = 'utf-8'
HEADER = 64
ADDR = (SERVER, PORT) 

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

def recv_collect(conn, num_bytes):

    chunks = []
    bytes_got = 0

    while bytes_got < num_bytes:
        
        chunk = conn.recv(num_bytes-bytes_got)

        if not chunk:
            return None
        
        chunks.append(chunk)
        bytes_got += len(chunk)

    return b''.join(chunks)

def runners(conn, addr):

    while True:

        raw_data = recv_collect(conn, HEADER)

        if not raw_data:
            logger("disconnected", 'unexpected disconnection')
            break
        
        length = int(raw_data.decode(FORMAT).strip())
        raw_data = recv_collect(conn, length)

        if not raw_data:
            break
        
        data = raw_data.decode(FORMAT).strip()

        if data == 'dis':
            logger('disconnect', 'client is disconnecting')
            break
        
        logger('message', data)

    conn.close()

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        newthread = threading.Thread(target=runners, args=(conn, addr))
        newthread.start()
        logger('new thread spawned', 'establishing new connection')

        

logger('server', 'starting')
start()




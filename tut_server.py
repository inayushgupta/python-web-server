import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DIS'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to the address
server.bind(ADDR)

def handle_client(conn, addr):
    
    connected = True
    print(f"[NEW CONNECTION]: {addr} connected")
    
    while connected:
        # this is also blocking
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:

            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
        
            if msg == DISCONNECT_MESSAGE:
                connected = False
            
            print(f"[{addr}]:{msg}")
            conn.sendall("MESSAGE RECEIVED!".encode(FORMAT))
    
    conn.close()



def start():
    server.listen()
    print(f"[LISTENING]:{SERVER}" )
    while True:

        # this line is blocking
        # it waits for the client
        # it returns connection and the address
        # of the client

        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print('[ACTIVE CONNECTION]:' + str(threading.activeCount() - 1))


server.listen()

print("[STARTING]:Server is starting")
start()



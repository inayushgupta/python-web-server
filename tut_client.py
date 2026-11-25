import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DIS'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)

    send_length += b' ' * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)
    
    got = client.recv(1024).decode(FORMAT)
    print(got)

while True:
    print("ENTER THE MESSAGE : ", end="")
    typed_message = input()
    send(typed_message)


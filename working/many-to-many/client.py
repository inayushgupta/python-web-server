import socket

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 7654
FORMAT = 'utf-8'
HEADER = 64
ADDR = (SERVER, PORT) 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send_message(msg):

    message_bytes = msg.encode(FORMAT)
    message_length = len(msg)

    send_length = str(message_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    client.sendall(send_length)
    client.sendall(message_bytes)


print("CONNECTED TO SERVER\n\n")
while True:
    user_input = input("> ")
    send_message(user_input)

    if user_input == 'dis':
        break

client.close()
print('DISCONNECTED')


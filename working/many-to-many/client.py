import socket
import sys

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 7654
FORMAT = 'utf-8'
HEADER = 64
ADDR = (SERVER, PORT) 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(ADDR)
except ConnectionRefusedError:
    print("Server refused connection request")
    print("Possible cause: server not started")
finally:
    sys.exit(1)

def send_message(msg):

    message_bytes = msg.encode(FORMAT)
    message_length = len(msg)

    send_length = str(message_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    client.sendall(send_length)
    client.sendall(message_bytes)


print("CONNECTED TO SERVER\n\n")

try:
    while True:
        user_input = input("> ")
        send_message(user_input)

        if user_input == 'dis':
            break
except KeyboardInterrupt:
    print("")
    send_message('dis')

finally:
    client.close()
    print('DISCONNECTED')


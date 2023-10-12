import socket
import json
import threading

# Server configuration
HOST = '127.0.0.1' # Loopback address for localhost
PORT = 12345 # Port to listen on


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

client_socket.connect((HOST, PORT))

print(f"Connected to {HOST}:{PORT}")

state = 0

nickname = 'Guest'
room_name = 'General'

def receive_message():
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break
        print(f"{message}")

receive_message = threading.Thread(target=receive_message)
receive_message.daemon = True
receive_message.start()

while True:
    if state == 0:
        nickname = input("Input your nickname (or 'exit' to quit):")
        if nickname.lower() == 'exit':
            break
        state = 1

    if state == 1:
        room_name = input("Input your room (or 'exit' to quit):")
        if room_name.lower() == 'exit':
            break
        state = 2
        print(f"You are in Room: {room_name}\nFeel free to chat")

        struct = {
            "type" : "connect",
            "payload" : {
                "name" : nickname,
                "room" : room_name
            }
        }

        message = json.dumps(struct)

        client_socket.send(message.encode('utf-8'))

    if state == 2:
        message= input("")

        if message.lower() == 'exit':
            break

        struct = {
            "type" : "message",
            "payload" : {
                "name" : nickname,
                "room" : room_name,
                "message" : message
            }
        }

        message = json.dumps(struct)

        client_socket.send(message.encode('utf-8'))


client_socket.close()
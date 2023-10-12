import socket
import threading
import json

client_rooms = dict()

def send_all(clients : list, buffer, exception=None):
    for client in clients:
        if client != exception:
            client.send(buffer)

def handle_client(client_socket, client_address):
    name = ''
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        struct = json.loads(message)
        type = struct["type"]


        # {
        #     "type" : "connect",
        #     "name" : name,
        #     "room" : room
        # }

        if   type == "connect":
            name = struct["name"]
            room = struct["room"]
            if room in client_rooms.items():
                client_rooms[room].append(name)
                struct = {
                    "type" : "notification",
                    "message" : f"{name} has joined the room"
                }
                response_message = json.dumps(struct).encode('utf-8')
                send_all(client_rooms[room], response_message, exception=client_socket)
            else:
                client_rooms[room] = [name]

        # {
        #     "type" : "message",
        #     "message" : message
        # }

        elif type == "message":
            struct = {
                "type" : "message",
                "message" : f"""{name}: {struct["name"]}"""
            }
            message = json.dumps(message).encode('utf-8')
            send_all(client_rooms[room], message, exception=client_socket)
            
        # {
        #     "type" : "upload"
        #     "file name" : name
        #     "file size" : int
        # }
        
        elif type == "upload_file":
            pass
            
        # {
        #     "type" : "download"
        #     "file name" : name
        # }
        
        elif type == "download_file":
            pass

HOST = '127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
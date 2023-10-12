import socket
import json
import threading
import os
import re

HOST = '127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.connect((HOST, PORT))

print(f"Connected to {HOST}:{PORT}")

def receive_message():
    while True:
        message = server_socket.recv(1024).decode('utf-8')
        struct = json.loads(message)
        _type = struct["type"]
        
        if _type == "message":
            print(struct["message"])
            
receive_message = threading.Thread(target=receive_message)
receive_message.daemon = True
receive_message.start()

nickname = input("Input your nickname: ")
roomname = input("Input the room you want to enter (Enter for General): ")
if roomname == '':
    roomname = 'General'
    
struct = {
    "type" : "connect",
    "name" : nickname,
    "room" : roomname
}
message = json.dumps(struct).encode('utf-8')
server_socket.send(message)


while True:
    message = input()
    x = re.search('^upload: .*', message)
    if x != None:
        file_path = message[8 : (x.span()[1])]
        if os.path.isfile(file_path):
            struct = {
                "type" : "upload file",
                "file name" : os.path.basename(file_path),
                "file size" : os.path.getsize(file_path)
            }
            message = json.dumps(struct).encode('utf-8')
            server_socket.send(message)
            message = server_socket.recv(1024).decode('utf-8')
            print("confirmed")
            struct = json.loads(message)
            _type = struct["type"]
            if _type == "upload not permitted":
                print(f"Failed: {type}\nReason: {struct["reason"]}")
            elif _type == "upload permitted":
                print('permission received')
                f = open(file_path, "rb")
                file_content = f.read()
                server_socket.send(file_content)
                f.close()
        else:
            print("The path to this file cannot be found\n")
    else:
        x = re.search('^download: .*', message)
    if x != None:
        file_name = message[10 : (x.span()[1])]
        if os.path.isfile(file_path):
            struct = {
                "type" : "download file",
                "file name" : file_name
            }
            message= json.dumps(struct).encode('utf-8')
            server_socket.send(message)
            message = server_socket.recv(1024).decode('utf-8')
            struct = json.loads(message)
            _type = struct["type"]
            if _type == "file not found":
                print(f"Failed: {_type}")
            elif _type == "file found":
                file_size = struct["file size"]
                decision = input(f"Download file {file_name} , size: {file_size}. Press (Y/n) to confirm")
                if decision == '' or decision == 'Y' or decision == 'y':
                    struct = {
                        "type" : "download confirm"
                    }
                    response_message = json.dumps(struct).encode('utf-8')
                    server_socket.send(response_message)
                    file_content = server_socket.recv(file_size)
                    f = open(file_name, "wb")
                    f.write(file_content)
                    f.close()
                else:
                    struct = {
                        "type" : "download abort"
                    }
                    response_message = json.dumps(struct).encode('utf-8')
                    server_socket.send(response_message)
                    print("File not found on the server media")
        else:
            print("The path to this file cannot be found\n")
    elif message == 'exit':
        break
    else:
        struct = {
            "type" : "message",
            "message" : message
        }
        message = json.dumps(struct).encode('utf-8')
        server_socket.send(message)
    
server_socket.close()
import socket
import threading
import json

HOST = '127.0.0.1' # Loopback address for localhost
PORT = 12345 # Port to listen on
# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the specified address and port
server_socket.bind((HOST, PORT))
# Listen for incoming connections
server_socket.listen()
print(f"Server is listening on {HOST}:{PORT}")

clients = dict()
# Function to handle a client's messages
def handle_client(client_socket, client_address):

    message = client_socket.recv(1024).decode('utf-8')
    struct = json.loads(message)

    if struct["type"] == "connect":
        room = struct["payload"]["room"]
        if not struct["payload"]["room"]:
            room = "General"
        if room not in clients.keys():
            clients[room] = [client_socket]
        else:
            clients[room].append(client_socket)

    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break # Exit the loop when the client disconnects 
        
        struct = json.loads(message)
        if struct["type"] == "message":

            message = f"""{struct["payload"]["name"]}: {struct["payload"]["message"]}"""
                    # Broadcast the message to all clients
            for client in clients[room]:
                # if client != client_socket: # find alternative to this IF
                if client != client_socket:
                    client.send(message.encode('utf-8'))
    # Remove the client from the list
    clients[room].remove(client_socket)
    client_socket.close()

while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
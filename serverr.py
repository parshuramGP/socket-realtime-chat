import socket
import threading

HOST ='127.0.0.1'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

clients = {}
nicknames = {}


def broadcast(message):
    for client in clients.values():
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)

            broadcast(message)
        except:
            index = list(clients.values()).index(client)
            del clients[nicknames[index]]
            del nicknames[index]
            client.close()
            broadcast(f"{nicknames[index]} has left the chat".encode())
            break


def receive():
    while True:
        client, address = server_socket.accept()
        print(f"Connection established with {address}")

        client.send("Enter your nickname: ".encode())
        nickname = client.recv(1024).decode()

        clients[nickname] = client
        nicknames[list(clients.values()).index(client)] = nickname

        client.send("Welcome to the chat!".encode())
        broadcast(f"{nickname} has joined the chat".encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening on {}:{}".format(HOST, PORT))

receive()

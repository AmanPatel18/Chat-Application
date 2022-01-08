import threading
import sys
import socket

host='10.0.0.4'
port=9999
server=socket.socket()
server.bind((host,port))
server.listen()
clients = []
names = []

# function to broadcast the message received from other clients to all the clients
def broadcast(message):
    for client in clients:
        client.send(message)

# function to handle the client connection
def handle_client(client):
    while True:
        try:
            message=client.recv(1024)
            broadcast(message)
        except:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            name=names[index]
            broadcast(f'{name} has left the chat room!'.encode('utf-8'))
            names.remove(name)
            break

# function to accept the new connections from the client
def receive():
    while True:
        print('\nServer is running!')
        print('Listening to the new connections...')
        client, address = server.accept()
        print('\nNew connection is established!')
        print(f'IP Address: {address[0]}')
        print(f'Port Number: {address[1]}')

        #client.send('Your name: '.encode('utf-8'))
        name=client.recv(1024).decode('utf-8')
        names.append(name)
        clients.append(client)

        print(f'Name of the client: {name}')
        broadcast(f'{name} has connected to the chat room!'.encode('utf-8'))

        thread=threading.Thread(target=handle_client,args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()

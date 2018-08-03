"""
project for a chatBot, source blog at
'https://www.codementor.io/saurabhchaturvedi63/
let-s-write-a-chat-app-in-python-e6lhqym8h?utm_swu=3470'
this is the server side script for multithreaded asynchronous chat app
"""
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread

# set constants
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

# 3 functions for accepting new connections, broadcasting messages
# and handling particular clients
def accepting_incoming_connections():
    """Sets up handling for incoming clients"""
    # set infinite loop so connection is always open
    while True:
        client, client_address = SERVER.accept()
        print('{} has connected.'.format(client_address))
        client.send(bytes('Greetings from the cave!' + '\n'
                    + 'Now type your name and press enter', 'utf8'))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client): # takes client as argument
    """Handles a single client connection"""
    name = client.recv(BUFSIZ).decode('utf8')
    welcome = 'Welcome {}! If you ever want to quit, type \'quit\' to exit'.format(name)
    client.send(bytes(welcome, 'utf8'))
    msg = '{} has joined the chat!'.format(name)
    broadcast(bytes(msg, 'utf8'))
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes('quit', 'utf8'):
            broadcast(msg, name + ': ')
        else:
            client.send(bytes('quit', 'utf8'))
            client.close()
            del clients[client]
            broadcast(bytes('{} has left the chat.'.format(name), 'utf8'))
            break

def broadcast(msg, prefix=''): # prefix is for name identification
    """Broadcasts a message to all the clients"""
    for sock in clients:
        sock.send(bytes(prefix, 'utf8') + msg)

if __name__ == "__main__":
    SERVER.listen(5) # listens for 5 connections at max
    print('Waiting for connection...')
    ACCEPT_THREAD = Thread(target=accepting_incoming_connections)
    ACCEPT_THREAD.start() # starts the infinite loop
    ACCEPT_THREAD.join()
    SERVER.close()

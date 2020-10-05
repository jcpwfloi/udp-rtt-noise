from socket import *

bind = '' #listen on any
port = 4098

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((bind, port))

while True:
    message, address = serverSocket.recvfrom(2048)
    print(message, address)
    serverSocket.sendto(message, address)

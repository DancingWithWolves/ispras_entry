from socket import *

print("Helloworld!")
server_port = 12000
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', server_port))
print("The server is ready to receive")
while True:
    message, client_address = server_socket.recvfrom(2048)
    server_socket.sendto(client_address[0], client_address)

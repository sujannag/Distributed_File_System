#Provides the directory service for the Distributed File Systems.
from socket import *
import server_ports

# Setup the directory service socket
server_socket = socket(AF_INET,SOCK_STREAM)
server_socket.bind(('localhost', server_ports.get_directory_service_port()))
server_socket.listen(10)

print ('Directory Service is ready to receive...')

def main():

	while True:
		connection_socket, addr = server_socket.accept()

		response = ""
		recv_msg = connection_socket.recv(1024)
		recv_msg = recv_msg.decode()
		print(recv_msg)

		response = ("DS: Received")
		connection_socket.send(response.encode())
		connection_socket.close()


if __name__ == "__main__":
	main()
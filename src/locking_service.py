#Provides the locking service for the Distributed File Systems.

from socket import *
import server_ports

serverAddr = "localhost"
serverPort = server_ports
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverAddr, serverPort))
serverSocket.listen(10)

if __name__ == "__main__":
	main()
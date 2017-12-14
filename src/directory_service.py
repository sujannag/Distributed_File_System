#Provides the directory service for the Distributed File Systems.

def main():

	while True:
		connectionSocket, addr = serverSocket.accept()

		response = ""
		recv_msg = connectionSocket.recv(1024)
		recv_msg = recv_msg.decode()
		print(recv_msg)

		response = ("DS: Received")
		connectionSocket.send(response.encode())
		connectionSocket.close()


if __name__ == "__main__":
	main()
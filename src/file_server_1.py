#Provides the file server services for the Distributed File Systems.

from socket import *
import server_ports

server_address = "localhost"
server_port = server_ports.get_file_server_port()
server_socket = socket(AF_INET,SOCK_STREAM)
server_socket.bind((server_address, server_port))
server_socket.listen(10)

print ('!!Started File Server 1!!')

#
#
#
def read_write_file(file_name, read_write, text, file_ver_map):
	if read_write == "r":	# if read request
		try:
			file = open(file_name, read_write)	
			text_in_file = file.read()		# read the file's text into a string
			if file_name not in file_ver_map:
				file_ver_map[file_name] = 0
			return (text_in_file, file_ver_map[file_name])			
		except IOError:				# IOError occurs when open(filepath,read_write) cannot find the file requested
			print (file_name + " does not exist in directory\n")
			return (IOError, -1)
			pass

	elif read_write == "a+":	# if write request

		if file_name not in file_ver_map:
			file_ver_map[file_name] = 0		# if empty (ie. if its a new file), set the version no. to 0
		else:
			file_ver_map[file_name] = file_ver_map[file_name] + 1		# increment version no.

		file = open(file_name, read_write)
		file.write(text)

		
		print("FILE_VERSION: " + str(file_ver_map[file_name]))
		return ("Success", file_ver_map[file_name])

#
#
#
def send_client_reply(resp, read_write, connection_socket):

	if resp[0] == "Success":
		reply = "File successfully written to..." + str(resp[1])

		print("Sending file version " + str(resp[1]))
		connection_socket.send(reply.encode())
		
	elif resp[0] is not IOError and read_write == "r":
		connection_socket.send(resp.encode())
		
	elif resp[0] is IOError: 
		reply = "File does not exist\n"
		connection_socket.send(reply.encode())

#
#
#
def main():

	file_ver_name = {}

	while 1:
		resp = ""
		connection_socket, addr = server_socket.accept()

		recv_msg = connection_socket.recv(1024)
		recv_msg = recv_msg.decode()

		if recv_msg != "" and "CHECK_VERSION" not in recv_msg:

			# file path to perform read/write on
			file_name = recv_msg.split("|")[0]	
			print ("file_name: " + file_name)

			# whether its a read or write
			read_write = recv_msg.split("|")[1]
			print ("read_write: " + read_write)

			# the text to be written (this text is "READ" for a read and is ignored)
			text = recv_msg.split("|")[2]
			print ("TEXT RECEIVED: " + text)

			# perform the read/write and check if successful
			resp = read_write_file(file_name, read_write, text, file_ver_name)

			# send back write successful message or send back text for client to read	
			send_client_reply(resp, read_write, connection_socket)

			# if read_write == 'a+':
			# 	replicate(file_name)


		elif "CHECK_VERSION" in recv_msg:
			# parse the version number to check
			client_file_name = recv_msg.split("|")[1]
			print("Version check on " + client_file_name)
			file_version = str(file_ver_name[client_file_name])
			connection_socket.send(file_version.encode())


	connection_socket.close()

if __name__ == "__main__":
	main()
from socket import *
import server_ports
import sys

#
#
#
def create_socket():
	sock = socket(AF_INET, SOCK_STREAM)
	return sock

#
#
#
def send_write(client_socket, file_server_IP_directory_service, file_server_port_directory_service, filename , RW, file_version_map, msg):
    if filename not in file_version_map:
        file_version_map[filename] = 0

    elif RW != "r":
        file_version_map[filename] = file_version_map[filename] + 1

    send_msg = filename + "|" + RW + "|" + msg 

    print("Sending version: " + str(file_version_map[filename]))

    # send the sting requesting a write to the file server
    client_socket.connect((file_server_IP_directory_service,file_server_port_directory_service))
    client_socket.send(send_msg.encode())	

#
#
#
def write(filename, client_id, file_ver_map):
    
	# create a socket to communicate with the directory service
	client_directory_service_socket = create_socket()

	# request info about the file from the directory service
	reply_directory_service = enquire_directory_service(client_directory_service_socket, filename, 'w', False)
	client_directory_service_socket.close()
	print(reply_directory_service)

	if reply_directory_service == "NO_SUCH_FILE":
		print(filename + " does not exist!!")
	else:

		file_name_directory_service = reply_directory_service.split('|')[0]
		file_server_IP_directory_service = reply_directory_service.split('|')[1]
		file_server_port_directory_service = reply_directory_service.split('|')[2]

		# write into the file
		print ("Enter text...")
		print ("write_end when done")
		
		write_client_input = ""
		while True:
			client_input = sys.stdin.readline()
			if "write_end" in client_input:  # check if user wants to finish writing
				break
			else: 
				write_client_input += client_input

		# write the data onto a file
		file_server_socket = create_socket()

		# send text and filename to the fileserver
		send_write(file_server_socket, file_server_IP_directory_service, int(file_server_port_directory_service), 
							file_name_directory_service, "a+", file_ver_map, write_client_input)
		
		reply_file_server = file_server_socket.recv(1024)
		reply_file_server = reply_file_server.decode()
		file_server_socket.close()

    	# split version num from success message and print message
		print (reply_file_server.split("...")[0])
		version_num = int(reply_file_server.split("...")[1]) 
        
		if version_num != file_ver_map[file_name_directory_service]:
			print("Server version no changed - updating client version no.")
			file_ver_map[file_name_directory_service] = version_num







#
#
#
def enquire_directory_service(file_server_socket, file_name, rw, list_files):
	
	server_name = 'localhost'
	server_port = server_ports.get_directory_service_port()
	file_server_socket.connect((server_name, server_port))

	if not list_files:
		message = file_name + '|' + rw

		# send the string requesting file info to directory send_directory_service
		file_server_socket.send(message.encode())
		reply = file_server_socket.recv(1024)
		reply = reply.decode()
	else:
		message = "LIST_FILES"

		# send the string requesting file info to directory service
		file_server_socket.send(message.encode())
		reply = file_server_socket.recv(1024)
		reply = reply.decode()
		file_server_socket.close()
		print ("Listing files on directory server...")
		print (reply)

	return reply

#
#
#
def help():
    print ("------------------- INSTRUCTIONS ----------------------")
    print ("read [filename] - Read from file!")
    print ("write_start [filename] - Write data to the file!")
    print ("write_end - Finish wrting to the file!")
    print ("help - Shows a lit of the instructions")
    print ("exit - Exits the application")
    print ("-------------------------------------------------------\n")

#
#
#
def check_input(input_string):
    # check for correct format for message split
    if len(input_string.split()) < 2:
        print ("Incorrect format")
        help()
        return False
    else:
        return True
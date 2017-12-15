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
def send_write(client_socket, file_server_IP_directory_service, file_server_port_directory_service, file_name , read_write, file_version_map, msg):
    if file_name not in file_version_map:
        file_version_map[file_name] = 0

    elif read_write != "r":
        file_version_map[file_name] = file_version_map[file_name] + 1

    send_msg = file_name + "|" + read_write + "|" + msg 

    print("Sending version: " + str(file_version_map[file_name]))

    # send the sting requesting a write to the file server
    client_socket.connect((file_server_IP_directory_service,file_server_port_directory_service))
    client_socket.send(send_msg.encode())	

#
#
#
def write(file_name, client_id, file_ver_map):
    
	# create a socket to communicate with the directory service
	client_directory_service_socket = create_socket()

	# request info about the file from the directory service
	reply_directory_service = enquire_directory_service(client_directory_service_socket, file_name, 'w', False)
	client_directory_service_socket.close()
	print(reply_directory_service)

	if reply_directory_service == "NO_SUCH_FILE":
		print(file_name + " does not exist!!")
	else:

		print(reply_directory_service)

		file_name_directory_service = reply_directory_service.split('|')[0]
		file_server_IP_directory_service = reply_directory_service.split('|')[1]
		file_server_port_directory_service = reply_directory_service.split('|')[2]

		# implement the locking service
		# create a socket to communicate with the locking services
		locking_service_socket = create_socket()
		grant_lock = get_lock_file(locking_service_socket, client_id, file_name_directory_service, "lock")
		locking_service_socket.close()

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

		# send text and file_name to the fileserver
		send_write(file_server_socket, file_server_IP_directory_service, int(file_server_port_directory_service), 
							file_name_directory_service, "a+", file_ver_map, write_client_input)
		
		reply_file_server = file_server_socket.recv(1024)
		reply_file_server = reply_file_server.decode()
		file_server_socket.close()
		print(reply_file_server)

    	# split version num from success message and print message
		print (reply_file_server.split("...")[0])
		version_num = int(reply_file_server.split("...")[1]) 
        
		if version_num != file_ver_map[file_name_directory_service]:
			print("Server version no changed - updating client version no.")
			file_ver_map[file_name_directory_service] = version_num


#
#
#
def get_lock_file(client_socket, client_id, file_name, lock_or_unlock):

    server_name = 'localhost'
    server_port = server_ports.get_directory_service_port()
    client_socket.connect((server_name,server_port))

    if lock_or_unlock == "lock":
        msg = client_id + "_1_:" + filename  # 1 = lock the file
    elif lock_or_unlock == "unlock":
        msg = client_id + "_2_:" + filename   # 2 = unlock the file

    # send the string requesting file info to directory service
    client_socket.send(msg.encode())
    reply = client_socket.recv(1024)
    reply = reply.decode()

    return reply

#
#
#
def enquire_directory_service(file_server_socket, file_name, read_write, list_files):
	
	server_name = 'localhost'
	server_port = server_ports.get_directory_service_port()
	file_server_socket.connect((server_name, server_port))

	if not list_files:
		message = file_name + '|' + read_write

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
    print ("ls - List the files present!")
    print ("read [file_name] - Read from file!")
    print ("write_start [file_name] - Write data to the file!")
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
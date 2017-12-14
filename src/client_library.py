from socket import *
import server_ports


#
#
#
def write(filename, client_id, file_ver_map):
    
    # create a socket to communicate with the directory service
    client_directory_service_socket = create_socket()

    # request info about the file from the directory service
    reply_directory_service = enquire_directory_service(client_directory_service_socket, filename)
    client_directory_service_socket.close()

    print(reply_directory_service)




#
#
#
def enquire_directory_service(client_socket, file_name):
	server_name = 'localhost'
	serverPort = directory_service_port
	client_socket.connect((server_name, server_port))

	message = "Hello! Filename:" + file_name
	client_socket.send(msg.encode())
	reply = client_socket.recv(1024)
    
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
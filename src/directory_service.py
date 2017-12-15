#Provides the directory service for the Distributed File Systems.
from socket import *
import server_ports
import csv

# Setup the directory service socket
server_socket = socket(AF_INET,SOCK_STREAM)
server_socket.bind(('localhost', server_ports.get_directory_service_port()))
server_socket.listen(10)

print ('!!Started Directory Service!!')

#
#
#
def check_file_mappings(client_message, list_files):

	print (client_message)
	file_name = client_message.split('|')[0]
	read_write = client_message.split('|')[1]

	# open the .csv file containing the file mapping
	with open("file_map.csv",'rt') as csv_file:
		d_reader = csv.DictReader(csv_file, delimiter=',')
		header = d_reader.fieldnames
		
		file_row = ""
		
		for row in d_reader:
			if list_files == False:
				# use the dictionary reader to read the values of the cells at the current row
				user_file_name = row['user_file_name']
				primary_copy = row['primary']

				print("file_name = " + file_name)
				print("read_write = " + read_write)

				if user_file_name == file_name and read_write == 'w':		# check if file inputted by the user exists	(eg. file123)
					print("WRITING")
					actual_file_name = row['actual_file_name']	# get actual file_name (eg. file123.txt)
					server_address = row['server_address']			# get the file's file server IP address
					server_port = row['server_port']			# get the file's file server PORT number

					print("actual_file_name: " + actual_file_name)
					print("server_address: " + server_address)
					print("server_port: " + server_port)

					return actual_file_name + "|" + server_address + "|" + server_port	# return string with the information on the file

				elif user_file_name == file_name and read_write == 'r' and primary_copy == 'no':
					print("READING")
					actual_file_name = row['actual_file_name']	# get actual file_name (eg. file123.txt)
					server_address = row['server_address']			# get the file's file server IP address
					server_port = row['server_port']			# get the file's file server PORT number

					print("actual_file_name: " + actual_file_name)
					print("server_address: " + server_address)
					print("server_port: " + server_port)

					return actual_file_name + "|" + server_address + "|" + server_port	# return string with the information on the file

			else:
				user_file_name = row['user_file_name']
				file_row = file_row + user_file_name +  "\n"		# append file_name to return string
		if list_files == True:
			return file_row		
	return None 	# if file does not exist return None

def main():

	while True:
		connection_socket, addr = server_socket.accept()

		response = ""
		recv_msg = connection_socket.recv(1024)
		recv_msg = recv_msg.decode()
		print(recv_msg)

		if "LIST_FILES" not in recv_msg:
			# Do not list the files
			response = check_file_mappings(recv_msg, False)

		elif "LIST_FILES" in recv_msg:
			# list the files
			response = check_file_mappings(recv_msg, True)

		if response is not None:
			response = str(response)
			
		else:
			response = "NO_SUCH_FILE"
			print("response:" + response)

		print("response:" + response)
		connection_socket.send(response.encode())
		connection_socket.close()


if __name__ == "__main__":
	main()
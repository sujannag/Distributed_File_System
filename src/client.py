import client_library	#import the client side file system proxy services
from time import gmtime, strftime
import sys

def main():

	client_library.help()
	client_id = strftime("%Y%m%d%H%M%S", gmtime())
	print(client_id)
	file_ver_map = {}

	while True:
		client_input = sys.stdin.readline()
		print(client_input)

		# List all the files
		if "ls" in client_input:
			client_directory_service_socket = client_library.create_socket()
			client_library.enquire_directory_service(client_directory_service_socket, "", "", True)
			client_directory_service_socket.close()

		if "write_start" in client_input:

			# make sure the user input is ok
			while not client_library.check_input(client_input):
				client_input = sys.stdin.readline()

			# get the filename as given by the user
			file_name = client_input.split()[1]
			print (file_name)

			resp = client_library.write(file_name, client_id, file_ver_map)
			if resp == False:
				print("Not able to write. Try again later!!")
		
		if "read" in client_input:

			# make sure the user input is ok
			while not client_library.check_input(client_input):
				client_input = sys.stdin.readline()

			# get the filename from the user
			filename = client_input.split()[1]
			print(filename)


		if "help" in client_input:
			# Show the help for the user
			client_library.help()

		if "exit" in client_input:
			# Exit the application
			print("Exiting the Client!!")
			sys.exit()


if __name__ == "__main__":
	main()



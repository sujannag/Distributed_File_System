import client_library	#import the client side file system proxy services
from time import gmtime, strftime
import sys

def main():

	client_library.help()
	client_id = strftime("%Y%m%d%H%M%S", gmtime())
	print(client_id)

	while True:
		client_input = sys.stdin.readline()
		print(client_input)

		if "write_start" in client_input:

			# make sure the user input is ok
			while not client_library.check_input(client_input):
				client_input = sys.stdin.readline()

			# get the filename as given by the user
			filename = client_input.split()[1]
			print (filename)
			
		
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



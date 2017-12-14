


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
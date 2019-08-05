# this imports the micro:bit-specific functions such as buttons, display, pins etc
from microbit import *

# brings in the micro:bit Bluetooth functions
import radio

# we use two tunes plus a bleep
import music

# Initialise all the global variables

# this variable is used to hold a single character at a time. 
character = ""

# this is an integer that is used to select one character from charList
charNum = 0

# all available characters - edit this list as required.
charList = "? ABCDEFG HIJKLM NOPQRST UVWXYZ .,:;*'?!1234567890"

# auto-detects the length of the above
numberOfChars = len(charList)

# ensures the message is blank at the outset.  
message = ""

# this is the message received so should be blank to start with.   
incomingMessage = ""

# The doneButtons variable is used to make sure that pressing BOTH buttons will
# prevent the code for buttons A OR B from operating
# When the if statement has run, the variable sets to 1 which prevents
# the other code from running.
# Each IF statement will only work if the doneButtons is 0.
doneButtons = 0

# This is the main loop that makes the programme work
while True:

    
    # resets the variable for each pass through the loop - it will only be 1 if a button has been pressed.
    doneButtons = 0

    # Pressing both buttons will send the message and play a tune
    if button_a.is_pressed() and button_b.is_pressed():

        # adds message start and end characters
        display.scroll(">" + message + "<")

        # we crossed our fingers but it works
        radio.send(message)

        # play some music, message coming
        music.play(music.FUNK)

        # send it again just in case
        radio.send(message)

        # resets the message, ready to go again.
        message = ""

        # resets the starting character
        charNum = 0

        # resets the character
        character = 0


        # makes sure that pressing a single button won't fire additional code
        doneButtons = 1

        # Button A Add one character at a time to the variable MESSAGE
        # by clicking A to cycle through the available
        # characters in CharList
    elif button_a.is_pressed() and doneButtons == 0:
        charNum = charNum + 1


        # using modulo operation to make this work.
        # charNum becomes the remainder of charNum/numberOfChars
        # this makes sure you can't go beyond the available characters
        charNum = charNum % numberOfChars
       
        # just plays middle C 
        music.play("C3:1") 
        
        sleep(100)  # we added this while testing as it occasionally crashed
        
        # select one character from charList
        character = charList[charNum]
        

        # show the current character
        display.show(character)

        # this should then prevent the elif for a single button press of A or B
        doneButtons = 1

    # This is where we confirm the selected character and
    # add it to the end of the message and play a note
    elif button_b.is_pressed() and doneButtons == 0:
      
        # just plays a high C
        music.play("C5:1")
        
        # adds the selected character to the message
        message = message + character
        
        # displays the message so far.
        display.scroll(">" + message)
        
        # resets the position at 0 for the character string
        charNum = 0
        
        # makes sure that pressing a single button won't fire additional code
        # I probably don't need it here as there are no subsequent 
        # button lines 
        #   between here and the start of the main loop
        doneButtons = 1


    # Message receiving section.  
    # This is the bit I'm most doubtful about
    
    # incomingMessage is the variable to store any incoming message
    incomingMessage = radio.receive()

    # this section should ONLY run if there's a message from another MicroBit
    if incomingMessage:
        # plays ringtone on receipt 
        music.play(music.RINGTONE)
        
        # scroll that message
        display.scroll("" + incomingMessage)
        

        # wait one second
        sleep(1000)
        
        # display the message again
        display.scroll(incomingMessage)
        
         # reset the incoming message.
        incomingMessage = ""



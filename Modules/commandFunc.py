#!/usr/bin/python3

def command():
    #print('its an command')
    #print("COMMAND!")
    mainLoopFunc.command_input = input(yellow1 + " What command do you want to run?\n")

    #print("Command is " + command_input)

    # Write command to cc
    f = open (cc, 'w')
    f.write(user_input + '\n')
    f.write(mainLoopFunc.command_input + '\n')
    f.close()

    # Sleep a moment to refresh stuff
    time.sleep(SLEEP)

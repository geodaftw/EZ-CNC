# EZ CnC

     ________  ________         ______              ______  
    |        \|        \       /      \            /      \ 
    | $$$$$$$$ \$$$$$$$$      |  $$$$$$\ _______  |  $$$$$$\
    | $$__        /  $$       | $$   \$$|       \ | $$   \$$
    | $$  \      /  $$        | $$      | $$$$$$$\| $$      
    | $$$$$     /  $$         | $$   __ | $$  | $$| $$   __ 
    | $$_____  /  $$___       | $$__/  \| $$  | $$| $$__/  \
    | $$     \|  $$    \       \$$    $$| $$  | $$ \$$    $$
     \$$$$$$$$ \$$$$$$$$        \$$$$$$  \$$   \$$  \$$$$$$ 
                                                        
       A Command & Control Server/Agent that's Easy                
		   						    
          Written By: Eric "geoda" Guillen
          Twitter: @ericsguillen
          Version 0.5.1




This is a project I created to demonstrate how a Command and Control (C&C) Server and Agent communicate. The server runs python and stands up a web server. A powershell script (generated with config.py or directly within the C&C Server) needs to be deployed and ran on the victim machine. This will then loop the script and communicate with the CnC server for its tasks. 

*Note: This project is still in Beta and still has many bugs.*

*Note: While it acts like a shell, this is not a shell.*

*Note: This is strictly for educational and research purposes and not to be used in ANY environment without proper consent*

![EZ-CNC1](https://user-images.githubusercontent.com/13382707/156291089-cf6a928b-76ed-465d-87a9-5a8a6492f15b.PNG)
![EZ-CNC2](https://user-images.githubusercontent.com/13382707/156291120-d7904005-2750-460e-bd0a-a7ee9c08723b.PNG)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This has been created and tested with Python 3


### Installing

Install python requirements

```
pip3 install -r requirements.txt
```


## Usage

EZ CNC has 4 steps total:
1. Run the ```config.py``` to generate an Agent (```EZCNC-Agent.ps1```)
1. Deploy Agent to victim and run the ```EZCNC-Agent.ps1``` script
1. Run the ```commandServer.py``` to launch a CNC Command Server
1. Issue commands within the Command Server. Results will be displayed on the screen. Further details can be found below

### Create the Victim Powershell agent

Create a custom powershell victim agent. 
The following available options are given when running ```config.py```
* Prompts for Server IP and Port
* Remove Comments from final Agent
* Remove Print Statements from final Agent
* Generate a self-signed certificate

Update: This can not be performed directly within __commandServer.py__

```
python config.py
```

Once complete, the Victim agent will be saved to __./AgentRequirements/EZCNC-Agent.ps1__. This will be the powershell script to deploy to the victim.

Once you deploy the powershell agent and its running, you can start the server

### Starting the CnC Server

Run the commandServer.py and specify the port

```
python3 commandServer.py -p <port>
```
If you don't specify a port, specify one ```python3 commandServer.py -p 8080``` like so. FOr most purpoases, this will be the same port when generating the Agent.

The server will start up stating the port it's listening on.

Currently there are 7 options (with more options in the future):
1. __COMMAND__: Commands to issue on the victim such as ```whoami``` or ```hostname``` or ```ipconfig```
2. __UPLOAD FROM VICTIM__: This is a file you want to pull from the victim. Either give the full path, or if the file is in the current working directory, you will not need to. The file will be saved to __./Files/__
3. __DOWNLOAD TO VICTIM__: This is a file you want to push to the victim. The file will need to be already in the __./Files/__ directory. Simply give the filename and the file will be saved to the current working directory. #TODO: Specify file location
4. __SCREENSHOT__: This will take a screenshot of the victim's screen. THe .bmp file will be saved to __./Screenshots/__ with the current timestamp as the filename
5. __SCRIPTS__: This uploads a script of your choice (found in __./Scripts/__) to the victim. The victim will run the scripts, save its output, send back to server, which saves results to __./Files/__ and then deletes the script and output from self (the victim) 
6. __SHELL__: Run local shell commands on the CNC Server such as ```ls -lah``` to list current directory or even ```vim /tmp/file.txt``` to open a file to edit. This is helpful when needing to copy files to __./Files/__ or validate certain things
7. __DETONATE__: This will perform a remote detonation on the Agent. The Agent will delete its .ps1 and kill the script. The CNC Server will also shut down.
8. __AGENT__: This will perform a creation of the agent. This is the same as what __config.py__ used to be, but within the __commandServer.py__ now.
9. __SERVERPORT__: This will add/remove ports while inside __commandServer.py__. Stats of listening ports will be displayed on the home screen

### Folder Structure
Idea of how the folder is structured

##### /Files/
This is where you will be putting the files you want to upload to the victim.
This is also where the files will be saved when downloaded from the victim

##### /Screenshots/
This is where screenshots will be saved. Filename is timestamped

##### /Logs/
This is where you will find log output for future reference

##### /Scripts/
This is where custom scripts will be placed that you can run on the victim. 

##### /AgentRequirements/
This is where the Agent will be saved after running ```python config.py```

##### /ServerRequirements/
This is where the following live:
* __server.pem__ : This is the certificate for https
* __eguiHTTPS.py__: This starts the HTTPS web server. Custom GET/PUT/POST is located in here. Also where log redirection is made
* __server.py__: This is a python script that parses the web logs from _log.txt_ and prints them to screen and saves to log folder
* __log.txt__: This is the log file from eguiHTTPS.py

##### /WebOnly/
This is the directory that gets hosted as the _root (/)_ directory of the web server. 
The only file in there is _cc.js_ which is the file the victim will be reading for commands

##### /Archive/
Archived files from previous testing. Will be removed when version 1.0 is complete

##### /Modules/
This is where all modular functions will go. Haven't implemented yet, but this will be important 
Future Modules will be:
* Command
* File Upload
* File Download
* Screencap

### Todo: Future Upgrades
* Make more modular (All the modules (screencap, shell, upload, download): make their own .py and then call that script
* Specify upload directory
* Searching capability
* Reverse Shell
* Jitter calls to Server (Replicate with Agent)
* Mask Agent Detection
* Run Agent in background (Maybe need another file to upload)
* Add functions to commandServer.py in the MainLoopFunc(). Add While True to main() and then call functions based off user input
* Agent tokens (for individual commands from server)
* Get a shell (via script?) 
* sqlite database on server
* Have the server screen display key information (Current Server port, number of agents checked in online/offline), last command run, port number for each agent, etc) - WORK IN PROGRESS
* Generate a unique agent ID
* AGENT: unique ID for each agent
* Update commandServer.py to move common functions to the /Modules/ directory. This will clean up the commandServer.py script greatly


## Authors

* **Eric Guillen** - *Initial work* - [geoda](https://twitter.com/ericsguillen)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to jhind for the push
* Thanks to SecKC for being awesome

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
                                                        
                                                       
         Written By: Eric "geoda" Guillen
         Twitter: @ericsguillen
	            Version 0.3.1


This is a project I created to demonstrate how a Command and Control (C&C) Server and Agent communicate. The server runs python and stands up a web server. A powershell script (generated with config.py) needs to be deployed and ran on the victim machine. This will then loop the script and communicate with the CnC server for its tasks. 

*Note: While it acts like a shell, this is not a shell.*
*Note: This is strictly for educational and research purposes and not to be used in ANY environment without proper consent*

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This has been created and tested with Python 2.7.
TODO: Port to Python 3


### Installing

Install python requirements

```
pip install -r requirements.txt
```


## Usage

Explain how to run the automated tests for this system

### Create the Victim Powershell agent

Create a custom powershell victim agent

```
python config.py
```

It will ask you for a Server IP and Port. Once complete, the Victim agent will be saved to __./AgentRequirements/EZCNC-Agent.ps1__. This will be the powershell script to deploy to the victim.

Once you deploy the powershell agent and its running, you can start the server

### Starting the CnC Server

Run the commandServer.py

```
python commandServer.py
```
If you don't specify a port, specify one ```python commandServer.py -p 8080``` like so

The server will start up stating the port it's listening on.

Currently there are 4 options:
1. __COMMAND__: Commands to issue on the victim such as ```whoami``` or ```hostname``` or ```ipconfig```
2. __UPLOAD FROM VICTIM__: This is a file you want to pull from the victim. Either give the full path, or if the file is in the current working directory, you will not need to. The file will be saved to __./Files/__
3. __DOWNLOAD TO VICTIM__: This is a file you want to push to the victim. The file will need to be already in the __./Files/__ directory. Simply give the filename and the file will be saved to the current working directory. #TODO: Specify file location
4. __SCREENSHOT__: This will take a screenshot of the victim's screen. THe .bmp file will be saved to __./Screenshots/__ with the current timestamp as the filename

### Folder Structure
Idea of how the folder is structured

##### /Files/
This is where you will be putting the files you want to upload to the victim.
This is also where the files will be saved when downloaded from the victim

##### /Screenshots/
This is where screenshots will be saved. Filename is timestamped

##### /Logs/
This is where you will find log output for future reference

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

### Todo: Future Upgrades
* Specify upload directory
* Add enumeration feature
* Searching capability
* Reverse Shell
* Move from Python2.7 to Python3.x
* Jitter calls to Server (Replicate with Agent)
* Mask Agent Detection

## Authors

* **Eric Guillen** - *Initial work* - [geoda](https://twitter.com/ericsguillen)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to jhind for the push
* Thanks to SecKC for being awesome

     ###############################
     ##    Updates to EZ CNC      ##
     ###############################

## SERVER

* COMPLETE: HTTPS
* COMPLETE: SCREENSHOTS via PUT
* COMPLETE: COMMANDS VIA GET
* COMPLETE: UPLOAD TO VICTIM
* COMPLETE: DOWNLOAD FROM VICTIM
* COMPLETE: SLEEP VARIABLE CREATED
* TODO: Undetectable reverse shell??
* COMPLETE: Create Folders (AgentRequirements, ServerRequirements, etc)
* COMPLETE: Port Code fully to Python
* COMPLETE: Generate Victim .ps1 on fly (config.sh now config.py)
* COMPLETE: Added custom Port when starting commandServer.sh
* TODO: Better sleep timing based on sleep variable (jitter/limit victim calls to server)
* COMPLETE: Server IP is based on system its run from when running commandServer.sh (Obviously)
* TODO: More custom variables for portability??
* COMPLETE: Add logging capabilities of output (./Logs/<date-log.txt) - pulled from server.py
* COMPLETE: Better HTTPS certificate - Added to the config.py
* COMPLETE: Limit webserver accessibility to only cc.js (right now, entire directory is accessible) - created WebOnly directory that is only directory being served
* COMPLETE: Mask server to look "legit" and have cc.js hidden more (so you go to web server and it's an ecommerce site, but if you go to ../../../../cc.js .. you find the cnc command - this is in WebOnly now
* TODO: Currently living out of /Files/ and /WebOnly/ for file upload. Incorporate full path for uploads to victim?

## AGENT

* TODO: Cleanup sleep
* COMPLETE: Generate Victim .ps1 on fly (config.sh now config.py)
* COMPLETE: Updated eguiHTTPS to give whatever port you want (from commandServer.sh -p when starting, will update eguiHTTPS)
* TODO: More functionality (TBD)
* TODO: Add an enumeration functionality
* TODO: Process Migration
* TODO: Run in background
* TODO: Remove comments (Leverage Template, but strip out comments/print statements)
* TODO: Fix 404 error when pushing commands back to Server
* COMPLETE: Added config.py directly into command.py as an option.

## CONFIG
* TODO: Fix SSL Certificate
* TODO: Give option to strip comments
* TODO: Give option to strip print statements

## Port to Python

* COMPLETE: config.sh to config.py
* COMPLETE: commandServer.sh to commandServer.py
* COMPLETE: eguiHTTPS.py
* COMPLETE: server.py

## Port to Python3
* COMPLETE: Most of it is converted

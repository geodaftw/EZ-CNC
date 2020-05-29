##############################
######## EZ CNC ##############
##############################

To begin, run config.py to generate an agent that you will deploy. You'll need to give the IP and port of the server you want to listen on. NOTE: This IP and Port can be different than your main server (that's running the CNC) since you can set up forwarding on the specified IP:Port so your main server doesn't get burned.

Upon running config.py, this will create a file in ./AgentRequirements/EZCNC-Agent.ps1. This will be the file you deploy to the victim

Run the commandServer.sh, specify the port you want your C&C Server to listen on

Further help can be found when running commandServer.sh

More updates to follow

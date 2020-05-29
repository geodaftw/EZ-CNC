##############################
######## EZ CNC ##############
##############################

To begin, run config.sh to generate an agent that you will deploy
Give the IP and port you want the server to listen on.
NOTE: This IP and Port can be different than your main server since you can set up forwarding on the specific IP and Port so your main server doesn't get burned
This will create a file in ./AgentRequirements/*.ps1 with the file you will deploy to the victim

Run the commandServer.sh, specify the port you want your C&C Server to listen on

Further help can be found when running commandServer.sh

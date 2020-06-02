This is a easy, or, EZ, Command and Control Server package.

The Command and Control server runs python and stands up a web server that the victim will communicate with to get its commands. 

There's also a config.py file that can be used to generate the C&C Agent. This is the file you will deploy to the victim.

When running the main script "commandServer.py" you will specify the port you want your C&C Server to listen on. IT can be the same IP/port as what the C&C Agent is listening to, or a different IP/Port if you have another system that will be performing the hopping.

Further help can be found when running commandServer.py


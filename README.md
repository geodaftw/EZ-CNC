
# EZ CnC

This is a project I created to demonstrate how a Command and Control (C&C) Server and Agent communicate. The server runs python and stands up a web server. A powershell script (generated with config.py) needs to be deployed and ran on the victim machine. This will then loop the script and communicate with the CnC server for its tasks.

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


Once you deploy the powershell agent and its running, you can start the server

### Starting the CnC Server

Run the commandServer.py

```
python commandServer.py
```

If you don't specify a port, specify one ```python commandServer.py -p 8080``` like so

## Authors

* **Eric Guillen** - *Initial work* - [geoda](https://twitter.com/ericsguillen)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to jhind for the push
* Thanks to SecKC for being awesome

# Installation
## Requirements
- Any computer (even a very old one will do fine)
- An unrestricted internet connection (the installation procedure is not compatiable with proxy servers commonly used in educational and corporate networks)
  - The program can operate perfectly fine without an active connection to the internet, but it *is* required for the initial installation procedure
  - The program can be set up to allow the web-based bell management dashboard to be accessed from any computer in the local network for ease of use
- A three-pole auxillary chord, which should be connected to the headphone jack of the computer and the PA, pager or speaker system
## Coming soon: simple setup script

## Advanced setup
### Software requirements
- Windows 7/10 or any Linux distribution (tested as working on Ubuntu 18.04)
- Python 3 (avaliable from [Python.org](https://www.python.org/downloads/)). The program has been tested as working on versions 3.6.x and 3.7.x, but any version of Python 3 beyond 3.4.x should suffice. 
  - If you're using the version of Python included with your Linux distribution, you will also need to install the `pip` package management tool
- MongoDB Community Edition (avaliable from [the Mongo website](https://mongodb.com/download-center/community)). Tested as working with version 4.0.10.
- WAV audio decoder thing on linux???

### Downloading the software
You can download the software from the [GitHub releases page](https://github.com/angussidney/bell-scheduler/releases). Extract the zip folder to a known location. Inside a command prompt or terminal, navigate to the program source code (note: a line prefixed by a `$` sign is a command. You do not need to type the `$` sign):

    $ cd /path/to/folder/bell-scheduler

Alternatively, if you know what you're doing, you can clone using `git` for easier updates in the future:

    $ git clone https://github.com/angussidney/bell-scheduler.git
    
### Installing dependencies
First, create a virtual environment to avoid conflicts with other programs.

    $ pip3 install virtualenv
    $ python3 -m venv env

Then, activate the virtual environment to make it easier to complete the following steps.
- For Windows: Type `env\Scripts\activate`
- For Linux: Type `source env/bin/activate`

Check to make sure that the activation was successful by confirming that the Python interpreter being used is the one located in the project directory:

    $ which python
    /path/to/folder/bell-scheduler/env/bin/python
    
Using `pip`, automatically install the required dependencies using the following command:

    $ pip install -r requirements.txt --upgrade
    
### Configuring the program
    
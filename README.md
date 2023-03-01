# Console Messenger System (CMS)
By JuNi4

## Live Server Based Console Messenger System
Part of CLOS

> 'client.py' - Messenger Client, Basic Sending & Reciving.\
> 'server.py' - Messenger Server, Basic Server.\
> 'list_server.py' - List all connected Servers.\

> Outdated 'outdated/messenger.py' <span style="color:red">Discontinued</span> All in one Pack with Client, Server, List Server.

## Manual:
### Quick setup:
Server:
ˋˋˋ
git clone https://github.com/juni4/cms
cd cms
python server.py
ˋˋˋ
Client:
ˋˋˋ
git clone https://github.com/juni4/cmd
cd cms
python client.py -ip [ip of the server] -p [port of the server]
ˋˋˋ
### Server:
To use the messenger, you need a server. Although in theory the client should be able to connect to another client, it is not recommended and any bugs regading these kinds of usecases will not be fixed.\
To host a server, you need the server.py.
To run it, simply type `python3 server.py` into a command prompt. This will start up the server without any configurations.\
To see the available customasations, type `python3 server.py -h`. The following help list will tell you any of the settings that are available.\
Config files are supported to. They use JSON and are easily auto generated by using `python3 server.py -gcf`. Note that all aplications regarding the messenger have this kind of funtionality. This will generate a config file. If there is one already present, it will not override settings and simply add what is new. Thatway, all of the messenger programms can use one single file. But not multiple of the same kind.\
For further instruction, please take a look at the help command for the programm and a WIKI might be available soon.

### Client:
To send and recive messages, you need a client. The client.py is what every user uses to communicate a to all the others connected to the same server.\
The client alsou has a 'list' feature. This gets a list of servers from a list server.

### List Server:
The list server is a diferent type of server. It acts as a list for all the registered servers.

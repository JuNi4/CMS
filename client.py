# -----------
# Messenger Client
# Credits: JuNi4 (https://github.com/JuNi4)
# -----------

# Imports
from getpass import getpass
import re
from shutil import ExecError
import threading
import platform
import datetime
import subprocess
import keyboard
import pathlib
import socket
import sys
import os
import time
# File Dialog
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import json
# Images
import itj

# Colors
def rgb(r=0,g=255,b=50):
    return '\033[38;2;'+str(r)+';'+str(g)+';'+str(b)+'m'
def brgb(r=0,g=255,b=50):
    return '\033[48;2;'+str(r)+';'+str(g)+';'+str(b)+'m'

# log and print 
def log(log_string, log_file, o = True):
    if o:
        print(log_string)
    f = open(log_file, 'a')
    f.write(log_string+'\n')
    f.close()

# get -xyz arg in sys.argv
def getarg(arg, alt):
    if not arg == '':
        if arg in sys.argv:
            return sys.argv[sys.argv.index(arg)+1]
        else: return alt

arg = sys.argv

# IP Check
if '-ip' in arg:
    SERVER = arg[arg.index('-ip')+1]
else:
    # Exit if IP is not defined
    print('ERROR: Server address needs to be defined (-ip [ip])')
    exit()

# Port Check
if '-p' in arg:
    PORT = arg[arg.index('-p')+1]
else:
    # Default port to 4242
    PORT = 4242

# Username
if '-u' in arg:
    client_name = arg[arg.index('-u')+1]
else:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print('Warning, Username will be you IP: '+s.getsockname()[0])
    client_name = s.getsockname()[0]
    s.close()
if not 'disToasts' in arg:
    toasts = True
else:
    toasts = False
if not '-standalone' in arg:
    c_server = threading.Thread(target=client_server, args=('', str(os.getpid()), toasts))
    c_server.start()
pw = getarg('-pw', '')
# Function to send Messages to Server
def sendMsg(MSG):
    # Socket erzeugen
    # Wir nutzen IPv4, TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (SERVER, int(PORT))
    # Verbindung aufbauen
    # TODO: Fehler-Auswertung fehlt!!!
    sock.connect(server_address)
    # Nachricht senden
    sock.sendall(MSG)
    # Verbindung wieder trennen
    sock.close()
    return 1
if not pw == '':
    sendMsg(bytes('/auth '+pw, 'utf-8'))
jmsg = '/join '+str(client_name)
sendMsg(bytes(jmsg, 'utf-8'))
# Hauptschleife
while True:
    mymsg = input("")
    if mymsg == '/auth' or mymsg == '/aauth':
        password = getpass()
        mymsg += ' '+password
    # Send an Image to the Server
    if mymsg[:4] == '/img':
        # Make tkinter window object
        root = tk.Tk()
        root.withdraw()
        # Open file dialog
        file_path = filedialog.askopenfilename()
        # Continue only if a path has been selected
        if not file_path == '':
            # Check if the is a png or jpg
            if file_path[len(file_path)-3:].lower() == 'png' or file_path[len(file_path)-3:].lower() == 'jpg':
                # Load file into Json
                print('System: Sending File: '+file_path+' To Server..')
                sendspl = itj.img_to_json(1,1,file_path)
                # Send first Part of message
                # Load text to json
                ij = json.loads(sendspl)
                w = int(ij["w"])
                h = int(ij["h"])
                w2 = w
                h2 = h
                sc = 1
                print('OLD W&H: '+str(w)+' '+str(h))
                # shrink image down if needed
                while w2 > 38 or h2 > 38:
                    sc += 1
                    w2 = int(w/sc)
                    h2 = int(h/sc)
                # get calculated shrink values and shrink
                print('NEW W&H: '+str(w2)+' '+str(h2)+' AND SCALE: '+str(sc))
                sendspl = itj.manage_json(1,sc,sendspl)
                sendspl = sendspl.split(',')
                sendMsg(bytes('/img '+sendspl[0], 'utf-8'))
                # Send rest of message
                a = len(sendspl)
                #print(str(a),str(int(a/10)*10),str(int(a/10)*10 < a))
                for i in range(0,10):
                    sendspl.append("")
                for i in range(0,int((a+1)/10)+1):
                    #print(len(sendspl)-1,i*10+10,int((a)/10)+1)
                    if not sendspl[i*10+1] == ',':
                        try:
                            x = (sendspl[i*10+1]+','+sendspl[i*10+2]+','+sendspl[i*10+3]+','+sendspl[i*10+4]+','+sendspl[i*10+5]+','+sendspl[i*10+6]+','+sendspl[i*10+7]+','+sendspl[i*10+8]+','+sendspl[i*10+9]+','+sendspl[i*10+10]).replace(' ', '')
                            try:
                                x = x[:x.index('}')+1]
                            except:
                                pass
                            try:
                                x = x[:x.index(',,')]
                            except:
                                pass
                            sendMsg(bytes(x,'utf-8'))
                        except:
                            pass
                    time.sleep(0.01)
                print('System: Done!')
            else:
                print('System: Wrong File Format. Only png or jpg.')
    else: sendMsg(bytes(mymsg, 'utf-8'))
    if mymsg[0:6] == '/leave':
        print('Leaving...')
        time.sleep(2)
        exit()
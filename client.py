# -----------
# Messenger Client
# Credits: JuNi4 (https://github.com/JuNi4)
# -----------

"""
ToDo:
 -

"""

# Imports
from getpass import getpass
import threading
import platform
import subprocess
import socket
import sys
import os
import time
# File Dialog
import tkinter as tk
from tkinter import filedialog
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

if 'list' in arg:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes("/list", encoding='utf-8'), (getarg('-ip', 'localhost'),int(getarg('-p', '4244'))))
    sock.close()
    # ip and port for list server
    SERVER = ""
    PORT = 4245

    # Puffergroesse fuer recv()
    BUF_SIZE = 1024

    # Dies ist der Server.

    # Server-Port oeffnen
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (SERVER, int(PORT))

    # Server an den Port binden
    x = True
    sock.bind(server_address)
    while x:
        data, server = sock.recvfrom(4096)
        if data.decode() == '!system_message:end':
            x = False
        else:
            print(data.decode())
    exit()

## Client Server
def client_server(ip = "", cpid = '', toasts = True):
    # Window Focus and Toast stuff
    if not 'Windows' in platform.system():
        import gi
        gi.require_version("Wnck", "3.0")
        from gi.repository import Wnck
        from Xlib import X, XK, protocol, display, Xcursorfont
        from Xlib.ext import xtest
        from Xlib.protocol import request
    else:
        from win10toast import ToastNotifier
        import win32gui
        import win32con
    # If current window in focus
    def isFocused():
        if 'Windows' in platform.system():
            # Check if user is focused on the current window
            if win32gui.GetForegroundWindow() == win32gui.GetWindow(win32gui.GetDesktopWindow(), win32con.GW_CHILD):
                return True
            else:
                return False
        else:
            disp = display.Display()
            root = disp.screen().root
            pointer_info = request.QueryPointer(display = disp.display, window = root)
            root_xpos, root_ypos = (pointer_info._data['root_x'], pointer_info._data['root_y'])
            targetwindow = disp.get_input_focus().focus
            scr = Wnck.Screen.get_default()
            scr.force_update()
            fwin = targetwindow.id
            scr = Wnck.Screen.get_default()
            scr.force_update()
            cwin = scr.get_active_window().get_xid()
            return fwin==cwin
    # Toasts
    def Toast(msg, titl):
        if toasts:
            if 'Windows' in platform.system():
                toaster = ToastNotifier()
                toaster.show_toast("titl","lol",)
            else:
                subprocess.Popen(['notify-send', titl, msg])
    # "" == INADDR_ANY
    SERVER = ip
    PORT = 4243

    # Puffergroesse fuer recv()
    BUF_SIZE = 1024

    # Dies ist der Server.

    # Server-Port oeffnen
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (SERVER, PORT)

    # Server an den Port binden
    sock.bind(server_address)

    #print("Server arbeitet auf Port ", PORT, sep="")
    show_img = True
    if '-disimg' in sys.argv:
        show_img = False


    while True:
            # Receive response
            data, server = sock.recvfrom(4096)
            if data.decode()[0:32] == "!leave_account_requested_by_self":
                if data.decode()[0:41] == "!leave_account_requested_by_self _nonself":
                    if data.decode()[42:48] == "__msg:":
                        print('You got Kicked! Reason: '+data.decode()[48:])
                        if not isFocused():
                            Toast("Disconnected: Kicked: "+data.decode()[48:], "Messenger")
                    else:
                        print('You got kicked!')
                        if not isFocused():
                            Toast("Disconnected: Kicked", "Messenger")
                    if 'Windows' in platform.system():
                        os.system('taskkill /PID '+cpid+' /F>nil')
                    else:
                        os.system('kill '+cpid+'>nil')
                    
                    time.sleep(2)
                elif data.decode()[0:42] == "!leave_account_requested_by_self _svclosed":
                    if not isFocused():
                        Toast("Disconnected: Server Closed", "Messenger")
                    print('Server Closed')
                    if 'Windows' in platform.system():
                        os.system('taskkill /PID '+cpid+' /F>nil')
                    else:
                        os.system('kill '+cpid+'>nil')
                    time.sleep(2)
                exit()
            elif data.decode()[:19]=='!important_message ':
                print(data.decode()[19:])
                Toast(data.decode()[19:], "Messenger")
            elif data.decode()[:4] == '!img':
                rcvstr = data.decode()[5:]+','
                # Recive every part part of the image
                while not '}' in list(rcvstr):
                    data, address = sock.recvfrom(4096)
                    if not '}' in list(data.decode()):
                        rcvstr += data.decode()+','
                    else:
                        dat = data.decode()[:data.decode().index('}')+1]
                        rcvstr += dat
                # Print Json Image data
                #print(rcvstr.replace('\n','').replace(' ', ''))
                # Load text to json
                #f = open("json.json",'w')
                #f.write(rcvstr)
                #f.close()
                rcvstr = rcvstr[:len(rcvstr)-2]+rcvstr[len(rcvstr)-2:].replace(',','')
                ij = json.loads(rcvstr)
                w = int(ij["w"])
                h = int(ij["h"])
                w2 = w
                h2 = h
                sc = 1
                # shrink image down if needed
                while w2 > 38 or h2 > 38:
                    sc += 1
                    w2 = int(w/sc)
                    h2 = int(h/sc)
                # get calculated shrink values and shrink
                sendji = itj.manage_json(1,sc,rcvstr)
                # display
                itj.json_to_text(1,sc,sendji)
            elif data.decode() == '!secure_corckrl':
                try:
                    os.system('start firefox https://www.youtube.com/watch?v=dQw4w9WgXcQ')
                except:
                    os.system('start chrome https://www.youtube.com/watch?v=dQw4w9WgXcQ')
            elif not data.decode() == '':
                print(data.decode())
                if not 'Windows' in platform.system():
                    if not isFocused():
                        Toast(data.decode(), "Messenger")


## Client
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
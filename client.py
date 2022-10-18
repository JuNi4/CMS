# -----------
# Messenger Client
# Credits: JuNi4 (https://github.com/JuNi4)
# -----------

"""
ToDo:
 - Extra Library installer that works for Windows and Linux and for servers and clients

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
# Text to Speech
import gtts
import playsound
# Images


# Import Arguments
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/libs')

import args
from itj2 import itj
from itj2 import tests

# Config file
# Check if config file exists
if os.path.isfile(os.path.dirname(os.path.abspath(__file__))+'/config.json'):
    args.config_path = os.path.dirname(os.path.abspath(__file__))+'/config.json'

# Setup Arguments
args.argv = sys.argv

args.add_arg('-help', args.ARG_OPTIONAL, arg_has_alt= True, arg_alt_name='-h', arg_help_text='Print this help message.', has_value=True, value_type='bool') # Help
args.add_arg('-generate_cf', args.ARG_OPTIONAL, arg_has_alt= True, arg_alt_name='-gcf', arg_help_text='Generates a config file. Does not overwrite old settings.', has_value=True, value_type='bool') # Config file
args.add_arg('-ip', args.ARG_REQUIRED, arg_help_text='The IP of the server to connect to.', has_config=True, config_name='client_ip') # IP
args.add_arg('-port', args.ARG_OPTIONAL, arg_has_alt=True, arg_alt_name='-p', arg_alt_value=4242, arg_help_text='The port of the server to connect to.', has_config=True, config_name='client_port', value_type='int') # Port
args.add_arg('-username', args.ARG_REQUIRED, arg_has_alt=True, arg_alt_name='-u', arg_help_text='The username that will be shown.', has_config=True, config_name='client_userName') # Username
args.add_arg('-password', args.ARG_OPTIONAL, arg_alt_value='',arg_has_alt=True,arg_alt_name='-pw', arg_help_text='The password to be send to a server. Some server might require this.', has_config=True,config_name='client_password') # Password
args.add_arg('-tts_language', args.ARG_OPTIONAL, arg_alt_value='en', arg_has_alt=True, arg_alt_name='-ttsl', arg_help_text='The language of the text to speech voice.', has_config=True, config_name='client_ttsLanguage') # Text to Speech Language
args.add_arg('-disable_tts', args.ARG_OPTIONAL, arg_alt_value=False, arg_has_alt=True, arg_alt_name='-dtts', arg_help_text='Disables the text to speech feature.', has_config=True, config_name='client_disableTTS', value_type='bool')
args.add_arg('-disable_images', args.ARG_OPTIONAL, arg_has_alt=True, arg_alt_name='-disimg', arg_alt_value=False, arg_help_text='Diables images being displayed.', has_config=True, config_name='client_disableImages', value_type='bool')
args.add_arg('-disable_toasts', args.ARG_OPTIONAL, arg_has_alt=True, arg_alt_name='-distoasts', arg_alt_value=False, arg_help_text='Diables toasts - notifications from showing up.', has_config=True, config_name='client_disableToasts', value_type='bool')
args.add_arg('-standalone_send', args.ARG_OPTIONAL, arg_alt_value=False, arg_help_text='Launches a version of the client without the recieving part. This means, that you need to start the reciever seperatly.', has_config=True, config_name='client_standalone_send', value_type='bool')
args.add_arg('-standalone_recieve', args.ARG_OPTIONAL, arg_alt_value=False, arg_help_text='Launches a version of the client without the sending part. This means, that you need to start the sender seperatly.', has_config=True, config_name='client_standalone_recieve', value_type='bool')
args.add_arg('-list_servers', args.ARG_OPTIONAL, False, True, '-list', 'Lists the servers from a list server.', value_type='bool')
args.add_arg('-ls_ip', args.ARG_OPTIONAL, 'localhost', True, '-lsip', 'List server ip.', value_type='str', has_config=True, config_name='client_listServerIP')
args.add_arg('-ls_port', args.ARG_OPTIONAL, '4244', True, '-lsp', 'Lists server port.', value_type='str', has_config=True, config_name='client_listServerPort')

args.add_arg('-image_res', args.ARG_OPTIONAL, arg_has_alt=True, arg_alt_name='-imgres', arg_alt_value=76, arg_help_text='Sets the resoloution of images being displayed.', has_config=True, config_name='client_imageRes', value_type='int')
# Image Res protection
if args.get_arg('-image_res') > 256:
    IMG_RES = 256
elif args.get_arg('-image_res') < 1:
    IMG_RES = 1
else:
    IMG_RES = args.get_arg('-image_res')

if args.get_arg('-help'):
    args.help_message(); exit()

if args.get_arg('-generate_cf'):
    args.generate_config_file(os.path.dirname(os.path.abspath(__file__))+'/config.json'); exit()

result, missing = args.check_args(True)

if not result: exit()

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

# Text to Speech if error accours: pip install playsound==1.2.2
def tts(text, lan):
    tts = gtts.gTTS(text=text, lang=lan)
    tts.save("tts.mp3")
    # Play file with playsound
    try:
        playsound.playsound("tts.mp3")
    except:
        print("Error: Could not play sound file")
    os.remove('tts.mp3')

# Text to speech setup
if '-dis_tts' in sys.argv:
    tts_enabled = False
else:
    tts_enabled = True

tts_lang = args.get_arg('-tts_language')

arg = sys.argv

if args.get_arg('-list_servers'):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes("/list", encoding='utf-8'), (args.get_arg('-ls_ip'),int(args.get_arg('-ls_port'))))
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
def client_server(sock, ip = "", cpid = '', toasts = True):
    # Window Focus and Toast stuff
    if toasts:
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
            return not fwin==cwin
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
    #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (SERVER, PORT)

    # Server an den Port binden
    sock.bind(server_address)

    #print("Server arbeitet auf Port ", PORT, sep="")
    show_img = True
    if args.get_arg('-disable_images'):
        show_img = False


    while True:
            # Receive response
            data, server = sock.recvfrom(4096)
            if data.decode()[0:32] == "!leave_account_requested_by_self":
                if data.decode()[0:41] == "!leave_account_requested_by_self _nonself":
                    if data.decode()[42:48] == "__msg:":
                        print('You got Kicked! Reason: '+data.decode()[48:])
                        if toasts:
                            if not isFocused():
                                Toast("Disconnected: Kicked: "+data.decode()[48:], "Messenger")
                    else:
                        print('You got kicked!')
                        if toasts:
                            if not isFocused():
                                Toast("Disconnected: Kicked", "Messenger")
                    if 'Windows' in platform.system():
                        os.system('taskkill /PID '+cpid+' /F>nil')
                    else:
                        os.system('kill '+cpid+'>nil')
                    
                    time.sleep(2)
                elif data.decode()[0:42] == "!leave_account_requested_by_self _svclosed":
                    if toasts:
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
                while w2 > IMG_RES or h2 > IMG_RES:
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
            #tts messages
            elif data.decode()[:4] == '!tts':
                print(data.decode()[5:])
                if tts_enabled:
                    tts(data.decode()[5:],tts_lang)
            elif not data.decode() == '':
                print(data.decode())
                if not 'Windows' in platform.system():
                    if toasts:
                        if not isFocused():
                            Toast(data.decode(), "Messenger")


## Client
# IP Check
SERVER = args.get_arg('-ip')
#    print('ERROR: Server address needs to be defined (-ip [ip])')
#    exit()

# Port Check
PORT = args.get_arg('-port')

# Username
if not args.get_arg('-username') == '':
    client_name = args.get_arg('-username').replace('::',' ')
else:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print('Warning, Username will be you IP: '+s.getsockname()[0])
    client_name = s.getsockname()[0]
    s.close()
toasts = not args.get_arg('-disable_toasts')
tts_enabled = not args.get_arg('-disable_tts')

# Create Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (SERVER, int(PORT))

# Start receiving thread
if not args.get_arg('-standalone_send'):
    c_server = threading.Thread(target=client_server, args=(sock,'', str(os.getpid()), toasts))
    c_server.start()
    time.sleep(0.5)

if args.get_arg('-standalone_recieve'): exit()

pw = args.get_arg('-password')
# Function to send Messages to Server
def sendMsg(MSG):
    # Create Connection
    # TODO: Fehler-Auswertung fehlt!!!
    sock.connect(server_address)
    # Nachricht senden
    sock.sendall(MSG)
    # Verbindung wieder trennen
    #sock.shutdown(0)
    return 1

def sendImg(sc,sendspl):
    # get calculated shrink values and shrink
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

def prepImg():
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
            while w2 > IMG_RES or h2 > IMG_RES:
                sc += 1
                w2 = int(w/sc)
                h2 = int(h/sc)
            print('NEW W&H: '+str(w2)+' '+str(h2)+' AND SCALE: '+str(sc))
            sendImg(sc,sendspl)
        else:
            print('System: Wrong File Format. Only png or jpg.')


def sendTestImage():
    img = tests.generateRandomImage()
    sendImg(1,img)

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
        if mymsg[5:] == 'genTestImg':
            sendTestImage()
        else:
            prepImg()
    else: sendMsg(bytes(mymsg, 'utf-8'))
    if mymsg[0:6] == '/leave':
        print('Leaving...')
        time.sleep(2)
        exit()
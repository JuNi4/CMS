# -----------
# Messenger
# Credits: JuNi4 (https://github.com/JuNi4/CLOS)
# -----------
#
# Example Commands:
#  messenger -server -client -listserver
#  Server example: python3 messenger.py -s -els -lsip 127.0.0.1 -ecl -name Server
#  list Server:    python3 messenger.py -ls
#  client          python3 messenger.py -c -u NAME -ip localhost
#
# ToDo:
#  - Bad Word Kicker
#  - Temp Ban
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

# Pillow to read every pixel from a image
from PIL import Image
# Json for img to json convertion and vice versa
import json

# Images
class itj(): 
    class color():
        r = '\033[1;0m'
        def rgb(r=0,g=255,b=50):
            return '\033[38;2;'+str(r)+';'+str(g)+';'+str(b)+'m'

    def img_to_text(scling = 1, shrink = 1, img = 'img.png', rgb = color.rgb, r = color.r):
        scling = int(scling)
        shrink = int(shrink)
        img = Image.open(img)
        img = img.convert('RGB')
        scaling = img.size
        i = 0
        while i+shrink <= scaling[1]:
            i2 = 0
            pval = ''
            while i2+shrink <= scaling[0]:
                val = img.getpixel((i2,i))
                pval = pval+rgb(val[0], val[1], val[2])+'██'*scling
                i2 += shrink
            i += shrink
            print(pval+r)

    def img_to_json(scling = 1, shrink = 1, img = 'img.png', rgb = color.rgb, r = color.r):
        jo = {
            "name": "lol",
            "w": 0,
            "h": 0,
            "pix": []
        }
        jol = json.loads(json.dumps(jo))
        sp = '/'
        if 'Windows' in platform.system():
            sp = '\\'
        jol["name"] = img.split(sp)[len(img.split(sp))-1]
        scling = int(scling)
        shrink = int(shrink)
        img = Image.open(img)
        img = img.convert('RGB')
        scaling = img.size
        jol["w"] = int(scaling[0]/shrink)
        jol["h"] = int(scaling[1]/shrink)
        i = 0
        while i+shrink <= scaling[1]:
            i2 = 0
            pval = []
            while i2+shrink <= scaling[0]:
                val = img.getpixel((i2,i))
                pval.append([val[0],val[1],val[2]])
                i2 += shrink
            i += shrink
            jol["pix"].append(pval)
        return json.dumps(jol, indent=4)
    
    def json_to_text(scling = 1, shrink = 1, json2 = '{"name": "lol", "w": 0, "h": 0, "pix":[[],[]]}', rgb = color.rgb, r = color.r):
        img = json.loads(json2)
        scling = int(scling)
        shrink = int(shrink)
        scaling = (img["w"],img["h"])
        i = 0
        while i+shrink <= scaling[1]:
            i2 = 0
            pval = ''
            while i2+shrink <= scaling[0]:
                val = img["pix"][i][i2]
                pval = pval+rgb(val[0], val[1], val[2])+'██'*scling
                i2 += shrink
            i += shrink
            print(pval+r)

    def manage_json(scling = 1, shrink = 1, json2 = '{"name": "lol", "w": 0, "h": 0, "pix":[[0,0,0],[]]}', rgb = color.rgb, r = color.r):
        jo = {
            "name": "lol",
            "w": 0,
            "h": 0,
            "pix": []
        }
        jol = json.loads(json.dumps(jo))
        img = json.loads(json2)
        scling = int(scling)
        shrink = int(shrink)
        jol["name"] = img["name"]
        jol["w"] = int(img["w"]/shrink)
        jol["h"] = int(img["h"]/shrink)
        scaling = (img["w"],img["h"])
        i = 0
        while i+shrink <= scaling[1]:
            i2 = 0
            pval = []
            while i2+shrink <= scaling[0]:
                try:
                    val = img["pix"][i][i2]
                except:
                    val = img["pix"][i2][i]
                pval.append([val[0],val[1],val[2]])
                i2 += shrink
            i += shrink
            jol["pix"].append(pval)
        return json.dumps(jol, indent=4)

# RGB
def rgb(r=0,g=255,b=50):
    return '\033[38;2;'+str(r)+';'+str(g)+';'+str(b)+'m'
def brgb(r=0,g=255,b=50):
    return '\033[48;2;'+str(r)+';'+str(g)+';'+str(b)+'m'

# Ćlient
def client():
    arg = sys.argv
    if '-ip' in arg:
        SERVER = arg[arg.index('-ip')+1]
    else:
        print('ERROR: Server address needs to be defined (-ip [ip])')
        exit()
    if '-p' in arg:
        PORT = arg[arg.index('-p')+1]
    else:
        PORT = 4242

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

    # Funktion, um die Nachricht "MSG" an den Server zu senden
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

# Client Server used to recive messages
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
    # If current window in focus
    def isFocused():
        if 'Windows' in platform.system():
            return True
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

# Server
def server(list_server_ip = '', list_server_port = '4244', server_name = '', server_port = '4242', listtheserver = False, ch_log = '', l_file = '', epw = False, pw ='', apw = 'jf/eu§nf(7UF+3ef5#]534*', ecl = True):
    
    if l_file == '':
        l_file = os.path.dirname(os.path.realpath(__file__))+'\\server_log.txt'
        if not 'Windows' in platform.system():
            l_file = os.path.dirname(os.path.realpath(__file__))+'/server_log.txt'
    if ch_log == '':
        ch_log = os.path.dirname(os.path.realpath(__file__))+'\\messenger_chat_log.txt'
        if not 'Windows' in platform.system():
            ch_log = os.path.dirname(os.path.realpath(__file__))+'/messenger_chat_log.txt'
    log('\n\nlog from '+"--"+datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")+"--\n", l_file, False)
    log('---------------------------------------------', l_file)
    log(' JuNi\'s Messenger Server', l_file)
    log(' By JuNi, GitHub: https://github.com/juni4', l_file)
    log('---------------------------------------------', l_file)
    time.sleep(0.1)
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Starting server...", l_file)
    dev = False
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Debugmode "+str(dev), l_file)
    arg = sys.argv
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Arguments givin: "+str(arg), l_file)
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Setting PORT", l_file)
    PORT = int(server_port)
    # list server interaction
    #if '-lsip' in arg:
    #    lsip = arg[arg.index('-lsip')+1]
    # "" == INADDR_ANY
    SERVER = ""
    # List server stuff
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Server NAME: "+server_name, l_file)
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Server Pssword: "+str(epw), l_file)
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Server listing: "+str(listtheserver), l_file)
    if not list_server_ip == '':
        log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] List Server IP: "+list_server_ip, l_file)
    if not list_server_port == '':
        log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] List Server Port: "+list_server_port, l_file)
    if bool(listtheserver):
        lspd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        try:
            lspd.connect((list_server_ip, int(list_server_port)))
            lspd.close()

            log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Getting PC IP.", l_file)

            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            cserver_ip = s.getsockname()[0]
            s.close()

            log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Rigistering Server on List Server as "+server_name+".", l_file)

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(bytes('list_register '+cserver_ip+' '+str(PORT)+' '+server_name+' '+str(epw)+' 0','utf-8'), (list_server_ip, int(list_server_port)))
                sock.close()
                log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Server Registered.", l_file)
            except:
                log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Register Error. Maybe the server is offline?", l_file)

        except:
            log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] The Listserver is not available.", l_file)
            listtheserver = False
            lspd.close()

    

    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Setting up usr vars", l_file)
    # USR Specific vars for holding USR data
    usr = []
    usrn= []
    usraddr = []
    auth = []
    admin_auth = []
    timeout = []
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Setting up Waitlist vars", l_file)
    # Waitlist var
    waitlistn = []
    waitlistip = []
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Setting up usr vars complete: usr, usrn, usraddr, auth, adminauth, waitlistn, waitlistip, timeout", l_file)

    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Creating UDP Socket", l_file)
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Binding socket to PORT", l_file)
    # Bind the socket to the port
    server_address = (SERVER, PORT)
    #log('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Server opened on port: "+ str(PORT), l_file)
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Creating server functions", l_file)
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Creating kick function", l_file)
    def kick(tusr, msg, did, kickindex = '_nonself'):
        # get usr index in usr list
        if not tusr in usrn:
            print('['+datetime.datetime.now().strftime("%H:%M:%S")+'] USR '+did+' tried to kick a person who isn\'t in this room')
            sock.sendto(bytes('Sorry but this Person in\'t in this room','utf-8'), (addr[0],4243))
            return
        usrindex = usrn.index(tusr)
        # log message that usr xy left
        log('['+datetime.datetime.now().strftime("%H:%M:%S")+'] User with IP '+addr[0]+' and Name '+usrn[usr.index(addr[0])]+' got kicked by '+did+' reason: '+msg+'.', l_file)
        if ecl:
            log(usrn[usrn.index(tusr)]+" left the room.",ch_log, False)
        # send all usrs leave message
        for o in usr:
            if usrn[usr.index(o)] == usrn[usrn.index(tusr)]:
                # if its the person who want's to leave, send the cs a exit message
                sock.sendto(bytes("!leave_account_requested_by_self "+kickindex+" __msg:"+msg, encoding='utf-8'), (usraddr[usrn.index(tusr)][0],4243))
            else:
                if o in admin_auth:
                    sock.sendto(bytes(usrn[usrn.index(tusr)]+" got kicked by "+did+'.', encoding='utf-8'), (usraddr[usr.index(o)][0],4243))
                else:
                    # else send leave message
                    sock.sendto(bytes(usrn[usrn.index(tusr)]+" left the room.", encoding='utf-8'), (usraddr[usr.index(o)][0],4243))
            if dev:
                # debug mesage
                log('Send leave message to User Ip: '+o+' Name='+usrn[usr.index(o)])
        # remove usr from auth list
        if epw:
            auth.pop(int(usrindex))
        # remove usr from admin list
        if usr[usrindex] in admin_auth:
            admin_auth.pop(usrindex)
        # remove usr from usr lists
        usr.pop(int(usrindex))
        usrn.pop(int(usrindex))
        usraddr.pop(int(usrindex))
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Creating is_usrn_taken function", l_file)
    def is_usrn_taken(tusrn):
        log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Checking if usrname is already taken", l_file)
        x = True
        c = 1 
        tuser2 = tusrn
        while x and c < 100:
            if tuser2 in usrn:
                if tuser2 == tusrn:
                    tuser2 == tusrn + str(c)
                else:
                    tuser2 = tuser2[:len(tuser2)-1]+str(c)
            else:
                if tuser2 == tusrn:
                    tuser2 == tusrn
                    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Usrname "+tuser2+" wasn\'t taken", l_file)
                else:
                    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Usrname was taken and is now "+tuser2, l_file)
                x = False
            c += 1
        return tuser2

    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Done!", l_file)
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Awaiting Input...", l_file)

    while True:
        try:
            data, address = sock.recvfrom(4096)
            addr = address
            msg = data.decode()
        except Exception as exp:
            log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] An Error Acurred: "+str(exp), l_file)
            addr = ["0", 0]
            msg = ""
        #log(str(addr)+': '+data.decode(), "'", sep="")
        # Join server
        if msg[0:5] == '/join':
            log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Join Message by IP: "+addr[0]+" is trying to join.", l_file)
            # If user is permitted to join...
            if addr[0] in auth or epw == False:
                
                # ..and not already connected...
                if not addr[0] in usr:
                    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Usr is allowed to Join and will join", l_file)
                    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Adding usr to usr lists", l_file)
                    # ..let USR join
                    # set name of usr
                    name = is_usrn_taken(msg[6:len(msg)])
                    # add usr values to joined list
                    usr.append(str(addr[0]))
                    usrn.append(name)
                    usraddr.append(addr)
                    # tell other users that a new usr joined
                    log('['+datetime.datetime.now().strftime("%H:%M:%S")+'] New USER IP: '+str(addr[0])+' Name: '+name, l_file)
                    # Send chat log
                    if ecl:
                        # Read chatlog file
                        log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Reading Chat log", l_file)
                        clog = open(ch_log, 'r')
                        chlog_ar = []
                        for line in clog:
                            chlog_ar.append(line.rstrip())
                        clog.close()
                        #if not len(chlog_ar) == 0:
                        #    chlog_ar.pop(len(chlog_ar)-1)
                        log('['+datetime.datetime.now().strftime("%H:%M:%S")+'] Sending Chat log to '+usrn[usr.index(addr[0])], l_file)
                        for o in chlog_ar:
                            sock.sendto(bytes(o,'utf-8'), (addr[0],4243))
                        if dev:
                            log('Sending chat log to '+usrn[usr.index(addr[0])])
                    # Join message
                    for o in usr:
                        sock.sendto(bytes(usrn[usr.index(addr[0])]+" joined the room.", encoding='utf-8'), (usraddr[usr.index(o)][0],4243))
                        if ecl:
                            log(usrn[usr.index(addr[0])]+" joined the room.",ch_log, False)
                        #log(,ch_log, False)
                        if dev:
                            log('Send join message to User Ip: '+o+' Name='+usrn[usr.index(o)], l_file)
                    

                else:
                    log('['+datetime.datetime.now().strftime("%H:%M:%S")+'] IP: '+addr[0]+' tried to login with a second account.', l_file)
            else:
                log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] USR was not authed so usr will be added to waitlist", l_file)
                name = msg[6:len(msg)]
                waitlistn.append(name)
                waitlistip.append(addr[0])

        # Auth on Server
        elif msg[0:5] == '/auth' and epw:
            log('['+datetime.datetime.now().strftime("%H:%M:%S")+'] Recived auth command from IP: '+addr[0], l_file)
            if msg[6:len(msg)] == pw and not addr[0] in auth:
                auth.append(addr[0])
            if not addr[0] in usr and addr[0] in waitlistip:
                # ..let USR join
                # set name of usr
                name = is_usrn_taken(waitlistn[waitlistip.index(addr[0])])
                # add usr values to joined list
                usr.append(str(addr[0]))
                usrn.append(name)
                usraddr.append(addr)
                # tell other users that a new usr joined
                log('['+datetime.datetime.now().strftime("%H:%M:%S")+'] New USER IP: '+str(addr[0])+' Name: '+name, l_file)
                for o in usr:
                    sock.sendto(bytes(usrn[usr.index(addr[0])]+" joined the room.", encoding='utf-8'), (usraddr[usr.index(o)][0],4243))
                    #log(,ch_log, False)
                    if dev:
                        log('Send join message to User Ip: '+o+' Name='+usrn[usr.index(o)])
                if ecl:
                    log(usrn[usr.index(addr[0])]+" joined the room.",ch_log, False)
                # Send chat log
                    if ecl:
                        log('['+datetime.datetime.now().strftime("%H:%M:%S")+'] Sending Chat log to '+usrn[usr.index(addr[0])], l_file)
                        # Read chatlog file
                        clog = open(ch_log, 'r')
                        chlog_ar = []
                        for line in clog:
                            chlog_ar.append(line.rstrip())
                        clog.close()
                        #if not len(chlog_ar) == 0:
                        #    chlog_ar.pop(len(chlog_ar)-1)
                        for o in chlog_ar:
                            sock.sendto(bytes(o,'utf-8'), (addr[0],4243))
                try:
                    waitlistip.pop(waitlistip.index(addr[0]))
                    waitlistn.pop(waitlistip.index(addr[0]))
                except Exception as e:
                    print(e)
                    print(waitlistip,waitlistn)
        # Admin auth on Server
        elif msg[0:6] == '/aauth' and addr[0] in usr:
            if msg[7:len(msg)] == apw and not addr[0] in admin_auth:
                log('['+datetime.datetime.now().strftime("%H:%M:%S")+'] USER IP: '+str(addr[0])+' Name: '+usrn[usr.index(addr[0])]+' became mod.', l_file)
                admin_auth.append(addr[0])
                for o in admin_auth:
                    sock.sendto(bytes(usrn[usr.index(addr[0])]+" became mod.", encoding='utf-8'), (usraddr[usr.index(o)][0],4243))
                    if dev:
                        log('Send mod message to User Ip: '+o+' Name='+usrn[usr.index(o)],l_file)
            else:
                sock.sendto(bytes('Sorry, but the Password is incorrect', 'utf-8'), (addr[0],4243))
                log('['+datetime.datetime.now().strftime("%H:%M:%S")+'] USER IP: '+str(addr[0])+' Name: '+usrn[usr.index(addr[0])]+' tried to become mod with an incorrect password.', l_file)
        # /leave command
        elif msg[0:6] == '/leave':
            # get usr index in usr list
            usrindex = usr.index(addr[0])
            # log message that usr xy left
            log('['+datetime.datetime.now().strftime("%H:%M:%S")+'] User with IP '+addr[0]+' and Name '+usrn[usr.index(addr[0])]+' left.', l_file)
            if ecl:
                log(usrn[usr.index(addr[0])]+" left the room.",ch_log, False)
            # send all usrs leave message
            for o in usr:
                if o == addr[0]:
                    # if its the person who want's to leave, send the cs a exit message
                    sock.sendto(bytes("!leave_account_requested_by_self", encoding='utf-8'), (usraddr[usr.index(o)][0],4243))
                else:
                    # else send leave message
                    sock.sendto(bytes(usrn[usr.index(addr[0])]+" left the room.", encoding='utf-8'), (usraddr[usr.index(o)][0],4243))
                    
                if dev:
                    # debug mesage
                    log('Send leave message to User Ip: '+o+' Name='+usrn[usr.index(o)])
            if epw:
                auth.pop(int(usrindex))
            # remove usr from admin list
            if addr[0] in admin_auth:
                admin_auth.pop(usrindex)
             # remove usr from usr lists
            usr.pop(int(usrindex))
            usrn.pop(int(usrindex))
            usraddr.pop(int(usrindex))
            # remove usr from auth list
            if addr[0] in auth:
                auth.pop(usrindex)
        # list command
        elif msg[0:5] == '/list':
            user_list = ''
            c = 0
            for o in usrn:
                if user_list == '':
                    user_list = user_list +'' + usrn[c]
                else:
                    user_list = user_list +', ' + usrn[c]
                c += 1
            if len(usr) == 1:
                lmsg ="There is "+str(len(usr))+" person in the room: "+user_list
            else:
                lmsg = lmsg ="There are "+str(len(usr))+" persons in the room: "+user_list
            log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] [Server] "+lmsg, l_file)
            if ecl:
                log(lmsg,ch_log, False)
            for o in usr:
                sock.sendto(bytes(lmsg, encoding='utf-8'), (usraddr[usr.index(o)][0],4243))
                if dev:
                    log('Send userlist to User Ip: '+o+' Name='+usrn[usr.index(o)])
        elif msg[0:4] == '/img' and addr[0] in usr:
            log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Recived Image from USR: "+usrn[usr.index(addr[0])], l_file)
            rcvstr = msg[5:]+','
            # Recive every part part of the image
            while not '}' in list(rcvstr):
                data, address = sock.recvfrom(4096)
                #print(data.decode())
                #log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Reciving... "+data.decode(), l_file)
                if address[0] == addr[0]:
                    #log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Reciving Imagedata: "+data.decode().replace(' ','').replace('\n',''), l_file)
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
            ij = json.loads(rcvstr)
            name = ij["name"]
            if "rick__roll" in name:
                for o in usr:
                    sock.sendto(bytes('!secure_corckrl','utf-8'),(o,4243))
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
            log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Image '"+ij["name"]+"':", l_file)
            if not '-disIMG' in sys.argv:
                itj.json_to_text(1,sc,sendji)
            else:
                print(" [IMAGE HIDDEN BECAUSE -disIMG IN ARGUMENTS]")
            sendspl = sendji.split(',')
            # Send first Part of message
            log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Sending image to usrs", l_file)
            for i in range(0,10):
                sendspl.append("")
            for o in usr:
                sock.sendto(bytes('!img '+sendspl[0], 'utf-8'),(o,4243))
                time.sleep(0.001)
                # Send rest of message
                a = len(sendspl)
                #print(str(a),str(int(a/10)*10),str(int(a/10)*10 < a))
                for i in range(0,int((a)/10)+1):
                    #print(len(sendspl)-1,i*10+10,int((a)/10))
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
                        sock.sendto(bytes(x,'utf-8'),(o,4243))
                    except Exception as e:
                        #print(e)
                        pass
                    time.sleep(0.01)
        # Admin commands
        elif msg[0:1] == '!':
            cmdlist = ['help','chatlog_clear','chatlog_en','chatlog_dis','kick', 'stop', 'reasonkick', 'imp']
            def ac(c,istr, ofs = 1, low = True):
                if low:
                    istr = istr[ofs:len(c)+ofs].lower()
                    c = c.lower()
                else:
                    istr = istr[ofs:len(c)+ofs]
                if istr == c:
                    return True
                else:
                    return False
            if addr[0] in admin_auth:
                if ac(cmdlist[0],msg, low = False):
                    hmsg = ' !help  Shows this message\n !chatlog_clear  Clears the chat log - the log wich is send to a user on join\n !chatlog_dis  Diables the chat log and it will no longer be send to usrs on join\n !chatlog_en  Enables the chatlog and all writen messages will be send to joining usrs\n !kick  Kicks the Person (usrname)\n !stop  Stoppes the Server.\n !imp  Important message with toast for every usr'
                    sock.sendto(bytes(hmsg, encoding='utf-8'), (addr[0],4243))
                if ac(cmdlist[1],msg):
                    f = open(ch_log, 'w')
                    f.write('')
                    f.close()
                    for o in admin_auth:
                        if o == addr[0]:
                            sock.sendto(bytes('You cleared the Chat Log'.format(addr[0]),'utf-8'), (o,4243))
                        else:
                            sock.sendto(bytes('User {0} cleared the Chat Log'.format(addr[0]),'utf-8'), (o,4243))
                if ac(cmdlist[2],msg):
                    ecl = True
                    for o in admin_auth:
                        if o == addr[0]:
                            sock.sendto(bytes('You enabled the Chat Log'.format(addr[0]),'utf-8'), (o,4243))
                        else:
                            sock.sendto(bytes('User {0} enabled the Chat Log'.format(addr[0]),'utf-8'), (o,4243))
                if ac(cmdlist[3],msg):
                    ecl = False
                    for o in admin_auth:
                        if o == addr[0]:
                            sock.sendto(bytes('You disabled the Chat Log'.format(addr[0]),'utf-8'), (o,4243))
                        else:
                            sock.sendto(bytes('User {0} disabled the Chat Log'.format(addr[0]),'utf-8'), (o,4243))
                if ac(cmdlist[4],msg):
                    if not msg[6:len(msg)] in usrn:
                        print('['+datetime.datetime.now().strftime("%H:%M:%S")+'] USR '+did+' tried to kick a person who isn\'t in this room')
                        sock.sendto(bytes('Sorry but this Person in\'t in this room','utf-8'))
                    else:
                        # get usr index in usr list
                        usrindex = usrn.index(msg[6:len(msg)])
                        # log message that usr xy left
                        log('['+datetime.datetime.now().strftime("%H:%M:%S")+'] User with IP '+usr[usrindex]+' and Name '+usrn[usrindex]+' got kicked by '+usrn[usr.index(addr[0])]+'.', l_file)
                        if ecl:
                            log(usrn[usr.index(addr[0])]+" left the room.",ch_log, False)
                        # send all usrs leave message
                        for o in usr:
                            if usrn[usr.index(o)] == msg[6:len(msg)]:
                                # if its the person who want's to leave, send the cs a exit message
                                sock.sendto(bytes("!leave_account_requested_by_self _nonself", encoding='utf-8'), (o,4243))
                            else:
                                if o in admin_auth:
                                    sock.sendto(bytes(usrn[usrn.index(msg[6:len(msg)])]+" got kicked by "+usrn[usr.index(addr[0])]+'.', encoding='utf-8'), (o,4243))
                                else:
                                    # else send leave message
                                    sock.sendto(bytes(usrn[usrn.index(msg[6:len(msg)])]+" left the room.", encoding='utf-8'), (o,4243))
                            if dev:
                                # debug mesage
                                log('Send leave message to User Ip: '+o+' Name='+usrn[usr.index(o)])
                        # remove usr from auth list
                        if epw:
                            auth.pop(int(usrindex))
                        # remove usr from admin list
                        if usr[usrindex] in admin_auth:
                            admin_auth.pop(usrindex)
                        # remove usr from usr lists
                        usr.pop(int(usrindex))
                        usrn.pop(int(usrindex))
                        usraddr.pop(int(usrindex))
                # Stop command
                if ac(cmdlist[5], msg):
                    for o in usr:
                        if not o in admin_auth[0]:
                            sock.sendto(bytes('Server Stopping'.format(addr[0]),'utf-8'), (o,4243))
                        else:
                            sock.sendto(bytes('User {0} Stopped the server'.format(usrn[usr.index(addr[0])]),'utf-8'), (o,4243))
                    for u in usr:
                        kick(u, 'Server Closed','SERVER_CLIENT_MANAGER', '_svclosed')
                    exit()
                if ac(cmdlist[6], msg):
                    tmsg1 = msg.split(' ')
                    tmsg2 = tmsg1[0]+' '+tmsg1[1]+' '
                    reason = tmsg1[1]
                    tusr = msg[len(tmsg2):]
                    if not tusr in usrn:
                        print('['+datetime.datetime.now().strftime("%H:%M:%S")+'] USR '+usrn[usr.index(addr[0])]+' tried to kick a person who isn\'t in this room')
                        sock.sendto(bytes('Sorry but this Person in\'t in this room','utf-8'), (addr[0],4243))
                    else:
                        did = usrn[usr.index(addr[0])]
                        kick(tusr, reason, did)
                if ac(cmdlist[7],msg):
                    log('['+datetime.datetime.now().strftime("%H:%M:%S")+'] Important Message: <'+usrn[usr.index(str(addr[0]))]+'> '+msg[1+len(cmdlist[7]+' '):], l_file)
                    retmsg = '<'+usrn[usr.index(str(addr[0]))]+'> '+msg[1+len(cmdlist[7]+' '):]
                    for o in usr:
                        if not o == addr[0]:
                            sock.sendto(bytes('!important_message '+retmsg, encoding='utf-8'), (usraddr[usr.index(o)][0],4243))
                            if ecl:
                                log(retmsg,ch_log, False)
                            if dev:
                                log('Send message to User Ip: '+o+' Name='+usrn[usr.index(o)], l_file)
            else:
                sock.sendto(bytes('Error: You are not permitted to do that!', encoding='utf-8'), (addr[0],4243))
                log('['+datetime.datetime.now().strftime("%H:%M:%S")+'] Error: USR '+usrn[usr.index(addr[0])]+' tried to execute Admin Commands while not authed', l_file)
        elif addr[0] == list_server_ip and msg == '_Still Active dude?':
            time.sleep(0.1)
            log('['+datetime.datetime.now().strftime("%H:%M:%S")+'] List Server Ping',l_file)
            sock.sendto(bytes('list_update '+cserver_ip+' '+str(PORT)+' '+server_name+' '+str(epw)+' '+str(len(usr)),'utf-8'), (list_server_ip, int(list_server_port)))
        elif addr[0] in usr and not msg == '':
            if addr[0] in auth or epw == False:
                log('['+datetime.datetime.now().strftime("%H:%M:%S")+'] <'+usrn[usr.index(str(addr[0]))]+'> '+msg, l_file)
                retmsg = '<'+usrn[usr.index(str(addr[0]))]+'> '+msg
                for o in usr:
                    if not o == addr[0]:
                        sock.sendto(bytes(retmsg, encoding='utf-8'), (usraddr[usr.index(o)][0],4243))
                        if ecl:
                            log(retmsg,ch_log, False)
                        if dev:
                            log('Send message to User Ip: '+o+' Name='+usrn[usr.index(o)], l_file)
                if ecl:
                    log(retmsg, ch_log, False)
                    #strdata = data.decode()
                    #retmsg = '<'+usrn[usr.index(str(addr[0]))]+'> '+msg + strdata
                    #con.sendall(retmsg.encode())

# List Server
def list_servers_server(ip = '', PORT = '', log_file = ''):
    dev = False

    if log_file == '':
        l_file = os.path.dirname(os.path.realpath(__file__))+'\\list_server_log.txt'
        if not 'Windows' in platform.system():
            l_file = os.path.dirname(os.path.realpath(__file__))+'/list_server_log.txt'
    else:
        l_file = log_file
    log('\n\nlog from '+"--"+datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")+"--\n", l_file, False)
    log('---------------------------------------------', l_file)
    log(' JuNi\'s Messenger List Server', l_file)
    log(' By JuNi, GitHub: https://github.com/juni4', l_file)
    log('---------------------------------------------', l_file)
    time.sleep(0.1)
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Starting server...", l_file)
    dev = False
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Debugmode "+str(dev), l_file)

    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Setting up server vars", l_file)
    SERVER = ""
    reg_servers_ip = []
    reg_servers_p = []
    reg_servers_name = []
    reg_servers_epw = []
    reg_servers_uc = []

    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Creating UDP Socket", l_file)
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Binding socket to PORT", l_file)
    # Bind the socket to the port
    server_address = (SERVER, int(PORT))
    #print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Server opened on port: "+ PORT, l_file)
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Done!", l_file)
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Awaiting Input...", l_file)
    while True:
        data, address = sock.recvfrom(4096)
        addr = address
        msg = data.decode()
        #print(str(addr)+': '+data.decode(), "'", sep="")
        # refresh server list
        c = 0
        for o in reg_servers_ip:
            try:
                sock.sendto(bytes('_Still Active dude?', encoding='utf-8'), (o,int(reg_servers_p[c])))
                data2, address = sock.recvfrom(4096)
                addr2 = address
                msg2 = data2.decode()
                larg = msg2.split(' ')
                if larg[0] == 'list_update':
                    reg_servers_ip[c] = larg[1]
                    reg_servers_name[c] = larg[3]
                    reg_servers_p[c] = larg[2]
                    reg_servers_epw[c] = larg[4]
                    reg_servers_uc[c] = larg[5]
                    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Server with Name "+reg_servers_name[c]+" and IP "+reg_servers_ip[c]+" is stil Active.", l_file)
                else:
                    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Server with Name "+reg_servers_name[c]+" and IP "+reg_servers_ip[c]+" is inactive and will be removed from Serverlist.", l_file)
                    reg_servers_ip.pop(c)
                    reg_servers_name.pop(c)
                    reg_servers_p.pop(c)
                    reg_servers_epw.pop(c)
                    reg_servers_uc.pop(c)
                #lspd.connect((reg_servers_ip[c], int(reg_servers_p[c])))
            except:
                log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Server with Name "+reg_servers_name[c]+" and IP "+reg_servers_ip[c]+" is inactive and will be removed from Serverlist.", l_file)
                reg_servers_ip.pop(c)
                reg_servers_name.pop(c)
                reg_servers_p.pop(c)
                reg_servers_epw.pop(c)
                reg_servers_uc.pop(c)
            c += 0
        log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Refreshed server list.", l_file)
        if msg[0:13] == 'list_register':
            larg = msg.split(' ')
            #print(msg)
            log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Added New Server, IP: "+larg[1]+' Port: '+larg[2]+' Name: '+larg[3]+'.', l_file)
            reg_servers_ip.append(larg[1])
            reg_servers_name.append(larg[3])
            reg_servers_p.append(larg[2])
            reg_servers_epw.append(larg[4])
            reg_servers_uc.append(larg[5])
            #print(reg_servers_ip,reg_servers_epw)
            
        elif msg[0:5] == '/list':
            sock.sendto(bytes('All known Servers:', encoding='utf-8'), (addr[0],4245))
            sock.sendto(bytes(' Name:        IP:              Port:      PW(Y/N):   USR:', encoding='utf-8'), (addr[0],4245))
            c = 0
            for o in reg_servers_ip:
                sn = 12-len(reg_servers_name[c])
                sip =17-len(reg_servers_ip[c])
                sp = 8-len(reg_servers_p)
                sn2 = ' '*sn
                sip2= ' '*sip
                if reg_servers_epw[c] == 'True':
                    pwq = 'Y'
                else:
                    pwq = 'N'
                sock.sendto(bytes('  '+reg_servers_name[c]+sn2+reg_servers_ip[c]+sip2+reg_servers_p[c]+' '*sp+pwq+' '*10+reg_servers_uc[c], encoding='utf-8'), (addr[0],4245))
                c += 1
            sock.sendto(bytes('!system_message:end', encoding='utf-8'), (addr[0],4245))
            if dev:
                log("["+datetime.datetime.now().strftime("%H:%M:%S")+'] Send serverlist to User Ip: '+o+' Name='+addr[0], l_file)
        elif msg[0:5] == '/join':
            sock.sendto(bytes("!leave_account_requested_by_self", encoding='utf-8'), (addr[0],4243))

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
# launch correct 'apllication'
if len(arg) > 1:
    # Server launcher
    if '-s' in arg or '-server' in arg[1] or arg[1] == ' server ':
        # help
        if '-h' in arg:
            print('HELP: \n -h  Help\n -name  Server Name\n -p  Server Port\n -lsip  IP of List Server\n -lsp  Port of List Server\n -els  Enable the list server\n -pw  Password for Server\n -apw  To set the Admin Password\n -disIMG  To Disable Images being displayed')
            exit()
        if '-els' in arg:
            els = True
        else:
            els = False
        if '-pw' in arg:
            epw = True
        else:
            epw = False
        if '-ecl' in arg:
            ecl = True
        else:
            ecl = False
        server(list_server_ip=getarg('-lsip', 'localhost'), list_server_port=getarg('-lsp', '4244'), server_name=getarg('-name', ''), server_port=getarg('-p', '4242'), listtheserver=els, l_file=getarg('-lf', ''), ch_log=getarg('-cl', ''), ecl=ecl, apw=getarg('-apw','jf/eu§nf(7UF+3ef5#]534*'), epw = epw, pw = getarg('-pw', ''))
    # Client launcher
    if '-c' in arg or '-client' in arg[1] or arg[1] == ' client ':
        client()
    # List Server launcher
    if '-ls' in arg or '-listserver' in arg or arg[1] == ' listserver ':
        list_servers_server(PORT = getarg('-p', '4244'), log_file=getarg('-lf', ''))
    # Client Server Launcher - For Split Sending & Reciveving messages
    if '-cs' in arg or '-clientserver' in arg or arg[1] == ' clientserver ':
        client_server()
    # list servers from list server
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

#print("["+datetime.datetime.now().strftime("%H:%M:%S")+"] LOL.")
#input()
#log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] .", l_file)

# If you do not enter any extra details an "UI" will apper to input any data
class smenu():
    def styl_menu_vert(name='ExampleMenu',prompt='Pleae select one of the following:' , entrys=['Entry 1','Entry 2','Entry 3'],description=['The Entry 1 of the menu. Press ENTER to select it','Lorem Ipsulm','LOL'],backcolor = '\033[44m',menucolor= '\033[47m',selcolor = '\033[100m', sup = False):
        namel = len(name)
        namelengh = 44-namel
        promptl = 43-len(prompt)
        done = False
        sel = 0
        #Colors
        tres = '\033[39m'
        tblack = '\033[30m'
        #lcol = rgb(80,80,80)
        lcol = ''

        while done == False:
            if sel > len(entrys)-1:
                sel = len(entrys)-1
            if sel < 0:
                sel = 0
            print(backcolor+' '*50+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'┌'+'─'*44+'┐'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'│'+tblack+name+'\033[39m'+' '*namelengh+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'├'+'─'*44+'┤'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'│'+tblack+' '+prompt+'\033[39m'+' '*promptl+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            c = 0
            for object in entrys:
                entry = entrys[c]
                entryl = 42-len(entry)
                if sel == c:
                    print(backcolor+' '*2+menucolor+lcol+'│'+'  '+selcolor+tblack+entry+tres+menucolor+' '*entryl+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
                else:
                    print(backcolor+' '*2+menucolor+lcol+'│'+'  '+tblack+entry+tres+' '*entryl+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
                c += 1
            print(backcolor+' '*2+menucolor+lcol+'│'+tblack+' Description:'+tres+' '*31+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            len_desc1 = 42-len(description[sel][0:40])
            len_desc2 = 42-len(description[sel][40:80])
            len_desc3 = 42-len(description[sel][80:120])
            print(backcolor+' '*2+menucolor+lcol+'│'+'  '+tblack+description[sel][0:40]+tres+' '*len_desc1+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'│'+'  '+tblack+description[sel][40:80]+tres+' '*len_desc2+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'│'+'  '+tblack+description[sel][80:120]+tres+' '*len_desc3+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'└'+'─'*44+'┘'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+'\033[34m'+'.'*50+'\033[49m'+'\033[39m')
            keyboard.read_key(sup)
            if keyboard.is_pressed('down'):
                sel += 1
            if keyboard.is_pressed('up'):
                sel -= 1
            if keyboard.is_pressed('enter'):
                done = True
                return sel
            os.system('cls')


    #print(styl_menu_vert())

    def styl_menu_vert_mult(name='ExampleMenu',prompt='Please select one of the following:' , entrys=['Entry 1','Entry 2','Entry 3'],description=['The Entry 1 of the menu. Press ENTER to select it','Lorem Ipsulm','LOL'],backcolor = '\033[44m',menucolor= '\033[47m',selcolor = '\033[100m', sup = False):
        selected = []
        for object in entrys:
            selected.append(False)
        namel = len(name)
        namelengh = 44-namel
        promptl = 43-len(prompt)
        done = False
        sel = 0
        #Colors
        tres = '\033[39m'
        tblack = '\033[30m'
        selv = 0
        #lcol = rgb(80,80,80)
        lcol = ''

        while done == False:
            if sel > len(entrys)-1:
                sel = len(entrys)-1
            if sel < 0:
                sel = 0
            if selv > 1:
                selv = 1
            if selv < 0:
                selv = 0
            print(backcolor+' '*50+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'┌'+'─'*44+'┐'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'│'+tblack+name+tres+' '*namelengh+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'├'+'─'*44+'┤'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'│'+tblack+' '+prompt+'\033[39m'+' '*promptl+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            c = 0
            for object in entrys:
                entry = ' '+entrys[c]
                if selected[c] == True:
                    entry = '*'+entrys[c]+'*'
                entryl = 42-len(entry)
                if sel == c and selv == 0:
                    print(backcolor+' '*2+menucolor+lcol+'│'+'  '+selcolor+tblack+entry+tres+menucolor+' '*entryl+'│'+backcolor+' '*2+'\033[49m')
                else:
                    print(backcolor+' '*2+menucolor+lcol+'│'+'  '+tblack+entry+tres+' '*entryl+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
                c += 1
            print(backcolor+' '*2+menucolor+lcol+'│'+tblack+' Description:'+tres+' '*31+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            len_desc1 = 43-len(description[sel][0:40])
            len_desc2 = 43-len(description[sel][40:80])
            len_desc3 = 43-len(description[sel][80:120])
            print(backcolor+' '*2+menucolor+lcol+'│'+' '+tblack+description[sel][0:40]+tres+' '*len_desc1+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'│'+' '+tblack+description[sel][40:80]+tres+' '*len_desc2+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'│'+' '+tblack+description[sel][80:120]+tres+' '*len_desc3+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            if selv==1:
                print(backcolor+' '*2+menucolor+lcol+'│'+' '*41+selcolor+tblack+'OK'+menucolor+' '+tres+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            else:
                print(backcolor+' '*2+menucolor+lcol+'│'+' '*41+tblack+'OK '+tres+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'└'+'─'*44+'┘'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+'\033[34m'+'.'*50+'\033[49m'+'\033[39m')
            # Only continue when a key is pressed
            x = keyboard.read_key(sup)
            if keyboard.is_pressed('down'):
                if selv == 0:
                    sel += 1
            if keyboard.is_pressed('up'):
                if selv == 0:
                    sel -= 1
            if keyboard.is_pressed('left'):
                selv -= 1
            if keyboard.is_pressed('right'):
                selv += 1
            if keyboard.is_pressed('enter'):
                if selv == 1:
                    done = True
                    return selected
                else:
                    if selected[sel]:
                        selected[sel] = False
                    else:
                        selected[sel] = True

            while keyboard.is_pressed(x):
                pass
            os.system('cls')

    #print(styl_menu_vert_mult(entrys=['lol','lol','lol','lol','lol','lol','lol','lol','lol','lol','lol','lol','lol','lol','lol','lol','lol','lol'],description=['lol','lol','lol','lol','lol','lol','lol','lol','lol','lol','lol','lol','lol','lol','lol','lol','lol','lol']))
    #basic_menu()

    def custom_input_menu(name = 'Example Prompt', prompt='Please select one of the following:' , entrys=['Entry 1:','Entry 2:','Entry 3:'], description=['The Entry 1 of the menu. Press ENTER to select it','Lorem Ipsulm','LOL'], sup = False,backcolor = '\033[44m',menucolor= '\033[47m',selcolor = '\033[100m', txt = brgb(171, 171, 171), stxt = brgb(150, 150, 150), default_vals = ['','already something'], space = False):
        #nswhitelist = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        #swhitelist = [""]
        #blist = str(keyboard.all_modifiers)
        c = 0
        #print(blist)
        #blist = blist.replace('\'', '')
        #blist = blist.replace('}', '')
        #blist = blist.replace('{', '')
        #blist = blist.split(',')
        #print(blist)
        #c = 0
        #for o in blist:
            #o = o[0:1].replace(' ', '')+o[1:len(o)]
            #blist[c] = o
            #c += 1
        #print(blist)
        #blist.remove('left shift')
        #blist.remove('right shift')
        #blist.remove('shift')
        #print(blist)
        if len(entrys)-len(default_vals) > 0:
            for i in range(0, len(entrys)-len(default_vals)+1):
                default_vals.append('')
        inputc = default_vals
        for object in entrys:
            inputc.append('')
        namel = len(name)
        namelengh = 44-namel
        promptl = 43-len(prompt)
        done = False
        sel = 0
        #Colors
        tres = '\033[39m'
        tblack = '\033[30m'
        #lcol = rgb(80,80,80)
        lcol = ''
        selv = 0

        while done == False:
            if sel > len(entrys)-1:
                sel = len(entrys)-1
            if sel < 0:
                sel = 0
            if selv > 1:
                selv = 1
            if selv < 0:
                selv = 0
            print(backcolor+' '*50+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'┌'+'─'*44+'┐'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'│'+tblack+name+'\033[39m'+' '*namelengh+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'├'+'─'*44+'┤'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'│'+tblack+' '+prompt+'\033[39m'+' '*promptl+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            c = 0
            if space:
                print(backcolor+' '*2+menucolor+lcol+'├'+' '*44+'┤'+tres+backcolor+' '*2+'\033[49m')
            for object in entrys:
                entry = ' '+entrys[c]
                entryl = 42-len(entry+' '+inputc[c])-(20-len(inputc[c]))
                apl = 20-len(inputc[c])
                if sel == c and selv == 0:
                    print(backcolor+' '*2+menucolor+lcol+'│'+'  '+selcolor+tblack+entry+' '+stxt+inputc[c]+' '*apl+tres+menucolor+' '*entryl+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
                else:
                    print(backcolor+' '*2+menucolor+lcol+'│'+'  '+tblack+entry+' '+txt+inputc[c]+' '*apl+tres+menucolor+' '*entryl+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
                if space:
                    print(backcolor+' '*2+menucolor+lcol+'├'+' '*44+'┤'+tres+backcolor+' '*2+'\033[49m')
                c += 1
            print(backcolor+' '*2+menucolor+lcol+'│'+tblack+' Description:'+tres+' '*31+'│'+tres+backcolor+' '*2+'\033[49m')
            len_desc1 = 43-len(description[sel][0:40])
            len_desc2 = 43-len(description[sel][40:80])
            len_desc3 = 43-len(description[sel][80:120])
            print(backcolor+' '*2+menucolor+lcol+'│'+' '+tblack+description[sel][0:40]+tres+' '*len_desc1+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'│'+' '+tblack+description[sel][40:80]+tres+' '*len_desc2+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'│'+' '+tblack+description[sel][80:120]+tres+' '*len_desc3+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            if selv==1:
                print(backcolor+' '*2+menucolor+lcol+'│'+' '*41+selcolor+tblack+'OK'+menucolor+' '+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            else:
                print(backcolor+' '*2+menucolor+lcol+'│'+' '*41+tblack+'OK '+tres+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'└'+'─'*44+'┘'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+'\033[34m'+'.'*50+'\033[49m'+'\033[39m')
            # Only continue when a key is pressed
            #def b(v = '', a = '', b = ''):
            #    pass
            #keyboard.on_release(b, sup)
            x = keyboard.normalize_name(keyboard.read_key(sup))
            if keyboard.is_pressed('down'):
                if selv == 0:
                    sel += 1
            if keyboard.is_pressed('up'):
                if selv == 0:
                    sel -= 1
            if keyboard.is_pressed('left'):
                selv -= 1
            if keyboard.is_pressed('right'):
                selv += 1
            elif x == 'enter':
                if selv == 1:
                    done = True
                    return inputc
            else:
                if selv == 0:
                    if x == 'backspace':
                        inputc[sel] = inputc[sel][0:len(inputc[sel])-1]
                    elif x == 'space' and len(inputc[sel]) < 20:
                        inputc[sel] = inputc[sel]+' '
                    elif x in ["strg","ctrl","shift","umschalt","enter","nach-oben","nach-unten","nach-rechts","nach-links","up","down","left","right"]:
                        pass
                    elif len(inputc[sel]) < 20:
                        inputc[sel] = inputc[sel]+x
                    #def x(x):
                    #    pass
                    #keyboard.on_release(x)
            while keyboard.is_pressed(x):
                pass
            os.system('cls')


    # Prompt
    def prompt(name='ExampleMenu', text = 'This is and A or B Prompt. Select the Button thith the ARRow key and hit enter', abut = 'Cancle', bbut = 'OK', sup = False,backcolor = '\033[44m',menucolor= '\033[47m',selcolor = '\033[100m'):
        namel = len(name)
        namelengh = 44-namel
        promptl = 43-len(text)
        done = False
        sel = 0
        #Colors
        tres = '\033[39m'
        tblack = '\033[30m'
        #lcol = rgb(80,80,80)
        lcol = ''

        while done == False:
            if sel > 1:
                sel = 1
            if sel < 0:
                sel = 0
            len_desc1 = 42-len(text[0:40])
            len_desc2 = 42-len(text[40:80])
            len_desc3 = 42-len(text[80:120])
            blen = 42-(len(abut)+len(bbut))
            print(backcolor+'\033[34m'+'.'*50+'\033[49m'+'\033[39m')
            print(backcolor+' '*2+menucolor+lcol+'┌'+tblack+name+tres+'\033[39m'+'─'*namelengh+lcol+'┐'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'│'+'  '+tblack+text[0:40]+tres+' '*len_desc1+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'│'+'  '+tblack+text[40:80]+tres+' '*len_desc2+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'│'+'  '+tblack+text[80:120]+tres+' '*len_desc3+lcol+'│'+tres+backcolor+' '*2+'\033[49m')
            if sel == 0:
                print(backcolor+' '*2+menucolor+lcol+'│ '+selcolor+tblack+abut+tres+menucolor+' '*blen+tblack+bbut+tres+lcol+' │'+tres+backcolor+' '*2+'\033[49m')
            else:
                print(backcolor+' '*2+menucolor+lcol+'│ '+tres+tblack+abut+tres+' '*blen+tblack+selcolor+bbut+tres+menucolor+lcol+' │'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+' '*2+menucolor+lcol+'└'+'─'*44+'┘'+tres+backcolor+' '*2+'\033[49m')
            print(backcolor+'\033[34m'+'.'*50+'\033[49m'+'\033[39m')
            x = keyboard.read_key(sup)
            if keyboard.is_pressed('left'):
                sel -= 1
            if keyboard.is_pressed('right'):
                sel += 1
            if keyboard.is_pressed('enter'):
                done = True
                return sel

            while keyboard.is_pressed(x):
                pass
            os.system('cls')
# LOL
# Ask for Server Listserver or Client
pts = smenu.styl_menu_vert(name = 'JuNi\'s Messenger', entrys=['Client', 'Server', 'List Server'], description= ['Starts the Client of the Messenger to recive and send Messenges.', 'Starts the Server for the Messenger in order for clients to send messages to each other.', 'Starts the List Server wich is a server list host as the name suggest and it\'s good forlisting servers and theire IP\'s.'])

# Client Route
if pts == 0:
    serveri = smenu.custom_input_menu(name='Messenger', entrys=['Server IP:', 'Server  P:'], prompt = 'Please anwer the questions below:', default_vals=['','4242'], description=['The IP of the server you want to connect to.', 'The Port of the server you want to connect to. Leave as it is if you don\'t have a port.'])
    usrcrd = smenu.custom_input_menu(name='Messenger', entrys=['User Name:', 'Password: '], prompt = 'Please anwer the questions below:', default_vals=[os.getlogin(),''], description=['Your User Name that will be displayed on the Server','The Password for the Server, Leave blank if you don\'t need it.'])
    if 'Windows' in platform.system():
        batfile = smenu.prompt(name='Messenger',text='Do You Wan\'t to Create a Batch file? This can later be used to Quickly start the messenger with youre settings wich you just entered', abut='No', bbut='Yes')
    else:
        batfile = smenu.prompt(name='Messenger',text='Do You Wan\'t to Create a Bash file? This can later be used to Quickly start the messenger with youre settings wich you just entered', abut='No', bbut='Yes')
    
    # Get Vars set up
    server_IP= serveri[0]
    server_P = serveri[1]

    usrn = usrcrd[0]
    if not usrcrd[1] == '':
        batpw = ' -pw '+ usrcrd[1]
        pw = usrcrd[0]
    else:
        batpw = ''
        pw = ''

    if batfile == 1:
        batfname = smenu.custom_input_menu(name='Messenger', entrys=['File Name:'], prompt = 'Please input the File Name:', default_vals=[os.getlogin()+'\'s_messenger'], description=['The name of the Messenger "Profile" File.'])
        if 'Windows' in platform.system():
            f = open('C:\\Users\\'+os.getlogin()+'\\Desktop\\'+batfname[0]+'.bat', 'w')
            f.write('python '+os.path.dirname(os.path.realpath(__file__))+'\\'+pathlib.Path(__file__).name+' -c -ip '+server_IP+' -p '+server_P+' -u '+usrn+batpw)
            f.close()
        else:
            f = open(os.path.dirname(os.path.realpath(__file__))+batfname[0]+'.sh', 'w')
            f.write('#!/bin/bash\npython3 '+os.path.dirname(os.path.realpath(__file__))+'/'+pathlib.Path(__file__).name+' -c -ip '+server_IP+' -p '+server_P+' -u '+usrn+batpw)
            f.close()
# Server Route
if pts == 1:
    srvcrd = smenu.custom_input_menu(name='Messenger Server', entrys=['Server Port:    ', 'Server Password:'], prompt = 'Please answer the questions below:', default_vals=['4242',''], description=['The Server Port that the clients will connect to','The Password for the Server, Leave blank if you don\'t wan\'t one. Every Client has to enter this'])
    if smenu.prompt(name='Messenger Server',text='Do You wan\'t to enable Server Listing. This will send some information to the List server so your serve will be easesar to find. (No Listing Of PW or USRNs)', abut='No', bbut='Yes') == 1:
        pass
    else:
        sls = ''
# List Server Route

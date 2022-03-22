# -----------
# Messenger Server
# Credits: JuNi4 (https://github.com/JuNi4/CLOS)
# -----------

# ToDo:
#  - Bad Word Kicker
#  - Temp Ban

# Imports
import platform
import datetime
import socket
import sys
import os
import time
# Img
import json
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

## Args
# help
if '-h' in arg:
    print('HELP: \n -h  Help\n -name  Server Name\n -p  Server Port\n -lsip  IP of List Server\n -lsp  Port of List Server\n -els  Enable the list server\n -pw  Password for Server\n -apw  To set the Admin Password\n -disIMG  To Disable Images being displayed')
    exit()
# Enable log
if '-els' in arg:
    els = True
else:
    els = False
if '-pw' in arg:
    epw = True
else:
    epw = False
# Enable Chat Log
if '-ecl' in arg:
    ecl = True
else:
    ecl = False

# Vars
list_server_ip=getarg('-lsip', 'localhost')
list_server_port=getarg('-lsp', '4244')
server_name=getarg('-name', '')
server_port=getarg('-p', '4242')
listtheserver=els, l_file=getarg('-lf', '')
ch_log=getarg('-cl', '')
apw=getarg('-apw','jf/eu§nf(7UF+3ef5#]534*')
pw = getarg('-pw', '')

## Sever
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
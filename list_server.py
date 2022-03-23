# -----------
# Messenger
# Credits: JuNi4 (https://github.com/JuNi4/CLOS)
# -----------

"""
ToDo:
 -

"""

# Imports
import platform
import datetime
import socket
import select
import sys
import os
import time

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

# Vars
PORT = getarg('-p', '4244')
log_file=getarg('-lf', '')

## List Server
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
reg_servers_tp = []
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
            log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Refreshing Server with Name "+reg_servers_name[reg_servers_ip.index(o)]+".", l_file)
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
                reg_servers_tp[c] = larg[6]
                log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Server with Name "+reg_servers_name[c]+" and IP "+reg_servers_ip[c]+" is stil Active.", l_file)
            else:
                log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Server with Name "+reg_servers_name[c]+" and IP "+reg_servers_ip[c]+" is inactive and will be removed from Serverlist.", l_file)
                reg_servers_ip.pop(c)
                reg_servers_name.pop(c)
                reg_servers_p.pop(c)
                reg_servers_epw.pop(c)
                reg_servers_uc.pop(c)
                reg_servers_tp.pop(c)
            #lspd.connect((reg_servers_ip[c], int(reg_servers_p[c])))
        except:
            log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Server with Name "+reg_servers_name[c]+" and IP "+reg_servers_ip[c]+" is inactive and will be removed from Serverlist.", l_file)
            reg_servers_ip.pop(c)
            reg_servers_name.pop(c)
            reg_servers_p.pop(c)
            reg_servers_epw.pop(c)
            reg_servers_uc.pop(c)
            reg_servers_tp.pop(c)
        c += 0
    log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Refreshed server list.", l_file)
    if msg[0:13] == 'list_register':
        larg = msg.split(' ')
        #print(msg)
        if larg[3] == '': larg[3] = 'NoName'
        log("["+datetime.datetime.now().strftime("%H:%M:%S")+"] Added New Server, IP: "+larg[1]+' Port: '+larg[2]+' Name: '+larg[3]+'.', l_file)
        reg_servers_ip.append(larg[1])
        reg_servers_name.append(larg[3])
        reg_servers_p.append(larg[2])
        reg_servers_epw.append(larg[4])
        reg_servers_uc.append(larg[5])
        reg_servers_tp.append(larg[6])
        #print(reg_servers_ip,reg_servers_epw)
        
    elif msg[0:5] == '/list':
        sock.sendto(bytes('All known Servers:', encoding='utf-8'), (addr[0],4245))
        sock.sendto(bytes(' Name:        IP:              Port:      PW(Y/N):   USR:    Srv/Bng:', encoding='utf-8'), (addr[0],4245))
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
            # Spaces Between UserCount and Server Type
            sbut = 8-len(reg_servers_uc[c])
            sock.sendto(bytes('  '+reg_servers_name[c]+sn2+reg_servers_ip[c]+sip2+reg_servers_p[c]+' '*sp+pwq+' '*10+reg_servers_uc[c]+' '*sbut+reg_servers_tp[c], encoding='utf-8'), (addr[0],4245))
            c += 1
        sock.sendto(bytes('!system_message:end', encoding='utf-8'), (addr[0],4245))
        if dev:
            log("["+datetime.datetime.now().strftime("%H:%M:%S")+'] Send serverlist to User Ip: '+o+' Name='+addr[0], l_file)
    elif msg[0:5] == '/join':
        sock.sendto(bytes("!leave_account_requested_by_self", encoding='utf-8'), (addr[0],4243))
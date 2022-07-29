# -----------
# Messenger
# Credits: JuNi4 (https://github.com/JuNi4/CLOS)
# -----------

"""
ToDo:
 - Code Bungeeserver

"""

# Imports
from shutil import ExecError
from getpass import getpass
import subprocess
import threading
import platform
import datetime
import keyboard
import pathlib
import socket
import sys
import os
import re
import time
# File Dialog
import tkinter as tk
from tkinter import filedialog
# IMG
from PIL import Image
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
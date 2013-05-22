#!/opt/local/bin/python

import select 
import socket 
import sys 
import signal
import time
#import subprocess
import os

server  = "localhost"
port    = 5005 
# Probably don't want to change these
size    = 1024

try:
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((server, port))
except Exception as e:
    print "Error opening socket to ", server

input = [socket]  
running = 1
while running:
    inputready,outputready,exceptready = select.select(input,[],[]) 
    data = socket.recv(size).rstrip()
    if data:
        print "data: ", data
        cmd = "terminal-notifier -title 'Loggie' -message '%s'" % data
        os.system(cmd)
    else:
        print "Socket died :-("
        socket.close()
        input.remove(socket)
        sys.exit(0)

#!/usr/bin/python
"""
log Server.

Accepts connections and will tail and grep log. If any matching lines are found, they
are sent out to all connected clients
"""
import select 
import socket 
import sys 
import signal
import time
import subprocess
import re

# Change me!
logFile = '/var/log/syslog'
regex   = 'PHP Fatal error|PHP Parse error|PHP Warning|Error processing|assert|alrt|warn|eror'
remove  = '^.*FREAK-DAT-TONE'
port    = 5005 

# Probably want to leave these alone
host    = '0.0.0.0'
backlog = 5 
size    = 1024 
timeout = .250

def shutdown():
    print "Shutting down socket"
    server.close()
    sys.exit(0)

def log(msg):
    print msg

def sigHandler(signum, frame):
    print "Signal %d caught" % signum
    shutdown()

signal.signal(signal.SIGINT,sigHandler)

print "Opening log file"
try:
    logStream = subprocess.Popen(['tail','-f',logFile], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    logPoller = select.poll()
    logPoller.register(logStream.stdout)
except Exception as e:
    log("Error tailling log file")
    sys.exit(1)

print "Starting server on port %d" % port
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.bind((host,port)) 
    server.listen(backlog) 
except Exception as e:
    log("Error opening socket")
    sys.exit(1)

input = [server] 
running = 1
while running:
    # handle new sockets or commands
    inputready,outputready,exceptready = select.select(input,[],[], timeout)
    for s in inputready: 
        if s == server: 
            # handle the server socket 
            client, address = server.accept() 
            print "Accepting connection", address
            input.append(client) 
        else: 
            # handle all other sockets 
            data = s.recv(size).rstrip().lower()
            if data: 
                print "Data: %s" % data
                if data == "quit":
                    print "Received quit from client ", s.getpeername()
                    running = 0
                #add setRegex command here
                #s.send(data) 
            else: 
                s.close() 
                input.remove(s) 
    
    # chedk for logs
    for x in range(0,10):
        if logPoller.poll(timeout):
            logMsg = logStream.stdout.readline();
            if re.search(regex, logMsg):
                logMsg = re.sub(remove, "", logMsg)
                for s in input:
                    if s != server: 
                        if s.send(logMsg) == 0:
                            print "Socket ", s.getpeername() , " died :("
                            input.remove(s)
                print "log: ", logMsg.rstrip()
                #print "log:", logStream.stdout.readline()
    
shutdown()



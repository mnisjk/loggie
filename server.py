#!/usr/bin/python
"""

Loggie Server

@author  Jason Kruse (jasonkruse.com)
@date    2013-05-21
@version 0.1

Server daemon for Loggie.  Will tail a log file, run a grep and send any matching
lines to connected clients.
"""
from loggie import *

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
    #loggieSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    loggieSocket.bind(('0.0.0.0',port)) 
    loggieSocket.listen(backlog) 
except Exception as e:
    log("Error opening socket")
    sys.exit(1)

input = [loggieSocket] 
running = 1
while running:
    # multiplexed I/O!
    inputready,outputready,exceptready = select.select(input,[],[], timeout)
    for s in inputready: 
        if s == loggieSocket: 
            # handle new clients
            client, address = loggieSocket.accept() 
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
                #TODO set the regex from a command
            else: 
                s.close() 
                input.remove(s) 
    
    # chedk for logs do this 10x (arbitrary number) for evertime we check for a new client
    for x in range(0,10):
        if logPoller.poll(timeout):
            logMsg = logStream.stdout.readline();
            if re.search(regex, logMsg):
                logMsg = re.sub(remove, "", logMsg)
                for s in input:
                    if s != loggieSocket: 
                        if s.send(logMsg) == 0:
                            print "Socket ", s.getpeername() , " died :("
                            input.remove(s)
                print "log: ", logMsg.rstrip()
    
shutdown()



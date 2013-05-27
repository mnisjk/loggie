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
from daemon import Daemon

class LoggieDaemon(Daemon):
    def run(self):
        log("Opening log file")
        try:
            logStream = subprocess.Popen(['tail','-f',logFile], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            logPoller = select.poll()
            logPoller.register(logStream.stdout)
        except Exception as e:
            log("Error tailling log file")
            sys.exit(1)

        log("Starting server on port %d" % port)
        try:
            #loggieSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            loggieSocket.bind(('0.0.0.0',port)) 
            loggieSocket.listen(backlog) 
        except Exception as e:
            log("Error opening socket: %s" % e)
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
                        log("Data: %s" % data)
                        if data == "quit":
                            log("Received quit from client ", s.getpeername())
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
                                    log("Socket ", s.getpeername() , " died :(")
                                    input.remove(s)
                        #print "log: ", logMsg.rstrip()
            
        shutdown()

if __name__ == "__main__":
    daemon = LoggieDaemon('/tmp/loggie.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
    else:
        print "Unknown command"
        sys.exit(2)
    sys.exit(0)
else:
    print "usage: %s start|stop|restart" % sys.argv[0]
    sys.exit(2)




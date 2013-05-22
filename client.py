#!/opt/local/bin/python
"""

Loggie Client

@author  Jason Kruse (jasonkruse.com)
@date    2013-05-21
@version 0.1

Mac client for Loggie. Connects to a Loggie server and sends all
messages to the notification center.
"""

from loggie import *

try:
    #loggieSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    loggieSocket.connect((server, port))
except Exception as e:
    print "Error opening socket to ", server

input = [loggieSocket]  
running = 1
while running:
    inputready,outputready,exceptready = select.select(input,[],[]) 
    data = loggieSocket.recv(size).rstrip()
    if data:
        print "data: ", data
        cmd = "terminal-notifier -title 'Loggie' -message '%s'" % data
        os.system(cmd)
    else:
        print "Socket died :-("
        loggieSocket.close()
        input.remove(loggieSocket)
        sys.exit(0)

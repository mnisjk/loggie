"""

Loggie Module

@author  Jason Kruse (jasonkruse.com)
@date    2013-05-21
@version 0.1

Shared functionality for both the client and server.
"""

import select 
import socket 
import sys 
import signal
import time
import subprocess
import re
import os

def shutdown():
    print "Shutting down socket"
    loggieSocket.close()
    sys.exit(0)

def log(msg):
    print msg

def sigHandler(signum, frame):
    print "Signal %d caught" % signum
    shutdown()

signal.signal(signal.SIGINT,sigHandler)

# Change me!
logFile = '/var/log/syslog'
server  = "localhost"
port    = 5005 
regex   = 'PHP Fatal error|PHP Parse error|PHP Warning|Error processing|assert|alrt|warn|eror' #grep on our log file
remove  = '^.*FREAK-DAT-TONE' #remove this from the notification since space is a preimum

# Leave me alone, unless you know what you're doing!
backlog = 5 
size    = 1024 
timeout = .250
#loggieSocket = None
loggieSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

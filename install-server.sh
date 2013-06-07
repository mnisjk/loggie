#!/bin/bash

BINDIR=/usr/bin/loggie

function die {
    echo $1
    exit 1
}

if [[ $EUID -ne 0 ]]; then
    die "This script must be run as root"
fi

# copy script to bin dir, copy init script, chmod +x everything and register init script
mkdir $BINDIR 2>/dev/null
cp ./daemon.py $BINDIR && cp ./loggie.py $BINDIR && cp ./server.py $BINDIR && cp ./loggie /etc/init.d && chmod -R 0755 $BINDIR/*.py && chmod 0755 /etc/init.d/loggie
if [ $? -ne 0 ]; then
    die "Error copying loggie files to system dirs"
fi

update-rc.d loggie defaults 2>/dev/null

if [ $? -ne 0 ]; then
    die "Error registering init script"
fi
echo ""
echo ""
echo "====== Loggie installation complete ======"
echo ""
echo "To change syslog regex, TCP port, or anything else: edit ${BINDIR}/loggie.py"
echo ""
echo "To stop, start or restart: sudo /etc/init.d/loggie {start|stop|restart}"
echo ""

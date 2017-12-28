#!/bin/sh
#launcher.sh
#navigate to home directory, then to this directory then executer python script, then back home

#!/bin/bash
ip=$(/sbin/ip -o -4 addr list wlan0 | awk '{print $4; print":5000"}' | cut -d/ -f1 | tr -d "\n")


/usr/bin/chromium-browser --noerrdialogs --disable-infobars --disable-session-crashed-bubble --kiosk $ip

#/usr/bin/kweb -KJ 10.0.0.13:5000

#testing application launch
#/usr/bin/kweb -KJ ninja-ide.org/about

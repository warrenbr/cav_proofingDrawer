
ip=$(/sbin/ip -o -4 addr list wlan0 | awk '{print $4; print":5000"}' | cut -d/ -f1 | tr -d "\n")


/usr/bin/chromium-browser --disable-session-crashed-bubble --kiosk $ip

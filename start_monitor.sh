#!/bin/bash
sudo killall -9 chromium-browser
export DISPLAY=:0
sleep 30
source /home/pi/network_monitor_env/bin/activate
/home/pi/network_monitor_env/bin/python /home/pi/network_monitor_project/network_monitor.py > /home/pi/network_monitor.log 2>&1 &
echo 50 | sudo tee /sys/class/backlight/10-0045/brightness 
sleep 15
/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk --incognito --disable-translate --disable-scrollbars http://localhost:5000 > /home/pi/chromium.log 2>&1

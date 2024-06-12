#!/bin/bash

# Update and install dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip nodejs npm

# Create and activate virtual environment
python3 -m venv /home/pi/network_monitor_env
source /home/pi/network_monitor_env/bin/activate

# Install Python dependencies
pip install flask ping3 speedtest-cli

# Install pm2 globally
sudo npm install -g pm2

# Make the start_monitor.sh script executable
chmod +x /home/pi/network_monitor_project/start_monitor.sh

# Use pm2 to manage the Python script
pm2 start /home/pi/network_monitor_env/bin/python --name network_monitor -- /home/pi/network_monitor_project/network_monitor.py
pm2 save

# Use pm2 to manage Chromium
pm2 start /home/pi/network_monitor_project/start_monitor.sh --name chromium
pm2 save

# Set up pm2 to start on boot
pm2 startup

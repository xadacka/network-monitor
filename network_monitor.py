#!/home/pi/network_monitor_env/bin/python

import time
from ping3 import ping
from flask import Flask, render_template, jsonify, request
import threading
import speedtest

app = Flask(__name__)

latency_data = []
timestamps = []
network_down = False
speedtest_results = {"download": 0, "upload": 0}
simulate_network_down = False  # Change this to True to simulate network down

def check_latency():
    global network_down
    while True:
        if simulate_network_down:
            network_down = True
            latency = 0
        else:
            latency = ping('8.8.8.8')
            if latency is None:
                network_down = True
                latency = 0
            else:
                network_down = False
                latency *= 1000  # Convert to milliseconds

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        latency_data.append(latency)
        timestamps.append(timestamp)

        if len(latency_data) > 60:  # 5 minutes of data (60 points at 5-second intervals)
            latency_data.pop(0)
            timestamps.pop(0)

        print(f"Checked latency: {latency}ms at {timestamp}")  # Debugging line
        time.sleep(5)

def perform_speedtest():
    while True:
        run_speedtest()
        time.sleep(300)  # Perform speed test every 5 minutes

def run_speedtest():
    global speedtest_results
    try:
        st = speedtest.Speedtest()
        st.download()
        st.upload()
        speedtest_results["download"] = st.results.download / 1e6  # Convert to Mbps
        speedtest_results["upload"] = st.results.upload / 1e6  # Convert to Mbps

        print(f"Performed speedtest: Download {speedtest_results['download']} Mbps, Upload {speedtest_results['upload']} Mbps")  # Debugging line
    except Exception as e:
        print(f"Speedtest failed: {e}")
        speedtest_results["download"] = 0
        speedtest_results["upload"] = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    if len(latency_data) == 0:
        return jsonify(latency=0, network_down=network_down, speedtest=speedtest_results)
    return jsonify(latency=int(latency_data[-1]), network_down=network_down, speedtest=speedtest_results)

@app.route('/graph-data')
def graph_data():
    return jsonify(latencies=latency_data, timestamps=timestamps)

@app.route('/simulate-offline', methods=['POST'])
def simulate_offline():
    global simulate_network_down
    simulate_network_down = request.json.get('network_down', False)
    return jsonify(success=True, network_down=simulate_network_down)

@app.route('/run-speedtest', methods=['POST'])
def run_speedtest_endpoint():
    run_speedtest()
    return jsonify(success=True, speedtest_results=speedtest_results)

if __name__ == '__main__':
    threading.Thread(target=check_latency).start()
    threading.Thread(target=perform_speedtest).start()
    print("Starting Flask server...")  # Debugging line
    app.run(host='0.0.0.0', port=5000)

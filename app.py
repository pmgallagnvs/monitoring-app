from flask import Flask, render_template, jsonify
import json
import requests
from threading import Timer
from datetime import datetime

app = Flask(__name__)

# Load configuration
with open('config.json') as f:
    config = json.load(f)

urls = config['urls']
check_interval = config['check_interval']

# In-memory storage for statuses
status_data = {url: [] for url in urls}

def check_url(url):
    try:
        response = requests.get(url, timeout=10)
        status = {
            "url": url,
            "code": response.status_code,
            "status": "up" if 200 <= response.status_code < 400 else "down",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except requests.RequestException:
        status = {
            "url": url,
            "code": None,
            "status": "down",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    status_data[url].append(status)
    # Keep only the last 100 records per URL to limit memory usage
    if len(status_data[url]) > 100:
        status_data[url].pop(0)
def schedule_checks():
    for url in urls:
        check_url(url)
    # Schedule the next run
    Timer(check_interval, schedule_checks).start()

# Start the first check
schedule_checks()

@app.route('/')
def index():
    return render_template('index.html', status_data=status_data)

@app.route('/api/status')
def api_status():
    return jsonify(status_data)

if __name__ == '__main__':
    app.run(debug=True)

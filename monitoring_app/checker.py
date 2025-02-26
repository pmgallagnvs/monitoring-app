import json
import os
import csv
import requests
from datetime import datetime
from threading import Timer

# Load configuration
config_path = os.environ.get('MONITORING_CONFIG', 'config.json')
print(f"checker: Using config: {config_path}")
with open(config_path) as f:
    config = json.load(f)

urls = config['urls']
print(f"checker: Using URLs: {urls}")
check_interval = config['check_interval']
print(f"checker: Using check interval: {check_interval}")
timeout = config['timeout']
print(f"checker: Using timeout: {timeout}")
data_dir = os.environ.get('MONITORING_DATA_DIR', 'data')
print(f"checker: Using data directory: {data_dir}")

def check_url(url):
    try:
        response = requests.head(url, timeout=timeout)
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
    
    # Write to CSV
    csv_file = f"{data_dir}/{url.replace('://', '_').replace('/', '_')}.csv"
    os.makedirs(data_dir, exist_ok=True)
    
    write_header = not os.path.exists(csv_file)
    with open(csv_file, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["url", "code", "status", "timestamp"])
        if write_header:
            writer.writeheader()
        writer.writerow(status)

def schedule_checks():
    for url in urls:
        check_url(url)
    Timer(check_interval, schedule_checks).start()

if __name__ == '__main__':
    schedule_checks()

from flask import Flask, render_template, jsonify
import json
import os
import csv
from datetime import datetime

class ReverseProxied(object):
  def __init__(self, app):
      self.app = app
  def __call__(self, environ, start_response):
      script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
      if script_name:
          environ['SCRIPT_NAME'] = script_name
          path_info = environ['PATH_INFO']
          if path_info.startswith(script_name):
              environ['PATH_INFO'] = path_info[len(script_name):]
      # Setting wsgi.url_scheme from Headers set by proxy before app
      scheme = environ.get('HTTP_X_SCHEME', 'https')
      if scheme:
        environ['wsgi.url_scheme'] = scheme
      # Setting HTTP_HOST from Headers set by proxy before app
      remote_host = environ.get('HTTP_X_FORWARDED_HOST', '')
      remote_port = environ.get('HTTP_X_FORWARDED_PORT', '')
      if remote_host and remote_port:
          environ['HTTP_HOST'] = f'{remote_host}:{remote_port}'
      return self.app(environ, start_response)

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

# Load configuration
config_path = os.environ.get('MONITORING_CONFIG', 'config.json')
print(f"Using config: {config_path}")
with open(config_path) as f:
    config = json.load(f)
data_dir = os.environ.get('MONITORING_DATA_DIR', 'data')
print(f"Using data directory: {data_dir}")

urls = config['urls']

def load_status_data():
    status_data = {}
    for url in urls:
        csv_file = f"{data_dir}/{url.replace('://', '_').replace('/', '_')}.csv"
        status_data[url] = []
        
        if os.path.exists(csv_file):
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                status_data[url] = list(reader)[-100:]
    
    return status_data

@app.route('/')
def index():
    return render_template('index.html', status_data=load_status_data())

@app.route('/api/status')
def api_status():
    return jsonify(load_status_data())

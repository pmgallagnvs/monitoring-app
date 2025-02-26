# Monitoring App

Monitor external connections from within Domino. Helpful to gather information about troublesome connections to on-premise systems.

This isn't a very sophisticated monitor. It simply makes HTTP HEAD requests against a list of URLs.

## Get started

1. Create a new project in Domino (called "monitoring-app" or whatever you'd like) and clone this repo into it.
2. Create config.json
    ```
    {
        "urls": [
            "https://aws.amazon.com",
            "https://github.com"
        ],
        "check_interval": 300,
        "timeout": 30
    }
    ```
3. Set two environment variables:
    * `MONITORING_CONFIG` - path to the config.json for the monitoring app, e.g., `/mnt/data/monitoring-app/config.json`
    * `MONITORING_DATA_DIR` - path to the data directory where monitoring results will be stored, e.g., `/mnt/data/monitoring-app`
4. Start a job to run `checker.py`
5. Go to Deployments > App and configure the App to run. The defaults are usually fine. Start the App.
6. View the App to see the monitoring dashboard. It shows the current status as well as a recent history of each URL.
7. The App and Checker job run independently. To update the checker, change the config.json file and restart the checker job.
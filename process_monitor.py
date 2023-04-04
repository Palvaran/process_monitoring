import os
import csv
import time
import psutil
from datetime import datetime

# List of processes to monitor
processes_to_monitor = ["firefox.exe", "chrome.exe", "notepad.exe"]

# CSV file path
csv_path = "C:\\Temp\\process_log.csv"

# Create the Temp folder if it doesn't exist
if not os.path.exists("C:\\Temp"):
    os.makedirs("C:\\Temp")

# Check if the CSV file exists, and create the header if not
if not os.path.isfile(csv_path):
    with open(csv_path, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Process", "Status", "Timestamp"])

# Function to log the process start and stop times
def log_process_status(process_name, status):
    with open(csv_path, "a", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        csv_writer.writerow([process_name, status, timestamp])

# Main loop to continuously check for the specified processes
process_statuses = {}

while True:
    for process in psutil.process_iter(["name"]):
        if process.info["name"].lower() in processes_to_monitor:
            if process.info["name"].lower() not in process_statuses:
                process_statuses[process.info["name"].lower()] = "running"
                log_process_status(process.info["name"], "started")

    for process_name in list(process_statuses.keys()):
        if process_name not in [p.info["name"].lower() for p in psutil.process_iter(["name"])]:
            log_process_status(process_name, "stopped")
            del process_statuses[process_name]

    time.sleep(1)

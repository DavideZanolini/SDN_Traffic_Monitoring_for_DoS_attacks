import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import pandas as pd
from datetime import datetime

SCRIPT_NAME = "cap_main.py"

def log_error(message):
    with open('errors_logs.txt', 'a') as log_file:
        log_file.write(f"{datetime.now()} [{SCRIPT_NAME}]: {message}\n")

def log_message(message):
    with open('logs.txt', 'a') as log_file:
        log_file.write(f"{datetime.now()} [{SCRIPT_NAME}]: {message}\n")

class PcapFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        if event.is_directory:
            return
        if event.src_path.endswith('.pcap'):
            message = f"New pcap file detected: {event.src_path}"
            log_message(message)
            self.process_pcap(event.src_path, script_dir)
        elif event.src_path.endswith('.csv'):
            message = f"New CSV file detected: {event.src_path}"
            log_message(message)
            self.process_csv(event.src_path, script_dir)

    def process_pcap(self, pcap_file, script_dir):
        try:
            log_message(f"Processing pcap file: {pcap_file}")
            subprocess.call(["python3", os.path.join(script_dir, "process_pcap.py"), pcap_file])
        except Exception as e:
            error_message = f"An error occurred while processing pcap file {pcap_file}: {e}"
            log_error(error_message)

    def process_csv(self, csv_file, script_dir):
        try:
            log_message(f"Processing pcap file: {csv_file}")
            subprocess.call(["python3", os.path.join(script_dir, "process_csv.py"), csv_file])
        except Exception as e:
            error_message = f"An error occurred while processing pcap file {csv_file}: {e}"
            log_error(error_message)

    def read_malicious_csv(self, script_dir):
        try:
            csv_file = os.path.join(script_dir, 'malicious_packets.csv')
            if os.path.exists(csv_file):
                data = pd.read_csv(csv_file)
                log_message(f"Read CSV file: {csv_file}")
                log_message(str(data))
                # Call check_malicious_packets.py script
                subprocess.call(["python3", "check_malicius_packets.py", csv_file])
            else:
                log_message(f"CSV file {csv_file} does not exist.")
        except Exception as e:
            error_message = f"An error occurred while reading the CSV file {csv_file}: {e}"
            log_error(error_message)

if __name__ == "__main__":
    tmp_dir = '/tmp'
    event_handler = PcapFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=tmp_dir, recursive=False)
    observer.start()
    log_message(f"Monitoring {tmp_dir} for new pcap and csv files...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    log_message("Stopped the file monitoring service.")
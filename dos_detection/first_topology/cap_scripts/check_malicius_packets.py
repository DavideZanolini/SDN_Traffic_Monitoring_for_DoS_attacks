import pandas as pd
from datetime import datetime, timedelta
import sys

def log_attack(source_ip, count):
    with open('attack_log.txt', 'a') as log_file:
        log_file.write(f"{datetime.now()} - {source_ip} sent {count} malicious packets in the last minute\n")

def detect_attacks(csv_file):
    try:
        # Load the CSV file
        data = pd.read_csv(csv_file)

        # Convert the timestamp column to datetime
        data['timestamp'] = pd.to_datetime(data['timestamp'])

        # Get the current time
        current_time = datetime.now()

        # Filter the data to include only the last minute
        one_minute_ago = current_time - timedelta(minutes=1)
        recent_data = data[data['timestamp'] >= one_minute_ago]

        # Count the occurrences of each source IP
        ip_counts = recent_data['source_ip'].value_counts()

        # Check for IPs with more than 10 occurrences
        for ip, count in ip_counts.items():
            if count > 10:
                log_attack(ip, count)

        # Filter the data to include only the last 10 minutes
        ten_minutes_ago = current_time - timedelta(minutes=10)
        data = data[data['timestamp'] >= ten_minutes_ago]

        # Save the updated data back to the CSV file
        data.to_csv(csv_file, index=False)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_malicious_packets.py <csv_file>")
        sys.exit(1)
    csv_file = sys.argv[1]
    detect_attacks(csv_file)
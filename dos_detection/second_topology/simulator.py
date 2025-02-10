import random
import time
import requests
import subprocess

# List of web server IPs
web_servers = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]
dns_server = "10.0.0.10"

# Function to send an HTTP request to a web server
def send_http_request(server_ip):
    url = f"http://{server_ip}"
    request_type = random.choice(["GET", "POST", "HEAD", "PUT", "PATCH", "OPTIONS", "DELETE"])
    params = {"q": random.choice(["data1", "data2", "data3"])}  # Random query string

    if request_type == "GET":
        requests.get(url, params=params, timeout=2)
    elif request_type == "POST":
        requests.post(url, data={"key": "value"}, timeout=2)
    elif request_type == "HEAD":
        requests.head(url, timeout=2)
    elif request_type == "PUT":
        requests.put(url, data={"key": "updated_value"}, timeout=2)
    elif request_type == "PATCH":
        requests.patch(url, data={"key": "patched_value"}, timeout=2)
    elif request_type == "OPTIONS":
        requests.options(url, timeout=2)
    elif request_type == "DELETE":
        requests.delete(url, timeout=2) 

# Function to send a ping to a server
def send_ping(server_ip):
    packet_size = random.randint(32, 1024)  # Random packet size in bytes
    count = random.randint(1, 3)  # Random number of packets
    subprocess.run(["ping", "-c", str(count), "-s", str(packet_size), server_ip],
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE,
                   text=True)

# Function to perform an nslookup using the DNS server
def perform_nslookup(dns_ip):
    query_name = random.choice(["portal1.com", "portal2.com", "portal3.local"])
    subprocess.run(["nslookup", query_name, dns_ip],
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE,
                   text=True)

# Infinite loop to generate random traffic
try:
    while True:
        # Randomly choose a server and traffic type
        traffic_type = random.choice(["http", "ping", "nslookup"])
        if traffic_type == "http":
            # HTTP request to a random web server
            target_server = random.choice(web_servers)
            send_http_request(target_server)
        elif traffic_type == "ping":
            # Ping a random server (web server or DNS server)
            target_server = random.choice(web_servers + [dns_server])
            send_ping(target_server)
        elif traffic_type == "nslookup":
            # Perform an nslookup using the DNS server
            perform_nslookup(dns_server)

        # Wait for a random time between 0.5 and 3 seconds
        time.sleep(random.uniform(0.2, 3))

except KeyboardInterrupt:
    print("Traffic simulation stopped.")

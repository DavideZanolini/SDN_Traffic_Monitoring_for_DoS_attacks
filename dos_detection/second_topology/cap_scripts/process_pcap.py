import csv
import os
from scapy.all import rdpcap, TCP, IP
from datetime import datetime

SCRIPT_NAME = "process_pcap.py"

def log_error(message):
    with open('errors_logs.txt', 'a') as log_file:
        log_file.write(f"{datetime.now()} [{SCRIPT_NAME}]: {message}\n")

def log_message(message):
    with open('logs.txt', 'a') as log_file:
        log_file.write(f"{datetime.now()} [{SCRIPT_NAME}]: {message}\n")

def pcap_to_csv(pcap_file, csv_file, exclude_non_tcp=False):
    try:
        log_message(f"Reading pcap file: {pcap_file}")
        packets = rdpcap(pcap_file)
        total_packets = len(packets)
        log_message(f"Total packets read: {total_packets}")
        
        non_tcp_packets_excluded = 0
        processed_packets = 0
        
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "id", "source_ip", "dur", "spkts", "sbytes", "sttl", "swin", "stcpb", 
                "dtcpb", "rate", "pps", "bpp", "ttl_ratio", "tcp_diff", "swin_interaction"
            ])
            
            for i, packet in enumerate(packets):
                if exclude_non_tcp and not packet.haslayer(TCP):
                    non_tcp_packets_excluded += 1
                    continue
                
                processed_packets += 1
                pkt_id = processed_packets
                
                # Extract basic features
                dur = getattr(packet, "time", "N/A")
                spkts = 1  
                sbytes = len(packet)
                sttl = getattr(packet[IP], "ttl", "N/A") if packet.haslayer(IP) else "N/A"
                swin = getattr(packet[TCP], "window", "N/A") if packet.haslayer(TCP) else "N/A"
                stcpb = getattr(packet[TCP], "seq", "N/A") if packet.haslayer(TCP) else "N/A"
                dtcpb = getattr(packet[TCP], "ack", "N/A") if packet.haslayer(TCP) else "N/A"
                source_ip = packet[IP].src if packet.haslayer(IP) else "N/A"
                
                # Calculate derived features using safe conversions

                # Convert duration to float
                try:
                    dur_float = float(dur)
                except (ValueError, TypeError):
                    dur_float = None

                # Rate (bytes per second)
                if dur_float is None or dur_float == 0:
                    rate = "N/A"
                else:
                    rate = sbytes / dur_float

                # Packets per second (pps)
                if dur_float is None or dur_float == 0:
                    pps = "N/A"
                else:
                    pps = spkts / dur_float

                # Bytes per packet (bpp)
                if spkts == 0:
                    bpp = "N/A"
                else:
                    bpp = sbytes / spkts

                # TTL ratio (sttl/dur)
                try:
                    sttl_float = float(sttl)
                except (ValueError, TypeError):
                    sttl_float = None
                if sttl_float is None or dur_float is None or dur_float == 0:
                    ttl_ratio = "N/A"
                else:
                    ttl_ratio = sttl_float / dur_float

                # TCP difference (dtcpb - stcpb)
                try:
                    stcpb_float = float(stcpb)
                except (ValueError, TypeError):
                    stcpb_float = None
                try:
                    dtcpb_float = float(dtcpb)
                except (ValueError, TypeError):
                    dtcpb_float = None
                if stcpb_float is None or dtcpb_float is None:
                    tcp_diff = "N/A"
                else:
                    tcp_diff = dtcpb_float - stcpb_float

                # swin_interaction (swin * stcpb)
                try:
                    swin_float = float(swin)
                except (ValueError, TypeError):
                    swin_float = None
                if swin_float is None or stcpb_float is None:
                    swin_interaction = "N/A"
                else:
                    swin_interaction = swin_float * stcpb_float

                writer.writerow([
                    pkt_id, source_ip, dur, spkts, sbytes, sttl, swin, stcpb, dtcpb, rate, pps, bpp, ttl_ratio, tcp_diff, swin_interaction
                ])

        log_message(f"Total packets processed: {processed_packets}")
        log_message(f"Non-TCP packets excluded: {non_tcp_packets_excluded}")

        # Delete the pcap file after processing
        os.remove(pcap_file)
        log_message(f"Deleted pcap file: {pcap_file}")

    except Exception as e:
        log_error(f"An error occurred while processing pcap file {pcap_file}: {e}")

if __name__ == "__main__":
    log_message("Processing pcap files...")
    tmp_dir = '/tmp'
    try:
        files = os.listdir(tmp_dir)
        pcap_files = [f for f in files if f.endswith('.pcap') and os.path.isfile(os.path.join(tmp_dir, f))]
        
        for pcap_file in pcap_files:
            pcap_path = os.path.join(tmp_dir, pcap_file)
            exclude_non_tcp = True
            csv_file = os.path.splitext(pcap_file)[0] + ("_tcp_only.csv" if exclude_non_tcp else ".csv")
            csv_path = os.path.join(tmp_dir, csv_file)
            pcap_to_csv(pcap_path, csv_path, exclude_non_tcp)
            log_message(f"CSV file saved as {csv_path}")
            os.remove(pcap_file)
            log_message(f"Deleted pcap file: {pcap_file}")
    except Exception as e:
        log_error(f"An error occurred: {e}")
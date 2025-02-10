import csv
import os
import random
from scapy.all import rdpcap, TCP, IP

def pcap_to_csv(pcap_file, csv_file, exclude_non_tcp=False):
    print(f"Reading pcap file: {pcap_file}")
    packets = rdpcap(pcap_file)
    total_packets = len(packets)
    print(f"Total packets read: {total_packets}")
    
    non_tcp_packets_excluded = 0
    processed_packets = 0
    normal_packets = 0
    malicious_packets = 0
    
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "id", "source_ip", "dur", "spkts", "sbytes", "sttl", "swin", "stcpb", "dtcpb", "rate", "pps", "bpp", "ttl_ratio", "tcp_diff", "swin_interaction", "label"
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
            label = "1" if packet[TCP].flags & 0x20 else "0"  # URG flag is 0x20
            
            if label == "0":
                normal_packets += 1
            else:
                malicious_packets += 1
            
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
                pkt_id, source_ip, dur, spkts, sbytes, sttl, swin, stcpb, dtcpb, rate, pps, bpp, ttl_ratio, tcp_diff, swin_interaction, label
            ])

    print(f"Total packets processed: {processed_packets}")
    print(f"Non-TCP packets excluded: {non_tcp_packets_excluded}")
    print(f"Normal packets (label 0): {normal_packets}")
    print(f"Malicious packets (label 1): {malicious_packets}")
    print(f"CSV file saved as {csv_file}")

if __name__ == "__main__":
    pcap_file = input("Enter the name of the pcap file (located in ../data/captures/): ")
    pcap_path = os.path.join("../data/captures/", pcap_file)

    exclude_non_tcp = input("Do you want to exclude non-TCP packets? (yes/no): ").strip().lower() == 'yes'

    csv_file = os.path.splitext(pcap_file)[0] + ("_tcp_only.csv" if exclude_non_tcp else ".csv")
    csv_path = os.path.join("../data/csv_files/", csv_file)

    pcap_to_csv(pcap_path, csv_path, exclude_non_tcp)
    print(f"CSV file saved as {csv_path}")
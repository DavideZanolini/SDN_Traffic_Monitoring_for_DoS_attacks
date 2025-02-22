# DoS Detection

This folder contains scripts for detecting Denial-of-Service (DoS) attacks in a simulated network environment using ComNetsEmu. The project is divided into two different networks, each with its own folder. The main files in each folder create the network and generate pcap files every 30 seconds. The scripts are designed to run on ComNetsEmu.

## Folder Structure

- `first_topology/`: Contains scripts and configurations for the first network.
- `second_topology/`: Contains scripts and configurations for the second network.
- `requirements.txt`: Lists the Python libraries required to run the scripts.

## Requirements

- Python 3.8 or higher
- Required Python libraries (listed in `requirements.txt`)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/DavideZanolini/SDN_Traffic_Monitoring_for_DoS_attacks.git
   cd SDN_Traffic_Monitoring_for_DoS_attacks/dos_detection
   ```

2. Install the required Python libraries:
   ```sh
   pip install -r requirements.txt
   ```

## Topology of the networks created

### Topology 1:

![Topology 1](media/network1.png)

### Topology 2:

![Topology 2](media/network2.png)

## Usage

### Note

Our team had some issues with the use of joblib to load the model to make the prediction, due to an issue with numpy, that is required by the joblib library. In `cap_scripts` you can find `process_csv.py`, this file works without any problems but it isn't able to make any prediction on the data. In `process_csv_joblib.py` you will find the file that causes the numpy issue (numpy._core: module not found).

### Setting Up ComNetsEmu

1. **Install ComNetsEmu**:
   Follow the installation instructions from the [ComNetsEmu GitHub repository](https://github.com/stevelorenz/comnetsemu).

2. **Run the Network Simulation**:
   Navigate to the respective network folder (`first_topology` or `second_topology`) and run the main file to create the network.

### Script Workflow

1. **PCAP File Generation**:
   The main file in each network folder creates a network and generates a pcap file every 30 seconds.

2. **PCAP File Processing**:
   When a pcap file is detected, the `process_pcap.py` script is called by `cap_main`. This script generates a CSV file from the pcap file.

3. **CSV File Processing**:
   When a CSV file is detected, the `process_csv.py` script is called. This script uses the trained model to find malicious packets in the CSV file and writes the source IP of the host sending malicious packets to `malicious_packets.csv`.

4. **Malicious Packet Checking**:
   The `check_malicious_packets.py` script is called to check if a host has sent more than 10 malicious packets in the last minute. If so, it writes the information to `attack_logs`.

### Running Attacks

To run attacks, you can use the `attack_launcher.py` script. For example, on `r1` you can run:
```sh
sudo apt-get install hping3
sudo python3 attack_launcher.py
```
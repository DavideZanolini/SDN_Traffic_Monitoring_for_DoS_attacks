# SDN Traffic Monitoring for DoS Attacks

This project was developed as part of the Networking 2 course at the University of Trento. It focuses on integrating cybersecurity principles with networking to create a simulated infrastructure capable of reconnaissance and protection against Denial-of-Service (DoS) attacks. By leveraging machine learning and network analysis techniques, the project aims to identify and mitigate threats in real time, ensuring a secure and adaptable system.

## Project Overview

The main objectives of this project are:
- **Traffic Monitoring**: Monitor network traffic in real-time to detect anomalies and potential DoS attacks.
- **Machine Learning**: Use machine learning algorithms to analyze network traffic patterns and predict potential threats.
- **DoS Attack Mitigation** (work in progress): Implement strategies to mitigate the impact of detected DoS attacks.
- **Simulated Infrastructure**: Create a simulated network environment to test and validate the effectiveness of the implemented solutions.

## Features

- **Real-time Traffic Analysis**: Continuously monitor network traffic for signs of DoS attacks.
- **Machine Learning Models**: Train and deploy machine learning models to classify and predict network traffic anomalies.
- **Automated Response**: Automatically respond to detected threats to minimize the impact of DoS attacks.

## Getting Started

To get started with the project, follow the instructions in the `ml_model_training/README.md` file to set up your environment and run the necessary scripts.

## Folder Structure of ml_model_training

- `data/`: Contains the data used for training and testing the machine learning models.
- `ml_model_training/`: Includes scripts and instructions for training the machine learning models.
- `tools/`: Contains utility scripts for processing data and testing the models.

## Folder Structure of dos_detection

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
   cd SDN_Traffic_Monitoring_for_DoS_attacks
   ```

## How to use our project

This project is divided in two parts: ml_model_training and dos_detection. In each folder you will find a guide on how to train the model and how to use it on comnetsemu.

## Using ComNetsEmu and Mininet

We used ComNetsEmu and Mininet to create a simulated network environment for testing and validating our solutions. ComNetsEmu extends Mininet with additional features for network experimentation, making it ideal for our project.

### Setting Up ComNetsEmu

1. **Install ComNetsEmu**:
   Follow the installation instructions from the [ComNetsEmu GitHub repository](https://github.com/stevelorenz/comnetsemu).

2. **Copy DoS detection**:
    Copy the dos_detection folder in you virtual machine and follow the instruction written on the readme contained in that folder

## Future Works

- **Mitigation System**: We plan to add a mitigation system where `check_malicious_packets.py` can send a REST API request to the controller to take action against malicious hosts.
- **Model Improvement**: We aim to improve our machine learning model to ensure better generalization and performance on unseen data.

## Contributors

- Alessandro Paladin ()
- Matteo Lorenzoni ()
- Davide Zanolini (zanolinidavide@gmail.com)
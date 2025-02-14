import pandas as pd
import json
import sys
import os
import numpy as np
from datetime import datetime
from collections import Counter
import joblib

SCRIPT_NAME = "process_csv.py"

def log_error(message):
    try:
        with open('errors_logs.txt', 'a') as log_file:
            log_file.write(f"{datetime.now()} [{SCRIPT_NAME}]: {message}\n")
    except Exception as e:
        print(f"An error occurred while logging an error: {e}")

def log_message(message):
    try:
        with open('logs.txt', 'a') as log_file:
            log_file.write(f"{datetime.now()} [{SCRIPT_NAME}]: {message}\n")
    except Exception as e:
        print(f"An error occurred while logging a message: {e}")

def load_csv(csv_file):
    try:
        data = pd.read_csv(csv_file)
        log_message(f"Loaded CSV file: {csv_file}")
        return data
    except Exception as e:
        error_message = f"An error occurred while loading the CSV file: {e}"
        log_error(error_message)
        sys.exit(1)

def load_model(model_file):
    try:
        model = joblib.load(model_file)
        log_message(f"Loaded model: {model_file}")
        return model
    except Exception as e:
        error_message = f"An error occurred while loading the model: {e}"
        log_error(error_message)
        sys.exit(1)

def load_scaler_params(scaler_params_file):
    try:
        with open(scaler_params_file, 'r') as f:
            scaler_params = json.load(f)
        log_message(f"Loaded scaler parameters: {scaler_params_file}")
        return scaler_params
    except Exception as e:
        error_message = f"An error occurred while loading the scaler parameters: {e}"
        log_error(error_message)
        sys.exit(1)

def scale_features(features, scaler_params):
    mean = np.array(scaler_params["mean"])
    scale = np.array(scaler_params["scale"])
    return (features - mean) / scale

def predict(data, model, scaler_params):
    try:
        # Extract the features used during training.
        features = data[["id", "dur", "spkts", "sttl", "swin", 
                         "stcpb", "dtcpb", "pps", "ttl_ratio", "tcp_diff", "swin_interaction"]]
        
        features_array = features.to_numpy()
        scaled_features = scale_features(features_array, scaler_params)
        predictions = model.predict(scaled_features)
        
        data['prediction'] = predictions
        log_message("Made predictions on the data")
        return data
    except Exception as e:
        error_message = f"An error occurred while making predictions: {e}"
        log_error(error_message)
        sys.exit(1)

def update_malicious_csv(data, output_file):
    try:
        # Add a timestamp column to the data
        data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Filter the data to include only malicious packets (assuming class "1" is malicious)
        malicious_data = data[data['prediction'] == 1][['source_ip', 'timestamp']]
        
        if not malicious_data.empty:
            if os.path.exists(output_file):
                # Append to the existing CSV file
                malicious_data.to_csv(output_file, mode='a', header=False, index=False)
            else:
                # Create a new CSV file
                malicious_data.to_csv(output_file, index=False)
            log_message(f"Updated malicious packets CSV file: {output_file}")
        else:
            log_message("No malicious packets found.")
    except Exception as e:
        error_message = f"An error occurred while updating the malicious packets CSV file: {e}"
        log_error(error_message)
        sys.exit(1)

if __name__ == "__main__":
    print("Starting process_csv.py")
    ensure_log_files_exist()
    log_message("Processing CSV file...")
    
    if len(sys.argv) != 2:
        log_error("Invalid number of arguments")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = sys.argv[1]
    model_file = os.path.join(script_dir, "trained_model.joblib")
    scaler_params_file = os.path.join(script_dir, "scaler_params.json")
    output_file = os.path.join(script_dir, "malicious_packets.csv")

    # Ensure the output file exists (creates a header if needed)
    if not os.path.exists(output_file):
        with open(output_file, 'w') as f:
            f.write('source_ip,timestamp\n')

    data = load_csv(csv_file)
    model = load_model(model_file)
    scaler_params = load_scaler_params(scaler_params_file)
    result = predict(data, model, scaler_params)

    # Update the malicious packets CSV file with the new predictions.
    update_malicious_csv(result, output_file)

    # Delete the processed CSV file.
    os.remove(csv_file)
    log_message(f"Deleted CSV file: {csv_file}")
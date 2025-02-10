import pandas as pd
import json
import sys
import os
import numpy as np
from datetime import datetime, timedelta
from collections import Counter

SCRIPT_NAME = "process_csv.py"

def ensure_log_files_exist():
    try:
        if not os.path.exists('logs.txt'):
            with open('logs.txt', 'w') as log_file:
                log_file.write(f"{datetime.now()} [{SCRIPT_NAME}]: Log file created\n")
        if not os.path.exists('errors_logs.txt'):
            with open('errors_logs.txt', 'w') as log_file:
                log_file.write(f"{datetime.now()} [{SCRIPT_NAME}]: Error log file created\n")
    except Exception as e:
        print(f"An error occurred while ensuring log files exist: {e}")
        sys.exit(1)

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
    """
    Loads the Random Forest JSON model.
    The JSON is assumed to be a list of tree structures.
    """
    try:
        with open(model_file, 'r') as f:
            model = json.load(f)
        log_message(f"Loaded JSON model: {model_file}")
        return model
    except Exception as e:
        error_message = f"An error occurred while loading the JSON model: {e}"
        log_error(error_message)
        sys.exit(1)

def predict_tree(tree, X):
    """
    Traverses a single decision tree (from the JSON model) using feature vector X.
    The tree structure uses:
      - "feature": index of the feature used at the node (-2 for leaf)
      - "threshold": threshold for decision
      - "children_left"/"children_right": indices of child nodes
      - "values": class distribution at the node
    """
    node = 0  # start at the root node
    # A feature value of -2 indicates a leaf node.
    while tree["feature"][node] != -2:
        feature_index = tree["feature"][node]
        threshold = tree["threshold"][node]
        if X[feature_index] <= threshold:
            node = tree["children_left"][node]
        else:
            node = tree["children_right"][node]
    # Return the class with the highest vote at the leaf node.
    return np.argmax(tree["values"][node])

def predict_forest(forest, X):
    """
    Runs a prediction over all trees in the forest and returns the majority vote.
    """
    predictions = [predict_tree(tree, X) for tree in forest]
    return Counter(predictions).most_common(1)[0][0]

def predict(data, model):
    try:
        # Extract the features used during training.
        # (Adjust the list below if your training used a different set of features.)
        features = data[["id", "dur", "spkts", "sttl", "swin", 
                         "stcpb", "dtcpb", "pps", "ttl_ratio", "tcp_diff", "swin_interaction"]]
        
        features_array = features.to_numpy()
        predictions = []
        for row in features_array:
            pred = predict_forest(model, row)
            predictions.append(pred)
        
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
    # Use the JSON file containing the Random Forest structure.
    model_file = os.path.join(script_dir, "forest_model.json")
    output_file = os.path.join(script_dir, "malicious_packets.csv")

    # Ensure the output file exists (creates a header if needed)
    if not os.path.exists(output_file):
        with open(output_file, 'w') as f:
            f.write('source_ip,timestamp\n')

    data = load_csv(csv_file)
    model = load_model(model_file)
    result = predict(data, model)

    # Update the malicious packets CSV file with the new predictions.
    update_malicious_csv(result, output_file)

    # Delete the processed CSV file.
    os.remove(csv_file)
    log_message(f"Deleted CSV file: {csv_file}")
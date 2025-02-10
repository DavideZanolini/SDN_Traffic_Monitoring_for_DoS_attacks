import pandas as pd
import numpy as np
import joblib
import json

def load_csv(csv_file):
    return pd.read_csv(csv_file)

def load_scaler_params(scaler_params_file):
    with open(scaler_params_file, 'r') as f:
        return json.load(f)

def scale_features(features, scaler_params):
    mean = np.array(scaler_params["mean"])
    scale = np.array(scaler_params["scale"])
    return (features - mean) / scale

def predict(data, model, scaler_params):
    features = data[["id", "source_ip", "dur", "spkts", "sbytes", "sttl", "swin", "stcpb", "dtcpb", 
            "rate", "pps", "bpp", "ttl_ratio", "tcp_diff", "swin_interaction", "label"]]
    features_array = features.to_numpy()
    scaled_features = scale_features(features_array, scaler_params)
    predictions = model.predict(scaled_features)
    return predictions

if __name__ == "__main__":

    # Update these paths with the actual file paths
    csv_file = "path/to/your/csv_file.csv"
    model_file = "path/to/your/model_file.joblib"
    scaler_params_file = "path/to/your/scaler_params.json"

    data = load_csv(csv_file)
    model = joblib.load(model_file)
    scaler_params = load_scaler_params(scaler_params_file)
    data['prediction'] = predict(data, model, scaler_params)
    
    normal_packets = data[data['prediction'] == 0].shape[0]
    malicious_packets = data[data['prediction'] == 1].shape[0]
    
    print(f"Normal packets: {normal_packets}")
    print(f"Malicious packets: {malicious_packets}")

    # Debugging information
    print("First 10 predictions:")
    print(data[['id', 'prediction']].head(10))
    print("First 10 rows of features:")
    print(data[["id", "source_ip", "dur", "spkts", "sbytes", "sttl", "swin", "stcpb", "dtcpb", 
            "rate", "pps", "bpp", "ttl_ratio", "tcp_diff", "swin_interaction", "label"]].head(10))
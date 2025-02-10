import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib
import json

def train_and_save_forest(train_data_path, test_data_path=None, model_save_path="forest_model.joblib", scaler_params_path="scaler_params.json"):
    """
    Trains a Random Forest classifier and saves its structure as a joblib file.
    """
    print("Loading training dataset...")
    train_df = pd.read_csv(train_data_path)

    if test_data_path:
        print("Loading test dataset...")
        test_df = pd.read_csv(test_data_path)
    else:
        print("Splitting training dataset into training and testing sets...")
        train_df, test_df = train_test_split(train_df, test_size=0.2, random_state=42)

    # Select features and target variable
    features = ["id", "dur", "spkts", "sttl", "swin", "stcpb", "dtcpb", 
                "pps", "ttl_ratio", "tcp_diff", "swin_interaction"]
    target = 'label'

    X_train = train_df[features]
    y_train = train_df[target]
    X_test = test_df[features]
    y_test = test_df[target]

    # Normalize the data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Save the scaler parameters
    scaler_params = {
        "mean": scaler.mean_.tolist(),
        "scale": scaler.scale_.tolist()
    }
    with open(scaler_params_path, 'w') as f:
        json.dump(scaler_params, f)

    print("Creating and training the Random Forest classifier...")
    model = RandomForestClassifier(n_estimators=10, random_state=42)  # 10 trees
    model.fit(X_train, y_train)

    print("Making predictions on the test set...")
    y_pred = model.predict(X_test)

    print("Evaluating model performance...")
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred, zero_division=0)

    print(f"Random Forest model accuracy: {accuracy}")
    print(f"Random Forest model precision: {precision}")
    print(f"Random Forest model recall: {recall}")
    print(f"Random Forest model F1 score: {f1}")
    print("Confusion Matrix:")
    print(conf_matrix)
    print("Classification Report:")
    print(class_report)

    # Save the model as a joblib file
    print("Saving the model as a joblib file...")
    joblib.dump(model, model_save_path)
    print(f"Random Forest model saved to {model_save_path}")

if __name__ == "__main__":

    data_dir = "../data/csv_files/"  

    train_file_name = input("Enter the name of the training CSV file: ")
    train_data_path = os.path.join(data_dir, train_file_name)

    test_file_name = input("Enter the name of the test CSV file: ")
    test_data_path = os.path.join(data_dir, test_file_name)

    print(f"\nTraining model with data from: {train_data_path}")
    print(f"Testing model with data from: {test_data_path}")

    model_save_path = "forest_model.joblib"
    scaler_params_path = "scaler_params.json"
    train_and_save_forest(train_data_path, test_data_path, model_save_path, scaler_params_path)
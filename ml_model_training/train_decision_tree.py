import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import os

def train_and_evaluate_model(train_data_path, test_data_path=None):
    """
    Trains a Decision Tree classifier on network traffic data and evaluates its performance on a separate test set.

    Args:
        train_data_path: Path to the CSV file containing the training data.
        test_data_path: Path to the CSV file containing the test data (optional).

    Returns:
        Trained Decision Tree classifier model.
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
    features = ['dur', 'spkts', 'sbytes', 'sttl', 'swin', 'stcpb', 'dtcpb']
    target = 'label'

    X_train = train_df[features]
    y_train = train_df[target]
    X_test = test_df[features]
    y_test = test_df[target]

    print("Creating and training the Decision Tree classifier...")
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    print("Making predictions on the test set...")
    y_pred = model.predict(X_test)

    print("Evaluating model performance...")
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred)

    print(f"Decision Tree model accuracy: {accuracy}")
    print(f"Decision Tree model precision: {precision}")
    print(f"Decision Tree model recall: {recall}")
    print(f"Decision Tree model F1 score: {f1}")
    print("Confusion Matrix:")
    print(conf_matrix)
    print("Classification Report:")
    print(class_report)

    return model

if __name__ == "__main__":
    data_dir = "../data/csv_files/"  # Replace with the actual directory path

    train_file_name = input("Enter the name of the training CSV file: ")
    train_data_path = os.path.join(data_dir, train_file_name)

    use_same_file = input("Do you want to use the same file for testing? (yes/no): ").strip().lower()

    if use_same_file == 'yes':
        test_data_path = None
    else:
        test_file_name = input("Enter the name of the test CSV file: ")
        test_data_path = os.path.join(data_dir, test_file_name)

    print(f"Training model with data from: {train_data_path}")
    if test_data_path:
        print(f"Testing model with data from: {test_data_path}")
    else:
        print("Using a split of the training data for testing")

    trained_model = train_and_evaluate_model(train_data_path, test_data_path)
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_feature_correlation(csv_file):
    # Load the CSV file
    df = pd.read_csv(csv_file)
    
    # Drop non-numeric columns (if any)
    df_numeric = df.select_dtypes(include=['number'])

    # Compute correlation matrix
    correlation_matrix = df_numeric.corr()

    # Plot heatmap of correlations
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Feature Correlation Matrix")
    plt.show()

if __name__ == "__main__":
    # User input for CSV file path
    csv_file = input("Enter the path to the CSV file: ")
    plot_feature_correlation(csv_file)

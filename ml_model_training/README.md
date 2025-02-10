# Model Training

This folder of the project includes scripts for training a Random Forest classifier to predict network traffic patterns. The guide below explains how to set up and use a virtual environment to run `train_random_forest.py`. In order to use the script, you need to create the CSV files that contain the training and testing sets. To do so, place the pcap files that you created in `../data/captures`. Then follow the steps below:

## 1. Create a Virtual Environment

First, create a virtual environment in your project directory. Open a terminal and navigate to your project directory, then run:

```sh
python -m venv venv
```

## 2. Activate the Virtual Environment

- **Windows**: 
  ```sh
  .\venv\Scripts\activate
  ```
- **MacOS**: 
  ```sh
  source venv/bin/activate
  ```

## 3. Install Required Libraries

```sh
pip install -r requirements.txt
```

## 4. Run `process_pcap.py`

```sh
python tools/process_pcap.py
```

Now you will find the dataset in `../data/csv_files`. Use this file to train the random forest model.

## 5. Run `train_random_forest.py`

```sh
python train_random_forest.py
```

# How to Check the Performance of Your Model

In the `tools` folder, you can find `test_model.py` to check if the model you created is functioning. Firstly, you need to change:

```sh
csv_file = "file_of_the_data" 
model_file = "file_of_the_model"
```

in your script with the actual directories of your files.
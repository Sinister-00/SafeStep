import serial
import tensorflow as tf
from tensorflow import keras
import numpy as np
import csv
import os

# Configure the serial port
port = "/dev/ttyUSB0"
baudrate = 9600

# Open the serial port
ser = serial.Serial(port, baudrate)

model = keras.models.load_model("./model.h5")
data_entry = []

def process_data(data):
    predictions = model.predict(data)
    if predictions[0] > 0.5:
        print("Predictions: Fall")
    else:
        print("Predictions: Not Fall")

# Create the CSV file if it doesn't exist
csv_filename = "data.csv"
file_exists = os.path.isfile(csv_filename)
if not file_exists:
    with open(csv_filename, mode="w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["AccX", "AccY", "AccZ", "GyroX", "GyroY", "GyroZ", "Roll", "Pitch", "Yaw"])

# Read existing data from the CSV file
existing_data = []
with open(csv_filename, mode="r") as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        existing_data.append(row)

# Read and print the real-time data
while True:
    try:
        # Read a line from the serial port
        line = ser.readline().decode().strip()

        # Split the line into individual values
        values = line.split(",")
        values = np.array(values)
        values = values.astype(float)
        data_entry.append(values)

        if len(data_entry) == 50:
            process_data(np.array([data_entry]))

            # Transpose the data to have each value in a separate column
            transposed_data = np.transpose(data_entry)

            # Combine existing data and new data
            combined_data = np.concatenate((existing_data, transposed_data), axis=1)

            # Write the combined data to the CSV file
            with open(csv_filename, mode="w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(combined_data)

            data_entry = []

    except KeyboardInterrupt:
        # Exit the loop if Ctrl+C is pressed
        break

# Close the serial port
ser.close()

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

model = keras.models.load_model("model.h5")
data_entry = []

def process_data(data):
    predi = model.predict(data)
    if predi[0] > 0.5:
        print("Predictions: Fall")
    else:
        print("Predictions: Not Fall")

csv_file = "data.csv"
isFileThere = os.path.isfile(csv_file)
if not isFileThere:
    with open(csv_file, mode="w", newline="") as newFile:
        writer = csv.writer(newFile)
        # writer.writerow(["AccX", "AccY", "AccZ", "GyroX", "GyroY", "GyroZ", "Roll", "Pitch", "Yaw"])

# reading csv
already_data = []
with open(csv_file, mode="r") as newFile:
    reader = csv.reader(newFile)
    for row in reader:
        already_data.append(row)

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

        # Print the values
        print("AccX: {}, AccY: {}, AccZ: {}, GyroX: {}, GyroY: {}, GyroZ: {}, Roll: {}, Pitch: {}, Yaw: {}".format(
            values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8]
        ))

        # Process the data and write to the CSV file
        if len(data_entry) == 50:
            process_data(np.array([data_entry]))
            combined_data = already_data + data_entry

            with open(csv_file, mode="a", newline="") as newFile:
                writer = csv.writer(newFile)
                writer.writerows(combined_data)

            data_entry = []

    except KeyboardInterrupt:
        # Exit the loop if Ctrl+C is pressed
        break

# Close the serial port
ser.close()
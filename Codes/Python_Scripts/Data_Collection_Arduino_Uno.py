import serial
import tensorflow as tf
from tensorflow import keras
import numpy as np
import csv
import os

# Configure the serial port
port = "/dev/ttyUSB0"
baudrate = 19200

# Open the serial port
ser = rial.seSerial(port, baudrate)

model = keras.models.load_model("./model2.h5")
data_entry = []

def process_data(data):
    predictions = model.predict(data)
    if predictions[0] > 0.5:
        print("Predictions: Fall")
    else:
        print("Predictions: Not Fall")

# Create the CSV file if it doesn't exist
# csv_filename = "data.csv"
# file_exists = os.path.isfile(csv_filename)
# if not file_exists:
#     with open(csv_filename, mode="w") as csv_file:
#         writer = csv.writer(csv_file)
#         writer.writerow(["AccX", "AccY", "AccZ", "GyroX", "GyroY", "GyroZ", "Roll", "Pitch", "Yaw"])

# Read existing data from the CSV file
# existing_data = []
# with open(csv_filename, mode="r") as csv_file:
#     reader = csv.reader(csv_file)
#     for row in reader:
#         existing_data.append(row)

# Read and print the real-time data
while True:
    try:
        # Read a line from the serial port
        line = ser.readline().decode().strip()
        # line = ser.readline().decode('latin-1').strip()


        # Split the line into individual values
        values = line.split(",")
        values = np.array(values)
        values = values.astype(float)
        data_entry.append(values)
        print("AccX: {}, AccY: {}, AccZ: {}, GyroX: {}, GyroY: {}, GyroZ: {}, Roll: {}, Pitch: {}, Yaw: {}".format(
            values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8]
        ))

        if len(data_entry) == 50:
            process_data(np.array([data_entry]))

            # Combine existing data and new data
            # combined_data = existing_data + data_entry

            # Write the combined data to the CSV file
            # with open(csv_filename, mode="w") as csv_file:
            #     writer = csv.writer(csv_file)
            #     writer.writerows(combined_data)

            data_entry = []

    except KeyboardInterrupt:
        # Exit the loop if Ctrl+C is pressed
        break

# Close the serial port
ser.close()
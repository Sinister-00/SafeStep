import socket
import time
import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
import csv

HOST = '192.168.43.151'  # Replace with the IP address of your ESP8266
PORT = 8888
RECEIVE_FREQUENCY = 0.1  # Data receive frequency in seconds (e.g., every 100 milliseconds)

data_entry = []

csv_file = "data_fall_back_delete.csv"
isFileThere = os.path.isfile(csv_file)
if not isFileThere:
    with open(csv_file, mode="w", newline="") as newFile:
        writer = csv.writer(newFile)

# reading csv
already_data = []
with open(csv_file, mode="r") as newFile:
    reader = csv.reader(newFile)
    for row in reader:
        already_data.append(row)

def receive_data():
    global data_entry  # Declare data_entry as a global variable

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            start_time = time.time()

            # Receive data
            data = s.recv(1024)

            # Process received data
            if data:
                data = data.decode().strip()
                lines = data.split("\n")  # Split data into lines

                for line in lines:
                    if line:
                        values = line.split(",")  # Split each line into values
                        if len(values) != 9:  # Skip lines with incorrect number of values
                            continue
                        values = np.array(values)
                        try:
                            values = values.astype(float)
                        except ValueError:
                            continue

                        data_entry.append(values)  # Append values to data_entry

                        if len(values) == 9:
                            print("AccX: {}, AccY: {}, AccZ: {}, GyroX: {}, GyroY: {}, GyroZ: {}, Roll: {}, Pitch: {}, Yaw: {}".format(
                                values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8]
                            ))
                            print("")  # Print a new line after 9 values

            # Write data_entry to CSV file
            if data_entry:
                with open(csv_file, mode="a", newline="") as newFile:
                    writer = csv.writer(newFile)
                    writer.writerows(data_entry)
                data_entry = []  # Clear the data_entry list after writing to the file

            # # Calculate remaining time until the next data receive
            # elapsed_time = time.time() - start_time
            # remaining_time = max(0, RECEIVE_FREQUENCY - elapsed_time)

            # # Wait for the remaining time
            # time.sleep(remaining_time)

if __name__ == '__main__':
    receive_data()
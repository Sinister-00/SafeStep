import socket
import time
import tensorflow as tf
from tensorflow import keras
import numpy as np

HOST = '192.168.43.151'  # Replace with the IP address of your ESP8266
PORT = 8888
RECEIVE_FREQUENCY = 0.1  # Data receive frequency in seconds (e.g., every 100 milliseconds)

model = keras.models.load_model("model2.h5")
data_entry = []

def process_data(data):
    data_tensor = tf.convert_to_tensor(data, dtype=tf.float32)  # Convert to TensorFlow tensor
    predi = model.predict(data_tensor)
    if predi[0] > 0.5:
        print("Prediction: Fall")
    else:
        print("Prediction: Not Fall")

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

                        if len(data_entry) == 50:
                            data_array = np.array(data_entry)
                            process_data(data_array.reshape((1, 50, 9)))
                            data_entry = []  # Reset data_entry after processing

                        if len(values) == 9:
                            print("AccX: {}, AccY: {}, AccZ: {}, GyroX: {}, GyroY: {}, GyroZ: {}, Roll: {}, Pitch: {}, Yaw: {}".format(
                                values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8]
                            ))
                            print("")  # Print a new line after 9 values

if __name__ == '__main__':
    receive_data()
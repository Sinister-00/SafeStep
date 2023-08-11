import socket
import time
import numpy as np

HOST = '192.168.43.151'  # Replace with the IP address of your ESP8266
PORT = 8888
RECEIVE_FREQUENCY = 0.1  # Data receive frequency in seconds (e.g., every 100 milliseconds)

EXPECTED_VALUES_COUNT = 9  # Update with the expected number of values in each received line

def receive_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            start_time = time.time()

            # Receive data
            data = s.recv(1024)

            # Process received data
            if data:
                line = data.decode().strip()
                values = line.split(",")

                if len(values) == EXPECTED_VALUES_COUNT:
                    formatted_values = [float(value) if value != '' else float('nan') for value in values]

                    print("AccX: {:.2f}, AccY: {:.2f}, AccZ: {:.2f}, GyroX: {:.2f}, GyroY: {:.2f}, GyroZ: {:.2f}, Roll: {:.2f}, Pitch: {:.2f}, Yaw: {:.2f}".format(
                        *formatted_values
                    ))
                else:
                    continue
                    # missing_values_count = EXPECTED_VALUES_COUNT - len(values)
                    # missing_values = ["N/A"] * missing_values_count
                    # formatted_values = values + missing_values

                    # print("Received data has incorrect number of values. Expected: {}, Received: {}. Data: AccX: {}, AccY: {}, AccZ: {}, GyroX: {}, GyroY: {}, GyroZ: {}, Roll: {}, Pitch: {}, Yaw: {}".format(
                    #     EXPECTED_VALUES_COUNT, len(values), *formatted_values
                    # ))

            # Calculate remaining time until the next data receive
            elapsed_time = time.time() - start_time
            remaining_time = max(0, RECEIVE_FREQUENCY - elapsed_time)

            # Wait for the remaining time
            time.sleep(remaining_time)

if __name__ == '__main__':
    receive_data()

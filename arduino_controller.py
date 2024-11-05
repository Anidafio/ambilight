import serial
import time
import struct

class ArduinoController:
    def __init__(self, port, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = serial.Serial(port, baudrate)
        time.sleep(2)  # Wait for Arduino to initialize

    def send_color_data(self, color_data):
        flat_color_data = [value for rgb in color_data for value in rgb]
        data_bytes = struct.pack(f"{len(flat_color_data)}B", *flat_color_data)
        self.serial_connection.write(data_bytes)

    def close(self):
        self.serial_connection.close()
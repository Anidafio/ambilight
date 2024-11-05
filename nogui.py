import time
import dxcam
import numpy as np
from PIL import Image
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

# Initialize dxcam with default settings
camera = dxcam.create(device_idx=0, output_idx=0)

# Screen dimensions (adjust these based on your monitor resolution)
screen_width = 3840  # Replace with your screen width
screen_height = 2160  # Replace with your screen height

# Zone configuration
leds_horizontal = 18
leds_vertical = 10
target_fps = 30
edge_step = 50
edge_thickness = 50  # Adjust thickness of the edge strips as needed

arduino_controller = ArduinoController("COM4")

# Define zones for each LED (skipping corners)
def calculate_led_zones():
    zones = []
    # Calculate bottom row (horizontal)
    for i in reversed(range(leds_horizontal)):
        x = int(edge_step + i * (screen_width - 2 * edge_step) / leds_horizontal)
        y = screen_height - edge_thickness
        width = int((screen_width - 2 * edge_step) / leds_horizontal)
        height = edge_thickness
        zones.append((x, y, width, height))

    # Calculate left column (vertical)
    for i in reversed(range(leds_vertical)):
        x = 0
        y = int(edge_step + i * (screen_height - 2 * edge_step) / leds_vertical)
        width = edge_thickness
        height = int((screen_height - 2 * edge_step) / leds_vertical)
        zones.append((x, y, width, height))

    # Calculate top row (horizontal)
    for i in range(leds_horizontal):
        x = int(edge_step + i * (screen_width - 2 * edge_step) / leds_horizontal)
        y = 0
        width = int((screen_width - 2 * edge_step) / leds_horizontal)
        height = edge_thickness
        zones.append((x, y, width, height))

    # Calculate right column (vertical)
    for i in range(leds_vertical):
        x = screen_width - edge_thickness
        y = int(edge_step + i * (screen_height - 2 * edge_step) / leds_vertical)
        width = edge_thickness
        height = int((screen_height - 2 * edge_step) / leds_vertical)
        zones.append((x, y, width, height))

    return zones

# Calculate average color for each zone in a frame
def analyze_frame(frame, zones):
    color_data = []
    for x, y, width, height in zones:
        # Crop each zone from the frame
        zone = frame[y:y + height, x:x + width]
        # Calculate the average color for the zone
        avg_color = np.mean(zone, axis=(0, 1))
        color_data.append(tuple(int(c) for c in avg_color))
    return color_data

def run_ambient_light_analyzer():
    zones = calculate_led_zones()
    frame_duration = 1.0 / target_fps

    while True:
        start_time = time.time()
        
        frame = None
        while frame is None:
            frame = camera.grab()  # Capture frame directly from GPU
            
        # Analyze the frame for edge zone colors
        color_data = analyze_frame(frame, zones)
        
        arduino_controller.send_color_data(color_data)

        end_time = time.time()
        elapsed_time = end_time - start_time
        fps = 1.0 / elapsed_time if elapsed_time > 0 else 0

        print(f"Processed frame in {elapsed_time:.3f} seconds (FPS: {fps:.2f})")
        
        # Sleep to maintain target FPS
        time_to_wait = frame_duration - elapsed_time
        if time_to_wait > 0:
            time.sleep(time_to_wait)


run_ambient_light_analyzer()
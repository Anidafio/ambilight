import time
import threading
from camera_handler import CameraHandler
from zone_analyzer import analyze_frame
from arduino_controller import ArduinoController

class AmbientLightController:
    def __init__(self, screen_width, screen_height, target_fps, arduino_port, zones):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.target_fps = target_fps
        self.zones = zones
        self.running = False

        # Initialize components
        self.camera_handler = CameraHandler()
        self.arduino_controller = ArduinoController(port=arduino_port)
        self.frame_duration = 1.0 / target_fps
        self.thread = None

    def start(self):
        """Start the ambient light processing in a separate thread."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run)
            self.thread.start()

    def stop(self):
        """Stop the ambient light processing and join the thread."""
        if self.running:
            self.running = False
            color_data = []
            for x, y, width, height in self.zones:
                color_data.append((0, 0, 0))
            self.arduino_controller.send_color_data(color_data)
            self.thread.join()
            self.arduino_controller.close()  # Ensure Arduino connection is closed

    def run(self):
        """Main loop for capturing frames, analyzing colors, and sending data."""
        try:
            while self.running:
                start_time = time.time()

                # Capture frame
                frame = self.camera_handler.capture_frame()

                # Analyze the frame for edge zone colors
                color_data = analyze_frame(frame, self.zones)

                # Send color data to Arduino
                self.arduino_controller.send_color_data(color_data)

                # Calculate FPS and wait if needed
                end_time = time.time()
                elapsed_time = end_time - start_time
                fps = 1.0 / elapsed_time if elapsed_time > 0 else 0
                print(f"Processed frame in {elapsed_time:.3f} seconds (FPS: {fps:.2f})")

                # Sleep to maintain target FPS
                time_to_wait = self.frame_duration - elapsed_time
                if time_to_wait > 0:
                    time.sleep(time_to_wait)
        finally:
            self.arduino_controller.close()
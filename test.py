import time
import dxcam
import random
from PIL import Image

# Initialize dxcam with default settings
camera = dxcam.create(device_idx=0, output_idx=0)

def test_capture_performance(frames=60):
    start_time = time.time()
    saved_frame = random.randint(0, frames - 1)  # Randomly choose a frame to save

    for i in range(frames):
        frame = None
        while frame is None:
            frame = camera.grab()  # Capture directly from GPU
        
        
        if frame is not None and i == saved_frame:
            # Save the captured frame as a PNG to verify
            img = Image.fromarray(frame)
            img.save("random_screenshot.png")
            print(f"Saved a screenshot at frame {i} as 'random_screenshot.png'")
        

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time to capture {frames} frames: {elapsed_time:.3f} seconds")
    print(f"Average time per frame: {elapsed_time / frames:.3f} seconds")
    print(f"Average FPS: {frames / elapsed_time:.2f}")

test_capture_performance(30)
import dxcam

class CameraHandler:
    def __init__(self, device_idx=0, output_idx=0):
        self.camera = dxcam.create(device_idx=device_idx, output_idx=output_idx)

    def capture_frame(self):
        frame = None
        while frame is None:
            frame = self.camera.grab()  # Capture frame directly from GPU
        return frame
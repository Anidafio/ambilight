import numpy as np

def analyze_frame(frame, zones):
    color_data = []
    for x, y, width, height in zones:
        # Crop each zone from the frame
        zone = frame[y:y + height, x:x + width]
        # Calculate the average color for the zone
        avg_color = np.mean(zone, axis=(0, 1))
        color_data.append(tuple(int(c) for c in avg_color))
    return color_data
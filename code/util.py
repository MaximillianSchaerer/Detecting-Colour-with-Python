import cv2
import numpy as np

def get_limits(colour):
    
    # Extract the hue value
    color = np.uint8([[colour]])
    hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
    hue = int(hsv_color[0][0][0])  # Hue, Saturation, Value (HSV)
    
    # Define hue range (±5)
    hue_range = 5
    lower_hue = hue - hue_range
    upper_hue = hue + hue_range

    # Ensure the hue values are within the valid range
    lower_limit1 = np.array([max(0, lower_hue), 80, 80], dtype=np.uint8)  # Ensure lower hue does not go below 0
    lower_limit2 = None

    upper_limit1 = np.array([min(179, upper_hue), 200, 200], dtype=np.uint8)  # Ensure upper hue does not exceed 179 (OpenCV max hue value)
    upper_limit2 = None

    # If the hue wraps around, create a second limit
    if lower_hue < 0:
            lower_limit2 = np.array([179 + lower_hue, 100, 100], dtype=np.uint8)  # ex: 179 + (-5) = 174
            upper_limit2 = np.array([179, 255, 255], dtype=np.uint8)

    elif upper_hue > 179:
            lower_limit2 = np.array([0, 100, 100], dtype=np.uint8)
            upper_limit2 = np.array([upper_hue - 179, 255, 255], dtype=np.uint8)

    return (lower_limit1, upper_limit1), (lower_limit2, upper_limit2)
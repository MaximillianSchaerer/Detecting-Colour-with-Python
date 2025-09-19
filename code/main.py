import cv2

# OpenCV Video Capture Example
from util import get_limits
from PIL import Image
# This script captures video from a file and processes each frame to isolate a specific color (yellow in this case).

# OpenCV uses BGR: Blue, Green, Red
color = [0, 0, 255]
(lower_limit1, upper_limit1), (lower_limit2, upper_limit2) = get_limits(color)  # Get the HSV limits for the color

# Open the video file
cap = cv2.VideoCapture('videos/RedBirb.mp4')  

# Check if the video was opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while cap.isOpened(): 
    
    # Checks for the next video frame and returns a bool
    ret, frame = cap.read()  

    # If no frame is returned, break the loop
    if not ret:  
        break

    # Convert the current frame HSV color space
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # create the first mask
    mask1 = cv2.inRange(hsvFrame, lower_limit1, upper_limit1) 

    # Create the second mask if hue wrapping occurred
    mask2 = None
    if lower_limit2 is not None:
        mask2 = cv2.inRange(hsvFrame, lower_limit2, upper_limit2) 

    # Combine the masks if both exist
    combo_mask = mask1 if mask2 is None else cv2.bitwise_or(mask1, mask2)  

    # Draw a rectangle around the detected color
    PIL_mask = Image.fromarray(combo_mask) # Convert to PIL Image for bounding box detection
    bbox = PIL_mask.getbbox()  
    if bbox is not None: 
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 5)  # Draw the rectangle in green

    # Display the original frame
    frame = cv2.resize(frame, (640 , 480))  # (width, height)
    cv2.imshow('Bounding Box', frame)  

    # Display the mask
    combo_mask = cv2.resize(combo_mask, (640 , 480))  # (width, height) 
    cv2.imshow('Mask', combo_mask)
    
    # Exit if 'q' is pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):  #waitKey controls the frame rate in this case
        print("Video playback stopped by user.")
        break

cap.release()  # Release the catpure object
cv2.destroyAllWindows()  # Close all OpenCV windows
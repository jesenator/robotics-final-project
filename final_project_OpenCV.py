# final_project_OpenCV.py
# Note: ChatGPT helped write parts of this code
import cv2
import numpy as np
from collections import deque
from scipy.spatial.distance import euclidean
import paho.mqtt.client as mqtt
import time
from my_secrets import ADAFRIUT

# Initialize Deque to store points with no maxlen
path = deque()


# Function to calculate total path length
def calculate_path_length(path):
    return sum([euclidean(path[i], path[i + 1]) for i in range(len(path) - 1)])


# The maximum path length for 100%
max_path_length = 3000.0  # units

# Start capturing video
cap = cv2.VideoCapture(1)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected")
    else:
        print("Failed to connect, return code %d\n", rc)


username = ADAFRIUT["username"]
password = ADAFRIUT["password"]
broker_address = "io.adafruit.com"
client = mqtt.Client("pycharm server")
client.on_connect = on_connect

client.username_pw_set(username, password)
client.connect(broker_address, 1883)
client.loop_start()


def send_to_dashboard(percent):
    print("sending")
    client.publish(f"{username}/feeds/progress_bar", str(percent))


dashboard_interval = 3

next_time = time.time() + dashboard_interval
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of blue color in HSV
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([140, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Apply Gaussian blur to the mask to reduce noise
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)

        # Compute the center of the contour
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            path.append((cX, cY))  # Append to the right for the drawing order

            # Draw the contour and center of the shape on the image
            cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 2)
            cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)

    # Draw the path
    for i in range(1, len(path)):
        cv2.line(frame, path[i - 1], path[i], (0, 0, 255), 2)

    # Calculate the path length
    path_length = calculate_path_length(path)

    # Calculate the percentage of the max path length
    path_percent = (path_length / max_path_length) * 100
    # Ensure the percentage does not exceed 100%
    path_percent = min(path_percent, 100.0)

    print(f"Path Length: {path_length:.2f}, Percentage of max path length: {path_percent:.2f}%")
    if time.time() > next_time:
        send_to_dashboard(path_percent)
        next_time = time.time() + dashboard_interval
    # Display the resulting frame
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
client.loop_stop()
client.disconnect()

cap.release()
cv2.destroyAllWindows()

# robotics-final-project

## Libraries used

### For final_pico.py:
mqtt: Used for handling MQTT (Message Queuing Telemetry Transport) communication. It's a lightweight messaging protocol for small sensors and mobile devices, optimized for high-latency or unreliable networks.

time: This module provides various time-related functions. It's standard in Python and used for handling time-related tasks like delays (sleep).

network, ubinascii: These are specific to MicroPython, used for network-related operations. network handles network configurations, and ubinascii is used for ASCII to binary conversions.

secrets: This module is used for managing secrets, like passwords or API keys, in this case storing Wi-Fi and Adafruit credentials.

urequests: A MicroPython library similar to Python's requests library, used for making HTTP requests.

machine: This is a MicroPython module used to interact with the hardware components of a microcontroller, like pins, PWM, I2C, and ADC.

math: A standard Python library for mathematical functions.

### For final_project_OpenCV.py:

cv2 (OpenCV): This is the OpenCV library used for computer vision tasks, like image and video processing.

numpy: A fundamental package for scientific computing in Python. It's commonly used with OpenCV for manipulating arrays (images, in this case).

collections: This module provides alternatives to Python’s general-purpose built-in containers. deque from collections is used here for efficient removal and appending of elements.

scipy.spatial.distance: This is a part of the SciPy library and is used here specifically for calculating Euclidean distance, useful in path-length computations.

paho.mqtt.client: This is the Paho MQTT client, used for handling MQTT communications in Python. It's similar to the mqtt library in the first script but more suited for standard Python environments.

my_secrets: Similar to the secrets module in the first script, used for managing sensitive information like credentials (there is some module, I forget which, that uses a secrets.py file internally so you can't have a file with the same name in the same directory)


Note: This was written the the help of ChatGPT

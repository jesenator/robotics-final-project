# final_pico.py
import mqtt
import time
import network, ubinascii
from secrets import Tufts_Wireless as wifi
from secrets import ADAFRIUT
import urequests
from machine import Pin, PWM, I2C, ADC
import math

fan_servo = PWM(Pin(15))
fan_servo.freq(50)
high_pin = Pin(26, Pin.OUT)
high_pin.on()
cel_pin = Pin(19, Pin.OUT)
far_pin = Pin(20, Pin.OUT)


def connect_wifi(wifi):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
    print("MAC " + mac)

    station.connect(wifi['ssid'], wifi['pass'])
    while not station.isconnected():
        time.sleep(1)
    print('Connection successful')
    print(station.ifconfig())


# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print("Connected")
#     else:
#         print("Failed to connect, return code %d\n", rc)

def num_to_range(num, inMin, inMax, outMin, outMax):
    return outMin + (float(num - inMin) / float(inMax - inMin) * (outMax
                                                                  - outMin))


def sControl(cent):
    return int((float(cent) / 100) * 1800 + 4800)


def toggle_leds(toggle):
    if toggle:
        cel_pin.on()
        far_pin.off()
    else:
        far_pin.on()
        cel_pin.off()



connect_wifi(wifi)
def whenCalled(topic, msg):
    topic = topic.decode()
    msg = msg.decode()
    print(topic)
    print(msg)
    if topic == "jesenator/feeds/go_button" and msg == "1":
        toggle_leds(False)
        print("red")
        fan_servo.duty_u16(sControl(100))
        time.sleep(1)
        fan_servo.duty_u16(sControl(-100))
    if topic == "jesenator/feeds/progress_bar" and msg == "100.0":
        print("green")
        toggle_leds(True)

broker_address = "io.adafruit.com"
username = ADAFRIUT["username"]
password = ADAFRIUT["password"]
client_name = "pico client"

client = mqtt.MQTTClient(client_name, broker_address, user=username, password=password, keepalive=1000)
client.connect()
client.set_callback(whenCalled)

client.subscribe(f"{username}/feeds/go_button")
client.subscribe(f"{username}/feeds/progress_bar")

print("mqtt connected")
toggle_leds(True)
time.sleep(.3)
toggle_leds(False)
time.sleep(.3)
toggle_leds(True)


while True:
    client.check_msg()

mins_till_next_read = 1
next_read_time = time.ticks_ms() + mins_till_next_read * 60 * 1000

client.disconnect()


 

import uos
import machine
import micropython
import network
from machine import ADC, Pin, Timer
from micropython import const
from umqtt.robust import MQTTClient
from time import sleep, localtime, time, sleep_ms
import gc
import ntptime
import sys
import wind_speed
import mqtt
import rainfall
import wind_direction

'''WiFi Parameters'''
WIFI_NAME = b"Extensity"
WIFI_PASSWORD = b"password1"

'''Access Point Parameters'''
ACCESS_POINT_NAME = b"Weather Station"
ACCESS_POINT_PASSWORD = b"password"

'''Weather Sensor Constants'''
WIND_DIRECTION_PIN = const(0)
WIND_SPEED_PIN = const(12)
RAINFALL_AMOUNT_PIN = const(13)

'''MQTT Server Parameters'''
MQTT_CLIENT_ID = b"Weather_Station_Vcom"
MQTT_BROKER = b"c1.vxt.net"
MQTT_USER = ""
MQTT_PASSWORD = ""
KEEP_ALIVE_DURATION = const(300)
MQTT_PORT = const(42883)

'''MQTT Publish Parameters'''
MQTT_TOPIC = b"vectracom/weather/all"

'''Connect ESP8266 to WiFi'''
def connectWiFi():
    time_now = time()
    print("Connecting to WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_NAME, WIFI_PASSWORD)
    while not sta_if.isconnected() or (time()-time_now>10):
        print(".", end="")
        sleep(0.1)
    print(" Connected!")
    return sta_if

'''Make the ESP8266 an access point'''
def makeAccessPoint():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ACCESS_POINT_NAME, password=ACCESS_POINT_PASSWORD)

    while ap.active() == False:
      pass
    print('Connection successful')
    print(ap.ifconfig())
    return ap

try:
    wifi_client = connectWiFi()  # Connect to WiFi
    access_point = makeAccessPoint() # Make access point
except OSError:
    wifi_client = connectWiFi()  # Connect to WiFi
    access_point = makeAccessPoint() # Make access point

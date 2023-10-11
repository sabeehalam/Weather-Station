import uos
import machine
import micropython
import network
from machine import ADC, Pin, Timer
from micropython import const
from umqtt.robust import MQTTClient
from time import sleep, localtime, time, sleep_ms
import uselect as select
import usocket as socket
import gc
import settings_server
import request_to_json
import webpage
import ntptime
import sys
import wind_speed
import mqtt
import rainfall
import wind_direction

'''Access Point Parameters'''
ACCESS_POINT_NAME = b"Weather Station"
ACCESS_POINT_PASSWORD = b"password"

'''Connect ESP8266 to WiFi'''
def connectWiFi(WIFI_NAME, WIFI_PASSWORD):
    time_now = time()
    print("Connecting to WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_NAME, WIFI_PASSWORD)
    while sta_if.isconnected()==0 and (time()-time_now <= 10):
#         print(time()-time_now > 10)
        sleep(0.1)
    if sta_if.isconnected():
        print("Connected to WiFi!")
    return sta_if

'''Make the ESP8266 an access point'''
def makeAccessPoint():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ACCESS_POINT_NAME, password=ACCESS_POINT_PASSWORD)
    while ap.active() == False:
      pass
    print('Access Point enabled successfully')
    print(ap.ifconfig())
    return ap

'''Weather Sensor Constants'''
WIND_DIRECTION_PIN = const(0)
WIND_SPEED_PIN = const(12)
RAINFALL_AMOUNT_PIN = const(13)

parameters = request_to_json.loadParameters()

'''WiFi Parameters'''
try:
    WIFI_NAME = parameters["Wifi-Name"]
    WIFI_PASSWORD = parameters["Wifi-Password"]
except (ValueError, NameError, KeyError):
    WIFI_NAME = "Embedded"
    WIFI_PASSWORD = "password1"

'''MQTT Server Parameters'''
try:
    MQTT_CLIENT_ID = parameters["MqttClientID"]
except (ValueError, NameError, KeyError):
    MQTT_CLIENT_ID = "Weather Station"

try:
    MQTT_BROKER = parameters["MqttBroker"]
except (ValueError, NameError, KeyError):
    MQTT_BROKER = "c1.vxt.net"

try:
    MQTT_USER = parameters["MqttUSER"]
except (ValueError, NameError, KeyError):
    MQTT_USER = ""

try:
    MQTT_PASSWORD = parameters["MqttPassword"]
except (ValueError, NameError, KeyError):
    MQTT_PASSWORD = ""
    
try:    
    KEEP_ALIVE_DURATION = int(parameters["KeepAlive"])
except (ValueError, NameError, KeyError):
    KEEP_ALIVE_DURATION = 0
    
try:
    MQTT_PORT = int(parameters["MqttPort"])
except (ValueError, NameError, KeyError):
    MQTT_PORT = 42883
    
'''MQTT Publish Parameters'''
try:
    MQTT_TOPIC = parameters["MqttPublishTopic"]
    MQTT_PUBLISH_TIME_GAP = int(parameters["MqttPublishTime"])
except (ValueError, NameError, KeyError):
    MQTT_TOPIC = "vectracom/weather/all"
    MQTT_PUBLISH_TIME_GAP = 10
    
'''Web Server Parameters'''
try:
    WEB_SERVER = parameters["WebServer"]
    WEB_PORT = int(parameters["WebPort"])
except (ValueError, NameError, KeyError):
    WEB_SERVER = "192.168.4.1"
    WEB_PORT = 80
    
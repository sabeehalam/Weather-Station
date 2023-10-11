# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
from umqtt.simple import MQTTClient
import sonofmqtt
import micropython
import network
import time
import gc
#uos.dupterm(None, 1) # disable REPL on UART(0)
#import webrepl
#webrepl.start()
gc.collect()

'''WiFi Parameters'''
WIFI_NAME     = "Extensity"
WIFI_PASSWORD = "password1"

'''Connect ESP8266 to WiFi''' 
def connect_WiFi():
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_NAME, WIFI_PASSWORD)
    while not sta_if.isconnected():
      print(".", end="")
      time.sleep(0.1)
    print(" Connected!")
    return sta_if

try:
    wifi_client = connect_WiFi() #Connect to WiFi
except OSError: wifi_client = connect_WiFi() 
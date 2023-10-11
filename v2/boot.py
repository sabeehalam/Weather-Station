# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
import micropython
import network
from machine import ADC, Pin, Timer
from micropython import const
from umqtt.robust import MQTTClient
import network
from time import sleep, time_ns, localtime, time, sleep_ms
import gc
import ntptime
#uos.dupterm(None, 1) # disable REPL on UART(0)
#import webrepl
#webrepl.start()
gc.collect()

'''WiFi Parameters'''
WIFI_NAME     = "Extensity"
WIFI_PASSWORD = "password1"

'''Weather Sensor Constants'''
WIND_DIRECTION_PIN  = const(0)
WIND_SPEED_PIN      = const(14)
RAINFALL_AMOUNT_PIN = const(13)
RESET_PIN			= const(1)

'''MQTT Server Parameters'''
MQTT_CLIENT_ID      = b"Weather_Station_Vcom"
MQTT_BROKER         = b"192.168.120.164"
MQTT_USER           = b""
MQTT_PASSWORD       = b""
KEEP_ALIVE_DURATION = 300
MQTT_PORT           = 1883

'''MQTT Publish Parameters'''
MQTT_TOPIC_RAIN      = b"weather/rain"
MQTT_TOPIC_WIND      = b"weather/wind_speed"
MQTT_TOPIC_DIR       = b"weather/direction"
MQTT_TOPIC_GUST      = b"weather/gust"
MQTT_TOPIC_RAIN_HOUR = b"weather/rain_hour"
MQTT_TOPIC_RAIN_DAY  = b"weather/rain_day"
MQTT_TOPIC_RAIN_WEEK = b"weather/rain_week"

'''Time Parameters'''
UTC_OFFSET = 5 * 60 * 60

'''Connect ESP8266 to WiFi''' 
def connectWiFi():
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_NAME, WIFI_PASSWORD)
    while not sta_if.isconnected():
      print(".", end="")
      time.sleep(0.1)
    print(" Connected!")
    return sta_if

'''Connect to MQTT Broker'''
def connectMQTTBroker():
    global MQTT_CON_FLAG
    try:
        print("Connecting to MQTT server... ", end="")
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD, \
                        keepalive = KEEP_ALIVE_DURATION, port = MQTT_PORT)
        client.connect()
        print("Connected!")
#         client.set_callback(MQTTCallback)
        return client
    
    except Exception as e:
        print("Error in mqtt connect: [Exception] %s: %s" % (type(e).__name__, e))
        sleep(0.5) # to brake the loop    


try:
    wifi_client = connectWiFi() #Connect to WiFi
    mqtt_client = connectMQTTBroker() #Connect to MQTT
except OSError:
    wifi_client = connect_WiFi()
    mqtt_client = connectMQTTBroker()
    
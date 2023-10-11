'''Import Libraries'''
from machine import ADC, Pin, Timer
from umqtt.simple import MQTTClient
import micropython
import network
import time
from time import sleep, time_ns, localtime, time
import gc
import ntptime


'''Weather Sensor Constants'''
WIND_DIRECTION_PIN  = 0
WIND_SPEED_PIN      = 14
RAINFALL_AMOUNT_PIN = 13
SPEED_AVG_COUNT     = 15

'''Global Variables'''
prev_hour           = 0
prev_day            = 0
prev_week           = 0
prev_month          = 0
last_value          = 0
pulse_duration      = 0
start_time          = 0
stop_time           = 0
speed_counter       = 0
avg_speed           = 0
prev_avg_speed      = 0
rain_state          = False
calc_start_time     = 0
new_speed_available = 0
rain_counter_hour   = 0
rain_counter_day    = 0
rain_counter_week   = 0
rain_counter_month  = 0
prev_speed_time     = 0
speed_time          = 0 

'''MQTT Server Parameters'''
MQTT_CLIENT_ID      = b"Weather_Station_Vcom"
MQTT_BROKER         = b"broker.mqtt-dashboard.com"
MQTT_USER           = b""
MQTT_PASSWORD       = b""
KEEP_ALIVE_DURATION = 300
MQTT_PORT           = 1883

'''MQTT Publish Parameters'''
MQTT_TOPIC_RAIN      = b"weather/rain"
MQTT_TOPIC_WIND      = b"weather/wind"
MQTT_TOPIC_DIR       = b"weather/direction"
MQTT_TOPIC_GUST      = b"weather/gust"
MQTT_TOPIC_RAIN_HOUR = b"weather/rain_hour"
MQTT_TOPIC_RAIN_DAY  = b"weather/rain_day"
MQTT_TOPIC_RAIN_WEEK = b"weather/rain_week"
MQTT_TOPIC_RAIN_MONTH= b"weather/rain_month"

'''Time Parameters'''
UTC_OFFSET = 5 * 60 * 60

MQTT_CON_FLAG = False #mqtt connection flag
PINGRESP_RCV_FLAG = True #indicator that we received PINGRESP
PING_INTERVAL = 20

next_ping_time = 0 

def ping_reset():
    global next_ping_time
    next_ping_time = time() + PING_INTERVAL #we use time.time() for interval measuring interval
    print("Next MQTT ping at", next_ping_time)

def ping(mqtt_client):
    mqtt_client.ping()
    ping_reset()

def check(mqtt_client):
    global next_ping_time
    global MQTT_CON_FLAG
    global PINGRESP_RCV_FLAG
        
    if (time() >= next_ping_time): #we use time.time() for interval measuring interval
        if not PINGRESP_RCV_FLAG :
            MQTT_CON_FLAG = False #we have not received an PINGRESP so we are disconnected
            print("No PINGRESP received so broker disconnected.")
        
        else:
            print("MQTT ping at", time())
            ping(mqtt_client)
            PINGRESP_RCV_FLAG = False
    
    response = mqtt_client.check_msg()
    if(response == b"PINGRESP") :
        PINGRESP_RCV_FLAG = True
        print("PINGRESP")
    

'''Connect to MQTT Broker'''
def connect_MQTT_Broker():
    global MQTT_CON_FLAG
    global PINGRESP_RCV_FLAG
    global next_ping_time
    try:
            print("Connecting to MQTT server... ", end="")
            client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD, \
                        keepalive = KEEP_ALIVE_DURATION, port = MQTT_PORT)
            client.connect()
            print("Connected!")
            MQTT_CON_FLAG = True
            PINGRESP_RCV_FLAG = True
            next_ping_time = time() + PING_INTERVAL
            
    except Exception as e:
            print("Error in mqtt connect: [Exception] %s: %s" % (type(e).__name__, e))
            sleep(0.5) # to brake the loop
    return client


'''Publish Variables'''
def publish_Wind_Speed(wind_speed):
    mqtt_client.publish(MQTT_TOPIC_WIND, str(wind_speed), qos = 1)
  
def publish_Wind_Direction(direction):
    mqtt_client.publish(MQTT_TOPIC_DIR, direction, qos = 1)
        
def publish_Check_Rain():
    mqtt_client.publish(MQTT_TOPIC_RAIN, "It's raining", qos = 1)
    
def publish_Gust():
    mqtt_client.publish(MQTT_TOPIC_GUST, "It's a gust", qos = 1)
    
def publish_Rain(topic, rain_volume):
    mqtt_client.publish(topic, str(rain_volume), qos = 1)
       
       
'''Calculate the average speed of wind'''
def average_Speed(wind_speed, direction):
    global speed_counter
    global avg_speed
    global prev_avg_speed
    global speed_time
    global prev_speed_time
    
    if(speed_counter != SPEED_AVG_COUNT):
        avg_speed += wind_speed
        speed_counter += 1
        return
    
    if(speed_counter == SPEED_AVG_COUNT):
        avg_speed = round(avg_speed / SPEED_AVG_COUNT)
        speed_time = time()
        sleep(0.05)

        if((avg_speed != prev_avg_speed) or (speed_time - prev_speed_time >=10)):
            print("Wind Speed", wind_speed)
            print("Average Speed", avg_speed)
            publish_Wind_Speed(avg_speed)
            publish_Wind_Direction(direction)
            prev_avg_speed = avg_speed
            prev_speed_time = speed_time
            speed_counter = 0
            avg_speed = 0
          
        if(wind_speed > (avg_speed + 2)):
            publish_Gust()
            prev_speed_time = speed_time
            sleep(0.05)            
    return
        

'''Calculate the speed of the anemometer'''
def calculate_Speed(pulse_time):
    Ar = 2.4
    if(pulse_time == 0):
        return 0
    else: speed = round(Ar * (1 / (pulse_time / 1000000000)), 0)
    return speed


'''Calculate the duration of the pulse'''
def wind_Speed_Pulse(wind_sensor):
    global last_value
    global calc_start_time
    global stop_time
    global start_time
    global new_speed_available
    current_value = wind_sensor.value()
    if(last_value != current_value):
        if(current_value == 1):
            calc_start_time = start_time
            stop_time = time_ns()
            start_time = stop_time
            new_speed_available = 1
    last_value = current_value
                  

'''Calculate the direction of the wind and map to directions'''
def wind_Direction(dir_sensor):

    if(dir_sensor>2.6 and dir_sensor<2.7):
        direction = "north"
    elif(dir_sensor>1.6 and dir_sensor<1.7):
        direction = "north-east"
    elif(dir_sensor>0.3 and dir_sensor<0.4):
        direction = "east"
    elif(dir_sensor>0.6 and dir_sensor<0.7):
        direction = "south-east"
    elif(dir_sensor>0.96 and dir_sensor<1.06):
        direction = "south"
    elif(dir_sensor>2.1 and dir_sensor<2.2):
        direction = "south-west"
    elif(dir_sensor>3.15 and dir_sensor<3.25):
        direction = "west"
    elif(dir_sensor < 2.95 or dir_sensor > 3.05):
        direction = "north-east"
    else: direction = "north-west"
    
    return direction


'''Check if it is raining'''
def check_Rain(rain_sense):
    global rain_state
    rain_state = True
    
    
'''Calculate the rainfall per hour'''       
def calculate_Rain_Hour():
    global rain_counter_hour
    rain_volume_hour = rain_counter_hour * 0.2794
    if(rain_volume_hour != 0):
        print("Rain volume per hour: ",rain_volume_hour)
        sleep(0.05)
        publish_Rain(MQTT_TOPIC_RAIN_HOUR, rain_volume_hour)
    rain_counter_hour = 0
    
    
'''Calculate the rainfall per day'''       
def calculate_Rain_Day():
    global rain_counter_day
    rain_volume_day = rain_counter_day * 0.2794
    if(rain_volume_day != 0):
        print("Rain volume per day: ",rain_volume_day)
        sleep(0.05)
        publish_Rain(MQTT_TOPIC_RAIN_DAY, rain_volume_day)
    rain_counter_day = 0
    
    
'''Calculate the rainfall per week'''       
def calculate_Rain_Week():
    global rain_counter_week
    rain_volume_week = rain_counter_week * 0.2794
    if(rain_volume_week != 0):
        print("Rain volume per week: ",rain_volume_week)
        sleep(0.05)
        publish_Rain(MQTT_TOPIC_RAIN_WEEK, rain_volume_week)
    rain_counter_week = 0
    
    
'''Calculate the rainfall per hour'''       
def calculate_Rain_Month():
    global rain_counter_month
    rain_volume_month = rain_counter_month * 0.2794
    if(rain_volume_month != 0):
        print("Rain volume per month: ",rain_volume_month)
        sleep(0.05)
        publish_Rain(MQTT_TOPIC_RAIN_MONTH, rain_volume_month)
    rain_counter_month = 0
    

'''Main function for calling all functions'''
try:
    wind_sensor = Pin(WIND_SPEED_PIN, Pin.IN,Pin.PULL_UP)
    rain_sensor = Pin(RAINFALL_AMOUNT_PIN, Pin.IN, Pin.PULL_UP)
    wind_sensor.irq(trigger = Pin.IRQ_RISING, handler = wind_Speed_Pulse)
    rain_sensor.irq(trigger = Pin.IRQ_FALLING, handler = check_Rain)
    mqtt_client = connect_MQTT_Broker()
    sleep(0.05)
    while True:
        
        check(mqtt_client)
#         if(MQTT_CON_FLAG == False):
#             try:
#                 mqtt_client = 0
#                 mqtt_client = connect_MQTT_Broker()
#             except: OSError: connect_MQTT_Broker()
            
        '''Read the time variables'''
        time_now = localtime(ttime() + UTC_OFFSET)
        hour  = time_now[3]
        day   = time_now[2]
        week  = time_now[6]
        month = time_now[1]
        
        dir_sensor = (ADC(WIND_DIRECTION_PIN).read()) * (3.3 / 1023.0)
        direction = wind_Direction(dir_sensor)
        sleep(0.05)
        
        if(new_speed_available == 1):
            pulse_duration = stop_time - calc_start_time
            speed = calculate_Speed(pulse_duration)
            average_Speed(speed, direction)
            new_speed_available = 0
            
        if(rain_state == True):
            sleep(0.4)
            print("Its raining")
            sleep(0.05)
#             publish_Check_Rain()
            rain_counter_hour += 1
            rain_counter_day += 1
            rain_counter_week += 1
            rain_counter_month += 1
            rain_state = False
                
        if(hour != prev_hour):
            calculate_Rain_Hour()
            prev_hour = hour
            
        if(day != prev_day):
            calculate_Rain_Day()
            prev_day = day
            
        if(week == 6):
            calculate_Rain_Week()
            
        if(month != prev_month):
            calculate_Rain_Month()
            prev_month = month
            
        gc.collect()
        
except KeyboardInterrupt:
    print("STOP!!")
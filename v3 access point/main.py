'''Interrupt handler for wind speed to calculate pulse duration'''
def windSpeedHandler(pin):
  global wind_interrupt
  wind_interrupt = 1

'''Interrupt handler for wind speed to calculate rain bucket tips'''
def rainfallHandler(pin):
  global rain_interrupt
  rain_interrupt = 1

'''Connect to MQTT Broker'''
def connectMQTTBroker():
  print("Connecting to MQTT server... ", end="")
  client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD, \
                        keepalive = KEEP_ALIVE_DURATION, port = MQTT_PORT)
  client.connect()
  print("Connected!")
  return client

def main():
  '''Interrupt global variables'''
  global wind_interrupt
  global rain_interrupt
  
  '''Variables used in the main function for calculating wind speed'''
  prev_time_on_wind_interrupt = 0
  time_on_wind_interrupt      = 0
  total_wind_speed            = 0
  speed_counter               = 0
  avg_wind_speed              = 0
  avg_wind_speed_calc_time    = 0
  prev_avg_wind_speed         = 0

  '''Variables used in the main function for calculating 'rainfall'''
  rain_hour_counter           = 0
  rain_day_counter            = 0
  time_on_rain_interrupt      = 0
  prev_time_on_rain_interrupt = 0
  last_rain_hour_calc_time    = 0
  last_rain_day_calc_time     = 0
  rain_per_day                = 0
  rain_per_hour               = 0
  rain_state                  = 0

  '''Variables for publishing rain every hour and everyday'''
  prev_hour = 0
  prev_day  = 0
  last_publish_time = 0
  
  '''Variable for allowing access point blocking'''
  time_start = time()
  socket_state = 0
  ap_after_con = 0
  
  '''Microcontroller pin declarations'''
  wind_direction_sensor = ADC(WIND_DIRECTION_PIN) #Wind direction pin
  wind_sensor = Pin(WIND_SPEED_PIN,Pin.IN,Pin.PULL_UP) #Wind speed pin
  rain_sensor = Pin(RAINFALL_AMOUNT_PIN,Pin.IN,Pin.PULL_UP) #Rainfall pin
  rain_sensor.irq(trigger=Pin.IRQ_FALLING,handler=rainfallHandler) #rain interrupt 
  wind_sensor.irq(trigger=Pin.IRQ_RISING,handler=windSpeedHandler) #wind interrupt
  
  try:
    '''Create wifi client and access according to wifi connectivity else raise exception'''
    access_point = makeAccessPoint() # Make access point
    wifi_client = connectWiFi(WIFI_NAME, WIFI_PASSWORD)  # Connect to WiFi
    '''Create an instance of MQTT Client. Check its connection on every run. If it isn't connected, reconnect it''' 
    mqtt_client = connectMQTTBroker()
    AP = 1
  except OSError as e:
    AP = 0
  
  while True:  
    if AP == 0 and socket_state == 0:
      '''Check whether an access point has been created to start web server
      Create a socket for web server and connect to it'''
      web_socket = settings_server.createSocket(WEB_SERVER, WEB_PORT)  
      '''Define a variable for loading webpage'''
      html_webpage = webpage.getWebPage()
      socket_state = 1
    
    while access_point.isconnected() and AP == 0 and socket_state == 1 and ap_after_con == 0:
      if not access_point.isconnected():
        AP = 1
      try:
        client, address = web_socket.accept()
        print('Got a connection from %s' % str(address))
        settings_server.respondWebServer(client, html_webpage)
        request = settings_server.receiveWebServer(client).decode("utf-8")
        if request is not None:
          data = str(request)
          referer = request_to_json.extractReferer(data)
        else:
          referer = None
        if referer is not None:
          params = request_to_json.extractRefererParams(referer)
        else:
          params = None
        if params is not None:
          print(params)
          ap_after_con = request_to_json.saveVariables(params)
          AP = 1
          break
      except (OSError, NameError) as e:
        pass

    while AP == 1:
      if access_point.isconnected() and ap_after_con == 0:
        AP = 0
      '''Time variables from NTPTime to find current hour and current day'''
      time_now = localtime(time())
      hour     = time_now[3]
      day      = time_now[2]
      week     = time_now[6]
      month    = time_now[1]

      '''Calculate the wind direction by first finding the value on the pin connected to the wind vane. Then use that value 
      to calculate the direction of the wind.'''
      wind_direction_value = wind_direction_sensor.read()
      wind_direction_worded = wind_direction.windDirection(wind_direction_value)

      '''Calculate the wind speed using the two functions below. One is for debouncing and the other for calculating the wind speed
      for every half rotation of the anemometer'''
      time_on_wind_interrupt, prev_time_on_wind_interrupt, wind_interrupt = wind_speed.debounceWindSpeedInterrupt(\
                                                                      prev_time_on_wind_interrupt, time_on_wind_interrupt, wind_interrupt)
      total_wind_speed, speed_counter, wind_interrupt = wind_speed.calculateWindSpeed(prev_time_on_wind_interrupt,\
                                                                      time_on_wind_interrupt,total_wind_speed,speed_counter, wind_interrupt)
        
      '''Calculate the average speed of wind at intervals of 2 seconds using winds speeds calculated above'''
      if(time() - avg_wind_speed_calc_time >= 3):
        avg_wind_speed, total_wind_speed, speed_counter  = wind_speed.calculateAverageSpeed(total_wind_speed, speed_counter,\
                                                                                              prev_avg_wind_speed)  
        avg_wind_speed_calc_time = time()
        prev_avg_wind_speed = avg_wind_speed

      '''Calculate the amount of rainfall per hour and per day using the functions below. The first function is for debouncing
      the bucket tip. The second function is for incrementing the counters for calculating the number of tips per hour and tips per day.
      The third and fourth functions will then calculate the amount of rain per hour and per day each time they are called. The check
      function then resets the counter whenever the hur and day changes'''
      rain_hour_counter, rain_day_counter, time_on_rain_interrupt, rain_interrupt = rainfall.debounceRainfallInterrupt(rain_hour_counter,\
                                                                      rain_day_counter, time_on_rain_interrupt, rain_interrupt)
      rain_per_hour, last_rain_hour_calc_time, prev_hour, rain_state = rainfall.calculateRainHour(rain_state, rain_per_hour, rain_hour_counter,\
                                                                      last_rain_hour_calc_time, hour, prev_hour)
      rain_per_day, last_rain_day_calc_time, prev_day  = rainfall.calculateRainDay(rain_per_day,\
                                                                      rain_day_counter, last_rain_day_calc_time, day, prev_day)
      if (hour != prev_hour or day != prev_day):
        rain_per_hour, prev_hour, rain_hour_counter, rain_state, rain_per_day, prev_day, rain_day_counter = \
                                                                      rainfall.checkRainCounters(rain_per_hour,hour,rain_hour_counter, \
                                                                        prev_hour, rain_state, rain_per_day, day, rain_day_counter, prev_day)      
        
      '''Publish all the variables via a single packet. The function will take all the variables and create ap packet of all of them.
      It will then check whether a packet has been published in the last five seconds. If not, it publishes the packet, else it
      returns the last published time.'''
      last_publish_time = mqtt.createPacketAndPublish(mqtt_client, MQTT_TOPIC, avg_wind_speed, wind_direction_worded, \
                                                         rain_state, rain_per_hour, rain_per_day, last_publish_time, MQTT_PUBLISH_TIME_GAP)

'''Global variables defined for interrupt handlers'''
wind_interrupt = 0
rain_interrupt = 0

if __name__ == "__main__":
    main()

import wind_speed
import mqtt
import time
import rainfall
import ntptime

'''Global variables defined for interrupt handlers'''
wind_interrupt = 0
rain_interrupt = 0

'''Interrupt handler for wind speed to calculate pulse duration'''
def windSpeedHandler(pin):
  global wind_interrupt
  wind_interrupt = 1

'''Interrupt handler for wind speed to calculate rain bucket tips'''
def rainfallHandler(pin):
  global rain_interrupt
  rain_interrupt = 1

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
  last_avg_wind_speed         = 0

  '''Variables used in the main function for calculating 'rainfall'''
  rain_hour_counter           = 0
  rain_day_counter            = 0
  time_on_rain_interrupt      = 0
  prev_time_on_rain_interrupt = 0
  rain_hour                   = 0
  rain_day                    = 0
  last_rain_hour_calc_time    = 0
  last_rain_day_calc_time     = 0

  '''Variables for publishing rain every hour and everyday'''
  prev_hour = 0
  prev_day  = 0
  
  dire_sensor = Pin(WIND_DIRECTION_PIN) #Wind direction pin
  wind_sensor = Pin(WIND_SPEED_PIN,Pin.IN,Pin.PULL_UP) #Wind speed pin
  rain_sensor = Pin(RAINFALL_AMOUNT_PIN,Pin.IN,Pin.PULL_UP) #Rainfall pin
  rain_sensor.irq(trigger=Pin.IRQ_FALLING,handler=rainfallHandler) #rain interrupt 
  wind_sensor.irq(trigger=Pin.IRQ_RISING,handler=windSpeedHandler) #wind interrupt
    
  while True:
    '''Variables from NTPTime'''
    time_now = localtime(time.time() + UTC_OFFSET)
    hour     = time_now[3]
    day      = time_now[2]
    week     = time_now[6]
    month    = time_now[1]

    time_on_wind_interrupt, prev_time_on_wind_interrupt, wind_interrupt = wind_speed.debounceWindSpeedInterrupt(\
                                                                    prev_time_on_wind_interrupt, time_on_wind_interrupt, wind_interrupt)
    total_wind_speed, speed_counter = wind_speed.calculateWindSpeed(prev_time_on_wind_interrupt,\
                                                                    time_on_wind_interrupt,total_wind_speed,speed_counter)
    time_on_rain_interrupt, prev_time_on_rain_interrupt, rain_interrupt = rainfall.debounceRainfallInterrupt(\
                                                                    prev_time_on_rain_interrupt, time_on_rain_interrupt, rain_interrupt)
    rain_hour_counter, rain_day_counter = rainfall.incrementRainCounters(time_on_rain_interrupt, prev_time_on_rain_interrupt, \
                                                                    rain_interrupt, rain_hour_counter, rain_day_counter)
    rain_hour, last_rain_hour_calc_time, prev_hour = rainfall.calculateRainHour(rain_hour_counter, last_rain_hour_calc_time, hour,prev_hour) 
    rain_day, last_rain_day_calc_time, prev_day  = rainfall.calculateRainDay(rain_day_counter, last_rain_day_calc_time, day, prev_day)
    rain_state = rainfall.checkRain(rain_hour) 

    if(time.time() - avg_wind_speed_calc_time > 5):
      avg_wind_speed, total_wind_speed, speed_counter  = wind_speed.calculateAverageSpeed(total_wind_speed,speed_counter,avg_wind_speed)  
      print("Average speed: ", avg_wind_speed)
      avg_wind_speed_calc_time = time.time()
      last_avg_wind_speed = avg_wind_speed
      avg_wind_speed = 0

if __name__ == "__main__":
    main()

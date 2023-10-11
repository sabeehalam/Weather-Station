from time import time_ns, time
import ntptime

'''Debounce the rain bucket tip interrupts to get a singular step time'''    
def debounceRainfallInterrupt(prev_time_on_rain_interrupt, time_on_rain_interrupt, rain_interrupt):
  if(rain_interrupt == 1 and (time_ns()-prev_time_on_rain_interrupt > 1000000000)):
    prev_time_on_rain_interrupt = time_on_rain_interrupt
    time_on_rain_interrupt = time_ns()
    rain_interrupt = 0    
    return time_on_rain_interrupt, prev_time_on_rain_interrupt, rain_interrupt
  elif(rain_interrupt == 1 and (time_ns()-prev_time_on_rain_interrupt <= 1000000000)):
    return time_on_rain_interrupt, prev_time_on_rain_interrupt, rain_interrupt
  else: 
    return time_on_rain_interrupt, prev_time_on_rain_interrupt, rain_interrupt

'''Increment rain counters for hour and day'''
def incrementRainCounters(time_on_rain_interrupt, prev_time_on_rain_interrupt, rain_interrupt, rain_hour_counter, rain_day_counter):
  if(rain_interrupt == 1 and (time_ns()-prev_time_on_rain_interrupt > 1000000000)):
    rain_hour_counter += 1
    rain_day_counter += 1
    return rain_hour_counter, rain_day_counter
  elif(rain_interrupt == 1 and (time_ns()-prev_time_on_rain_interrupt <= 1000000000)):
    return rain_hour_counter, rain_day_counter
  else: 
    return rain_hour_counter, rain_day_counter

'''Calculate the rain per hour and per day using the counters'''
def calculateRainHour(rain_hour_counter, last_rain_hour_calc_time, hour, prev_hour):
  if(hour != prev_hour):
    rain_hour = 0.2794 * rain_hour_counter
    print("Rain last hour: ", rain_hour)
    last_rain_hour_calc_time = time()
    return rain_hour, last_rain_hour_calc_time, hour
  else: return 0, last_rain_hour_calc_time, hour

'''Calculate the rain per day using the counters'''
def calculateRainDay(rain_day_counter, last_rain_day_calc_time, day, prev_day):
  if(day != prev_day):
    rain_day = 0.2794 * rain_day_counter
    last_rain_day_calc_time = time()
    return rain_day, last_rain_day_calc_time, day
  else: return 0, last_rain_day_calc_time, day

'''Çheck whether it is raining and return true or false on the result'''
def checkRain(rain_hour):
  if(rain_hour > 0):
    print("It is raining")
    return True
  else:
    return False


    
from time import time_ns
    
'''Debounce the wind speed interrupts to get a singular step time'''    
def debounceWindSpeedInterrupt(prev_time_on_wind_interrupt, time_on_wind_interrupt, wind_interrupt):
  if(wind_interrupt == 1 and (time_ns()-prev_time_on_wind_interrupt > 300000000)):
    prev_time_on_wind_interrupt = time_on_wind_interrupt
    time_on_wind_interrupt = time_ns()
    wind_interrupt = 0    
    return time_on_wind_interrupt, prev_time_on_wind_interrupt, wind_interrupt
  elif(wind_interrupt == 1 and (time_ns()-prev_time_on_wind_interrupt <= 300000000)):
    return time_on_wind_interrupt, prev_time_on_wind_interrupt, wind_interrupt
  else: return time_on_wind_interrupt, prev_time_on_wind_interrupt, wind_interrupt


'''Calculate the wind speed using the time on the last two wind interrupts'''
def calculateWindSpeed(prev_time_on_wind_interrupt, time_on_wind_interrupt, total_wind_speed, speed_counter):
  if(prev_time_on_wind_interrupt == 0 or time_on_wind_interrupt == 0):
    return total_wind_speed, speed_counter      
  
  wind_speed = 2.4 * (1/((time_on_wind_interrupt - prev_time_on_wind_interrupt) / 1000000000))
#   print("Previous time and current time: ", prev_time_on_wind_interrupt, "  ", time_on_wind_interrupt)   
  if(wind_speed > 150):
    return total_wind_speed, speed_counter
    
  total_wind_speed += wind_speed
  speed_counter  += 1
  return total_wind_speed, speed_counter
      
'''Calculate and return the average wind speed'''
def calculateAverageSpeed(total_wind_speed,speed_counter,last_avg_wind_speed):
  if(speed_counter > 0):
    avg_wind_speed = total_wind_speed / speed_counter
    total_wind_speed, speed_counter = 0,0
    return avg_wind_speed, total_wind_speed, speed_counter
  else:
    total_wind_speed, speed_counter = 0,0
    return 0, total_wind_speed, speed_counter


from time import ticks_ms, ticks_diff

def debounceWindSpeedInterrupt(prev_time_on_wind_interrupt, time_on_wind_interrupt, wind_interrupt):
    current_time = ticks_ms()
    if wind_interrupt and (ticks_diff(current_time,prev_time_on_wind_interrupt) > 300):
        prev_time_on_wind_interrupt = time_on_wind_interrupt
        time_on_wind_interrupt = current_time
    elif wind_interrupt and (ticks_diff(current_time,prev_time_on_wind_interrupt) < 300):
        time_on_wind_interrupt = current_time
    return time_on_wind_interrupt, prev_time_on_wind_interrupt, wind_interrupt

def calculateWindSpeed(prev_time_on_wind_interrupt, time_on_wind_interrupt, total_wind_speed, speed_counter, wind_interrupt):
    if prev_time_on_wind_interrupt == 0 or time_on_wind_interrupt == 0 or wind_interrupt == 0:
        return total_wind_speed, speed_counter, wind_interrupt
    
    wind_speed = 2.4 / (ticks_diff(time_on_wind_interrupt,prev_time_on_wind_interrupt) / 1000)
    wind_interrupt = 0
    
    if wind_speed > 100 and (ticks_diff(time_on_wind_interrupt,prev_time_on_wind_interrupt) <= 250):
        return total_wind_speed, speed_counter, wind_interrupt
    
    total_wind_speed += wind_speed
    speed_counter += 1
    return total_wind_speed, speed_counter, wind_interrupt

def calculateAverageSpeed(total_wind_speed, speed_counter, last_avg_wind_speed):
    avg_wind_speed = 0
    if speed_counter != 0:
        avg_wind_speed = total_wind_speed / speed_counter
    if avg_wind_speed != last_avg_wind_speed:
        total_wind_speed, speed_counter = 0, 0
        return avg_wind_speed, total_wind_speed, speed_counter
    else:
        total_wind_speed, speed_counter = 0, 0
        return 0, total_wind_speed, speed_counter

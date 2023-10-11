from time import time_ns, time

def debounceRainfallInterrupt(rain_hour_counter, rain_day_counter, time_on_rain_interrupt, rain_interrupt):
    current_time = time_ns()
    if rain_interrupt and not time_on_rain_interrupt:
        time_on_rain_interrupt = current_time
    elif rain_interrupt and current_time - time_on_rain_interrupt > 400000000:
        time_on_rain_interrupt = 0
        rain_hour_counter += 1
        rain_day_counter += 1
        rain_interrupt = 0
    return rain_hour_counter, rain_day_counter, time_on_rain_interrupt, rain_interrupt

def calculateRainHour(rain_state, rain_per_hour, rain_hour_counter, last_rain_hour_calc_time, hour, prev_hour):
    current_time = time()
    if hour == prev_hour and current_time - last_rain_hour_calc_time >= 5 and rain_hour_counter >= 1:
        rain_per_hour = 0.2794 * rain_hour_counter
        last_rain_hour_calc_time = current_time
        rain_state = True
    return rain_per_hour, last_rain_hour_calc_time, prev_hour, rain_state

def calculateRainDay(rain_per_day, rain_day_counter, last_rain_day_calc_time, day, prev_day):
    current_time = time()
    if day == prev_day and current_time - last_rain_day_calc_time >= 5 and rain_day_counter >= 1:
        rain_per_day = 0.2794 * rain_day_counter
        last_rain_day_calc_time = current_time
    return rain_per_day, last_rain_day_calc_time, prev_day

def checkRainCounters(rain_per_hour, hour, rain_hour_counter, prev_hour, rain_state, rain_per_day, day, rain_day_counter, prev_day):
    if hour != prev_hour:
        prev_hour = hour
        rain_hour_counter = 0
        rain_per_hour = 0
        rain_state = False
    if day != prev_day:
        prev_day = day
        rain_day_counter = 0
        rain_per_day = 0
    return rain_per_hour, prev_hour, rain_hour_counter, rain_state, rain_per_day, prev_day, rain_day_counter

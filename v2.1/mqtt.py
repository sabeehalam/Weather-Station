from time import time

def MQTTCallback(topic, msg):
    print("Callback")
    cb_publish_time = time()

def createPacketAndPublish(mqtt_client, topic, avg_wind_speed, wind_direction, rain_state, rain_hour, rain_day, last_publish_time):
    current_time = time()
    if current_time - last_publish_time >= 3:
        msg = str([avg_wind_speed,wind_direction,rain_state,rain_hour,rain_day])
        mqtt_client.publish(topic, msg)
        last_publish_time = current_time
    return last_publish_time

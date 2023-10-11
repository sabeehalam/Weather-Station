'''Publish Variables'''
def publishWindSpeedFunc(wind_speed, mqtt_client):
    mqtt_client.publish(MQTT_TOPIC_WIND, str(wind_speed), qos = 0)
  
def publishWindDirectionFunc(direction, mqtt_client):
    mqtt_client.publish(MQTT_TOPIC_DIR, direction, qos = 0)
        
def publishCheckRainFunc(mqtt_client):
    mqtt_client.publish(MQTT_TOPIC_RAIN, "It's raining", qos = 0)
       
def publishRainFunc(topic, rain_volume, mqtt_client):
    mqtt_client.publish(topic, str(rain_volume), qos = 0)
    
'''MQTT callback function to raise connection flag'''
def MQTTCallback(topic, msg):
    print("Callback")
    cb_publish_time = time()
    

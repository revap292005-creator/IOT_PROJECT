import paho.mqtt.client as mqtt
import time
import random

# MQTT Broker details
BROKER = "test.mosquitto.org"   # or your local broker IP
PORT = 1883
TOPIC = "environment/data"

# Create MQTT client
client = mqtt.Client()

# Connect to broker
client.connect(BROKER, PORT, 60)

print("Connected to MQTT Broker")

while True:
    temperature = round(random.uniform(25, 40), 2)
    humidity = round(random.uniform(40, 80), 2)
    gas = random.randint(100, 500)

    # Status logic
    if gas < 300:
        status = "NORMAL"
    elif gas < 400:
        status = "WARNING"
    else:
        status = "DANGER"

    payload = f"{temperature},{humidity},{gas},{status}"

    client.publish(TOPIC, payload)
    print("Published:", payload)

    time.sleep(5)
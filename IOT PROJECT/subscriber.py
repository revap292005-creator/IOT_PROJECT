import json
import mysql.connector
import paho.mqtt.client as mqtt
import requests

# ---------------- DATABASE CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="smart_environment_monitoring_system1"
)
cursor = db.cursor()

# ---------------- THINGSPEAK CONFIG ----------------
THINGSPEAK_API_KEY = "V06OT4YLSATH9BYY"


# ---------------- MQTT CALLBACKS ----------------
def on_connect(client, userdata, flags, reason_code, properties):
        print("Connected to MQTT Broker")
        client.subscribe("envdata")
        print("subscribed to topic: envdata")

def on_message(client, userdata, msg):
        data = json.loads(msg.payload.decode())

        temp = data["temp"]
        humidity = data["humidity"]
        gas = data["gas"]

        print("Data Received:")
        print(f"temp: {temp} °C")
        print(f"humidity  : {humidity} %")
        print(f"gas  : {gas}")
        print("-" * 30)
    
        cursor.execute(
            "INSERT INTO envdata (temp, humidity, gas) VALUES (%s, %s, %s)",
            (temp, humidity, gas)
        )
        db.commit()

        requests.get(
            "https://api.thingspeak.com/update",
        params={
            "api_key": THINGSPEAK_API_KEY,
            "field1": temp,
            "field2": humidity,
            "field3": gas
        }
    ) 



client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)
client.loop_forever()
import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

# Load environment variables from the .env file
load_dotenv()

# Get the values from the environment variables
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))  # Default to 1883 if not found
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# MQTT command and status topics
MQTT_TOPIC = "cmnd/smettus_plug/POWER"
MQTT_STATUS_TOPIC = "stat/smettus_plug/POWER"

def on_message(client, userdata, msg):
    print(f"Plug status: {msg.payload.decode()}")

def connect_mqtt():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.on_message = on_message
    return client

def turn_on():
    client = connect_mqtt()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(MQTT_TOPIC, "ON")
    client.disconnect()
    print("Plug turned ON")

def turn_off():
    client = connect_mqtt()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.publish(MQTT_TOPIC, "OFF")
    client.disconnect()
    print("Plug turned OFF")

def get_status():
    client = connect_mqtt()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.subscribe(MQTT_STATUS_TOPIC)
    client.loop_start()
    client.publish(MQTT_STATUS_TOPIC, "")
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    turn_on()
    get_status()
    turn_off()
    get_status()

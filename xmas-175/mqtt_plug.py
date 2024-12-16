import os
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

# first I need to run a broker!!

# Load environment variables from the .env file
load_dotenv()

# Get the values from the environment variables
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))  # Default to 1883 if not found
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_CLIENT = os.getenv("MQTT_CLIENT")

# MQTT command and status topics
MQTT_TOPIC = "cmnd/smettus_plug/POWER"
MQTT_STATUS_TOPIC = "stat/smettus_plug/POWER"

def on_message(client, userdata, msg):
    print(f"Plug status: {msg.payload.decode()}")

def connect_mqtt():
    # Specify the callback API version (2.0)
    client = mqtt.Client(client_id=MQTT_CLIENT, protocol=mqtt.MQTTv311)
    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.on_message = on_message
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print(f"Connected to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    except Exception as e:
        print(f"Failed to connect to MQTT broker: {e}")
        exit(1)  # Exit if connection fails
    return client

def turn_on(client):
    client.publish(MQTT_TOPIC, "ON")
    print("Plug turned ON")

def turn_off(client):
    client.publish(MQTT_TOPIC, "OFF")
    print("Plug turned OFF")

def get_status(client):
    client.subscribe(MQTT_STATUS_TOPIC)
    print("Subscribed to status topic...")
    client.loop_start()  # Start the network loop
    # Wait for the message to be received
    input("Press Enter to stop listening for status...\n")  # Block until the user stops
    client.loop_stop()  # Stop the loop when done
    print("Unsubscribed and disconnected from status topic")
    client.disconnect()

if __name__ == "__main__":
    client = connect_mqtt()  # Connect once

    turn_on(client)  # Turn the plug on
    get_status(client)  # Get the plug's status
    turn_off(client)  # Turn the plug off
    get_status(client)  # Get the plug's status again

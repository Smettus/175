import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

PLUG_IP = os.getenv("PLUG_IP")

# Function to send command to the Tasmota plug
def send_command(command):
    url = f"http://{PLUG_IP}/cm?cmnd={command}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Command '{command}' sent successfully!")
            
            if command == "Status+10":
                return response.json()
        else:
            print(f"Failed to send command. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending command: {e}")



# Function to turn the plug on
def turn_on():
    send_command("Power On")

# Function to turn the plug off
def turn_off():
    send_command("Power off")

# Function to toggle the plug power
def toggle_power():
    send_command("Power Toggle")
def get_device_status():
    data = send_command("Status+10")
    return data

# Example usage
if __name__ == "__main__":
    #turn_on()  # Turn the plug on
    #toggle_power()  # Toggle the plug's power
    status_data = get_device_status()
    if status_data:
        # Print the JSON response
        print(json.dumps(status_data, indent=4))

    
    #turn_off()  # Turn the plug off

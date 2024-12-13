import os
from time import sleep
import logging
#import RPi.GPIO as GPIO
from gpiozero import DigitalInputDevice, MotionSensor

# 0) Hardware
# https://toptechboy.com/understanding-raspberry-pi-4-gpio-pinouts/
# 1) Logic & code
# https://gpiozero.readthedocs.io/en/latest/api_input.html
# 2) Automate:
# crontab -e
# Add this line at the end:
# @reboot python path2song

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(message)s',
    filename='motion_trigger.log',
    filemode='a'
)

counter_file = 'motion_count.txt'
def load_counter():
    """Load the counter from a file or initialize to 0 if file doesn't exist."""
    if os.path.exists(counter_file):
        with open(counter_file, 'r') as f:
            return int(f.read())
    return 0
def save_counter(count):
    """Save the counter to a file."""
    with open(counter_file, 'w') as f:
        f.write(str(count))

def play_song(path):
    """Play song of choice. Uses mpg321, should be installed in rpios"""
    os.system(f'mpg321 {path}') # add '&' if want the song to continue in the bg

def main():
    # GPIO.setmode(GPIO.BCM)
    # PIR_PIN = 17 # is phyisical pin 11
    # GPIO.setup(PIR_PIN, GPIO.IN)
    PIR_PIN = 17
    song_path = './Christmas Tape Vol175.mp3'
    pir = MotionSensor(PIR_PIN)
    
    count = load_counter()
    logging.info("System initialized. Waiting for motion...")
    
    while True:
        pir.wait_for_motion()
        count += 1
        logging.info(f"Motion detected! Triggering song. Total detections {count}")
        save_counter(count)
        play_song(song_path)

if __name__ == '__main__':
    main()
    
    
    
# def sensorloop():
#     # https://docs.sunfounder.com/projects/umsk/en/latest/05_raspberry_pi/pi_lesson12_pir_motion.html#pi-lesson12-pir-motion
#     # Initialize the motion sensor as a digital input device on GPIO pin 17
#     motion_sensor = DigitalInputDevice(17)

#     # Continuously monitor the state of the motion sensor
#     while True:
#         if motion_sensor.is_active:
#             print("Somebody here!")
#             # Play the song
#         else:
#             print("Monitoring...")

#         # Wait for 0.5 seconds before the next sensor check
#         sleep(0.5)

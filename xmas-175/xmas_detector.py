import os
from time import sleep
import logging
import subprocess
import pygame
#import RPi.GPIO as GPIO
from gpiozero import DigitalInputDevice, MotionSensor

# 0) Hardware
# https://toptechboy.com/understanding-raspberry-pi-4-gpio-pinouts/
# https://docs.sunfounder.com/projects/umsk/en/latest/05_raspberry_pi/pi_lesson12_pir_motion.html#pi-lesson12-pir-motion
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
"""
def play_song(path):
    #Play song with retry if audio device is busy.
    max_retries = 5
    retries = 0
    while retries < max_retries:
        try:
            os.system(f'mpg123 {path}') # add '&' if want the song to continue in the bg
            # mpg321 -q {path} > /dev/null 2>&1
            #subprocess.run(['mpg123', path, '-q', '> /dev/null 2>&1'])
            break
        except Exception as e:
            logging.error(f"Error playing song: {e}")
            retries += 1
            sleep(1)
    if retries == max_retries:
        logging.error("Failed to play song after multiple attempts.")
"""
def play_song(path):
    """Play song using pygame.mixer."""
    pygame.mixer.init()
    
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        logging.info(f"Playing song: {path}")
        while pygame.mixer.music.get_busy():
            sleep(0.1)  # Wait for the song to finish playing
    except Exception as e:
        logging.error(f"Error playing song: {e}")
def main():
    # GPIO.setmode(GPIO.BCM)
    # PIR_PIN = 17 # is phyisical pin 11
    # GPIO.setup(PIR_PIN, GPIO.IN)
    PIR_PIN = 17
    song_path = os.path.join(os.getcwd(), 'lesPopos.mp3')
    pir = MotionSensor(PIR_PIN)
    
    count = load_counter()
    logging.info("System initialized. Waiting for motion...")
    
    while True:
        i = 0
        while i < 3:
            pir.wait_for_motion()
            i += 1
        count += 1
        logging.info(f"Motion detected! Triggering song. Total detections {count}")
        save_counter(count)
        play_song(song_path)
        sleep(2)

def set_audio_output():
    # Set audio output to the 3.5mm jack
    subprocess.run(['amixer', 'cset', 'numid=3', '1'])

    # Unmute the audio
    subprocess.run(['amixer', 'set', 'Master', 'unmute'])

    # Set volume to 80%
    subprocess.run(['amixer', 'set', 'Master', '80%'])
def start_pulseaudio():
    """Start PulseAudio if not already running."""
    # Check if PulseAudio is already running
    try:
        # Check if pulseaudio is already running for the current user
        result = subprocess.run(['pgrep', '-u', str(os.getuid()), 'pulseaudio'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            # PulseAudio is not running, so start it
            print("PulseAudio not running, starting it...")
            subprocess.run(['pulseaudio', '--start'], check=True)
        else:
            print("PulseAudio is already running.")
    except Exception as e:
        print(f"Failed to check or start PulseAudio: {e}")

if __name__ == '__main__':
    start_pulseaudio()
    sleep(2)
    set_audio_output()
    sleep(2)
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
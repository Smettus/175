import neopixel
import board
from time import sleep

# run file with: 
# sudo ./venv-xmas175/bin/python lights.py
# https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage


# Hardware:
#   Data on GPIO10 to female white wire on the WS2811 strip.
#   Ground on ground, you can use the same as the motionsensor (leftmost)
#   Power to lightstrip from screw terminal block barrel jack


# https://pinout.xyz/
# D18 won't work, cuz audio:
#   PWM hardware on GPIO 18 and GPIO 19 is already reserved for the audio system. 
#   This creates a conflict because the same PWM hardware block is also used for controlling WS281x LEDs.
#   On gpio 12, I also hear sound if I try to use that pin...
#   sudo raspi-gpio get
# Solutions:
# 1. Software PWM
# 2. SPI (raspi config) (+: more stable than PWM, GPIO 10 MOSI)
# -> yes: sudo raspi-config -> Interfacing Options -> SPI -> yes
# 3. GPIO13 and 19 (PWM1, channel 1)
# doesnt work

# Just do SPI. However, need to level convert in future! 3.3V -> 5V with 
# simple 1N4001 power diode or with a level converter chip like the 74AHCT125 (koop dit).
# https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring


LED_COUNT = 100
LED_PIN = board.D10
ORDER = neopixel.GRB # because my strip has swapped R and G
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=1, pixel_order=ORDER) #, auto_write=False)


pixels.fill((255, 0, 0)) 
pixels.show()
sleep(1)

pixels.fill((0,255, 0))
pixels.show()
sleep(1)

pixels.fill((0,0, 255))
pixels.show()
sleep(1)

pixels.fill((255, 0, 0)) 
pixels.show()
sleep(1)

pixels.fill((0,255, 0))
pixels.show()
sleep(1)

pixels.fill((0,0, 255))
pixels.show()
sleep(1)

pixels.fill((255, 0, 0)) 
pixels.show()
sleep(1)

pixels.fill((0,255, 0))
pixels.show()
sleep(1)

pixels.fill((0,0, 255))
pixels.show()
sleep(1)

# end sequence - make the tree green and red alternating
def set_alternate_colors():
    for i in range(LED_COUNT):
        if i % 2 == 0:
            pixels[i] = (0, 255, 0)  # Green
        else:
            pixels[i] = (255, 0, 0)  # Red
    pixels.show()  # Update the LEDs
    
set_alternate_colors()
sleep(1)
# to be sure
set_alternate_colors()
sleep(1)


# Make tree off
# pixels.fill((0,0,0))
# pixels.show()
# sleep(1)
# pixels.fill((0,0,0))
# pixels.show()
# sleep(1)

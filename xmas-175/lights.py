import neopixel
import board
from time import sleep

pixels = neopixel.NeoPixel(board.D18, 16, brightness=1) # first 10 pixels
pixels.fill((0, 0, 0))
sleep(2)
pixels.fill((255, 0, 0))
pixels.show()
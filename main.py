#!/usr/bin/env python3
from time import sleep

from ev3dev2.display import Display
from ev3dev2.sensor import Sensor, INPUT_1, INPUT_4
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.port import LegoPort
from pixycamev3.pixy2 import Pixy2


# EV3 Display
lcd = Display()

# Connect TouchSensor to port #4
ts = TouchSensor(INPUT_4)

# Set LEGO port for Pixy on input port 1 
pixy2 = Pixy2(port=1, i2c_address=0x54)
version = pixy2.get_version()
print('Hardware: ', version.hardware)
print('Firmware: ', version.firmware)

# Turn upper leds on for 2 seconds, then turn off
pixy2.set_lamp(1, 0)
sleep(2)
pixy2.set_lamp(0, 0)


# Set mode to detect signature 1 only
pixy2.mode = 'SIG1'

# Read and display data until TouchSensor is pressed
while not ts.value():
    # Clear EV3 display
    lcd.clear()
    # Read values from Pixy


    nr_blocks, blocks = pixy2.get_blocks(1, 1)
    if nr_blocks >= 1: 
        x = blocks[0].x_center     # X-coordinate of centerpoint of object
        y = blocks[0].y_center     # Y-coordinate of centerpoint of object
        w = blocks[0].width     # Width of rectangle around detected object
        h = blocks[0].height    # Heigth of rectangle around detected object

        # scale to resolution of EV3 display:
        # Resolution Pixy while color tracking: (255x199)
        # Resolution EV3 display: (178x128)
        x *= 0.7
        y *= 0.6
        w *= 0.7
        h *= 0.6

        # Calculate reactangle to draw on EV3-display
        dx = int(w/2)         # Half of the width of the rectangle
        dy = int(h/2)         # Half of the height of the rectangle
        xa = x - dx           # X-coordinate of top-left corner
        ya = y + dy           # Y-coordinate of the top-left corner
        xb = x + dx           # X-coordinate of bottom-right corner
        yb = y - dy           # Y-coordinate of the bottom-right corner

        # Draw rectangle on display
        lcd.draw.rectangle((xa, ya, xb, yb), fill='black')

        # Update display to show rectangle
        lcd.update()
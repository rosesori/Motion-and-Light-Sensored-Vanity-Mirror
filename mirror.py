#import GPIO and time
import RPi.GPIO as GPIO
from time import sleep
from gpiozero import MotionSensor, LED
import os
import time
from time import sleep
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Set up Photoresistor and MCP3008 Chip
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI) # Create the spi bus
cs = digitalio.DigitalInOut(board.D22)                             # Create the CS (chip select)
mcp = MCP.MCP3008(spi, cs)                                         # Create the MCP object
chan0 = AnalogIn(mcp, MCP.P0)                                      # Create an analog input channel on pin 0

# Set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

# Set up PIR Sensor
pir = MotionSensor(18)

# Global variables
motionon = [0] * 10
motionoff = []
sixAreOn = False
fourAreOn = False
twoAreOn = False
zeroAreOn = True

# Calculates average of 10 elements of array to see if motion was detected (5 consecutive 1's)
def motionDetectionCount(myArr):
    count = 0
    for i in range(len(myArr)):
        if myArr[i] == 1:
            count += 1
    return count

def turnOnSix():
    global sixAreOn
    global fourAreOn
    global twoAreOn
    global zeroAreOn
    GPIO.output(26, True)
    GPIO.output(13, True)
    GPIO.output(19, True)
    GPIO.output(6, True)
    GPIO.output(16, True)
    GPIO.output(20, True)
    sixAreOn = True
    fourAreOn = False
    twoAreOn = False
    zeroAreOn = False
    
def turnOnFour():
    global sixAreOn
    global fourAreOn
    global twoAreOn
    global zeroAreOn
    GPIO.output(26, True)
    GPIO.output(13, True)
    GPIO.output(19, False)
    GPIO.output(6, False)
    GPIO.output(16, True)
    GPIO.output(20, True)
    sixAreOn = False
    fourAreOn = True
    twoAreOn = False
    zeroAreOn = False
    
def turnOnTwo():
    global sixAreOn
    global fourAreOn
    global twoAreOn
    global zeroAreOn
    GPIO.output(26, True)
    GPIO.output(13, True)
    GPIO.output(19, False)
    GPIO.output(6, False)
    GPIO.output(16, False)
    GPIO.output(20, False)
    sixAreOn = False
    fourAreOn = False
    twoAreOn = True
    zeroAreOn = False

def turnOnZero():
    global sixAreOn
    global fourAreOn
    global twoAreOn
    global zeroAreOn
    GPIO.output(26, False)
    GPIO.output(13, False)
    GPIO.output(19, False)
    GPIO.output(6, False)
    GPIO.output(16, False)
    GPIO.output(20, False)
    sixAreOn = False
    fourAreOn = False
    twoAreOn = False
    zeroAreOn = True
    
def lightIntensity():
    if chan0.value > 60000:
        print('light value w six bulbs ', chan0.value)
        turnOnSix()
    elif chan0.value >= 55000 and chan0.value < 60000:
        print('light value w four bulbs ', chan0.value)
        turnOnFour()
    elif chan0.value >= 40000 and chan0.value < 55000:
        print('light value w two bulbs ', chan0.value)
        turnOnTwo()
    else:
        print('light value w zero bulbs ', chan0.value)
        turnOnZero()
    
# START; turn off all lights
turnOnZero()

# If motion is detected, append 1. Else append 0. Pop 1st element so list only has 10 elements
hasApproached = False
initialLight = 0
heldFlashlight = 0
while True:
    if pir.value == 1:
        print('motion detected')
        motionon.pop(0)
        motionon.append(1)
        print(motionon)
    else:
        print('no motion')
        motionon.pop(0)
        motionon.append(0)
        print(motionon)
    # If motion was detected from avg
    if motionDetectionCount(motionon) > 6: # Light is on
        if hasApproached == False:
            initialLight = chan0.value
            lightIntensity()
            hasApproached = True            
    else:                                  # Light is off
        print('Lights are off')
        hasApproached = False
        turnOnZero()
    sleep(0.5)
    print('Light value: ', chan0.value)
    print("-------------------")
 
# Cycle tionhe relay depending on PIR sensor
GPIO.cleanup()
 


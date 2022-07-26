#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import *
import argparse
import socket
import threading
import encodings


# LED strip configuration:
LED_COUNT      = 900      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
NUM_ITER       = 300



# Define functions which animate LEDs in various ways.
def allOneColor(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)

    strip.show()

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def parse_midi_data(in_data, delay_time=2):
    if len(in_data.split(';')) > 4:
        print("Too much data... skipping this double message")
        return
    note, ml_key, prob_ml_key, is_in = in_data.split(';')
    print(f"Note: {note} played in predicted context of {ml_key} ({prob_ml_key}). Inside? {is_in}")
    data2color(note, ml_key, float(prob_ml_key), is_in)
        #time.sleep(delay_time)

def data2color(note, ml_key, prob_ml_key, is_in):
    ml_key = ml_key.upper()
    if ml_key == "C":
        color = (255,0,0)
    elif ml_key == "D-":
        color = (255, 116, 0)
    elif ml_key == "D":
        color = (255, 177, 0)
    elif ml_key == "E-":
        color = (255, 229, 0)
    elif ml_key  == "E":
        color = (204, 255, 0)
    elif ml_key == "F":
        color = (39, 255, 0)
    elif ml_key == "G-":
        color = (0, 255, 218)
    elif ml_key == "G":
        color = (0, 231, 255)
    elif ml_key == "A-":
        color = (0, 166, 255)
    elif ml_key == "A":
        color = (0, 0, 255)
    elif ml_key == "B-":
        color = (152, 0, 255)
    elif ml_key == "B":
        color = (255, 0, 229)
    else:
        print("Whoops")

    if is_in == "True":
        allOneColor(strip, Color(round(color[0]*prob_ml_key), round(color[1]*prob_ml_key), round(color[2]*prob_ml_key)))
    else:
        theaterChase(strip, Color(round(255*prob_ml_key), round(255*prob_ml_key), round(255*prob_ml_key)), iterations=1)

def my_client():
    threading.Timer(3, my_client).start()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        inp = input("Enter Command ")
        inp_enc = inp.encode('utf-8')
        s.sendall(inp_enc)
        while True:
            data = s.recv(1024).decode('utf-8')
            #print(data)
            if data == "Terminate":
                break
            parse_midi_data(data)
        s.close()

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    ###HOST = '10.30.21.220'
    ###HOST = '10.30.1.232'
    ###HOST = '127.0.0.1'
    ###HOST = '10.30.19.223'
    HOST = '10.30.19.191'
    PORT = 12345 

    #while True:
    my_client()




    try:
        #while True:
        #for N in range(NUM_ITER):
            #print ('Color wipe animations.')
            #colorWipe(strip, Color(255, 0, 0))  # Red wipe
            #colorWipe(strip, Color(0, 255, 0))  # Blue wipe
            #colorWipe(strip, Color(0, 0, 255))  # Green wipe
            #print (f"Theater chase animations. Iteration {N}")
            #theaterChase(strip, Color(127, 127, 127))  # White theater chase
            #theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            #theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            #print (f"Rainbow animations. Iteration {N}")
            #rainbow(strip)
            #rainbowCycle(strip)
            #theaterChaseRainbow(strip)
        colorWipe(strip, Color(0,0,0), 10)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)

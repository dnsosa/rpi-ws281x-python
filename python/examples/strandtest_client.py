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
NUM_ITER       = 50



# Define functions which animate LEDs in various ways.
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

def midi_string_to_dict(in_data):
    res = []
    for sub in in_data.split(' '):
        if "=" in sub:
            res.append(map(str.strip, sub.split('=', 1)))
    res = dict(res)
    return res

def parse_midi_data(in_data, delay_time=2):
    midi_event_list = in_data.split(';')
    for event_string in midi_event_list:
        midi_event = midi_string_to_dict(event_string)
        if midi_event['velocity'] == 0:
            continue  # This is lazy, need to look at event type, not just velocity
        note = int(midi_event['note'])
        print(note)
        note2color(note)
        #time.sleep(delay_time)

def note2color(note):
    one_octave_note = (note % 12)
    if one_octave_note == 0:
        color = Color(40,255,0)
    elif one_octave_note == 1:
        color = Color(0, 255, 232)
    elif one_octave_note == 2:
        color = Color(0, 124, 255)
    elif one_octave_note == 3:
        color = Color(5, 0, 255)
    elif one_octave_note == 4:
        color = Color(69, 0, 234)
    elif one_octave_note == 5:
        color = Color(87, 0, 158)
    elif one_octave_note == 6:
        color = Color(116, 0, 0)
    elif one_octave_note == 7:
        color = Color(179, 0, 0)
    elif one_octave_note == 8:
        color = Color(238, 0, 0)
    elif one_octave_note == 9:
        color = Color(255, 99, 0)
    elif one_octave_note == 10:
        color = Color(255, 236, 0)
    elif one_octave_note == 11:
        color = Color(153, 255, 0)
    else:
        print("Whoops")

    theaterChase(strip, color, iterations=1)

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

    HOST = '10.30.21.220'
    PORT = 65432

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

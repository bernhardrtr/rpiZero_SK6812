#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
********************************************************************************
* FILENAME:    light.py
*
* AUTHORS:
*       Bernhard Reiter
*
* DATE:
*       Fri Sep 25 21:04:20 2020
*
* DESCRIPTION:
*       Setup a SK6812 LED strip to switch on/off via two buttons.
*       The strip is splitted in two independent zones.
*
********************************************************************************
"""


# ----------------------------------------------------------------------------
# MODULES
# ----------------------------------------------------------------------------

# IO Modules
import rpi_ws281x as neopixel
import pigpio
from gpio_event import GPIO
from led_animations import colorWipe
from led_animations import setColor
from led_animations import showColor

# Standard Modules
import signal
import time
import sys
import os


# ----------------------------------------------------------------------------
# VARIABLES
# ----------------------------------------------------------------------------

# LED strip configuration:
LED_COUNT      = 299     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = neopixel.ws.SK6812_STRIP_GRBW   # Strip type and colour ordering

BTN_01_PIN     = 27
BTN_02_PIN     = 22
BTN_SH_PIN     = 3       # Shutdown button

ZONE_01_START  = 0
ZONE_01_STOP   = 176
ZONE_01_INC    = 1
ZONE_01        = list(range(ZONE_01_START, ZONE_01_STOP, ZONE_01_INC))

ZONE_02_START  = 299
ZONE_02_STOP   = 177
ZONE_02_INC    = -1
ZONE_02        = list(range(ZONE_02_START, ZONE_02_STOP, ZONE_02_INC))

COLOR_OFF      = neopixel.Color(0, 0, 0, 0)     # Color: Off
COLOR_SH_IND   = neopixel.Color(0, 10, 0, 10)   # Color: Shutdown indicator
COLOR_ON_IND   = neopixel.Color(10, 0, 0, 10)   # Color: Shutdown indicator
COLOR_STAGE01  = neopixel.Color(0, 0, 0, 1)     # Color: Stage 01
COLOR_STAGE02  = neopixel.Color(0, 0, 0, 3)     # Color: Stage 02

# ----------------------------------------------------------------------------
# FUNCTIONS
# ----------------------------------------------------------------------------

def signal_handler(signum, frame):
    colorWipe(strip, COLOR_OFF, [], "down", 5)
    sys.exit(0)


def shutdown():
    colorWipe(strip, COLOR_SH_IND, [], "up", 5)
    colorWipe(strip, COLOR_OFF, [], "down", 5)
    colorWipe(strip, COLOR_SH_IND, [], "up", 5)
    colorWipe(strip, COLOR_OFF, [], "down", 5)

    os.system("sudo shutdown -h now")
    sys.exit(0)


# ----------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------

# Main program:
if __name__ == '__main__':

    # INIT
    # ------------------------------------------------------------------------

    # Start pigpio daemon
    os.system("sudo killall pigpiod")
    os.system("sudo pigpiod")
    time.sleep(1)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # GPIO's
    pi = pigpio.pi()

    BTN_01 = GPIO(pi, BTN_01_PIN)
    BTN_02 = GPIO(pi, BTN_02_PIN)
    BTN_SHUTDOWN = GPIO(pi, BTN_SH_PIN, 3000)

    # Create NeoPixel object with appropriate configuration.
    strip = neopixel.Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ,
                                       LED_DMA, LED_INVERT, LED_BRIGHTNESS,
                                       LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    colorWipe(strip, COLOR_ON_IND, [], "up", 5)
    colorWipe(strip, COLOR_OFF, [], "down", 5)

    # MAIN
    # ------------------------------------------------------------------------

    btn01ShortCnt = 0
    btn02ShortCnt = 0

    while True:
        btn01State = BTN_01.state()
        btn02State = BTN_02.state()
        btnSHState = BTN_SHUTDOWN.state()

        # Shutdown
        if btnSHState == "LONG":
            shutdown()

        # Button 1
        if btn01State == "LONG":
            showColor(strip, COLOR_OFF, ZONE_01)
        elif btn01State == "SHORT" and btn01ShortCnt == 0:
            btn01ShortCnt += 1
            setColor(strip, COLOR_OFF, ZONE_01)
            showColor(strip, COLOR_STAGE01, ZONE_01)
        elif btn01State == "SHORT" and btn01ShortCnt == 1:
            btn01ShortCnt = 0
            setColor(strip, COLOR_OFF, ZONE_01)
            showColor(strip, COLOR_STAGE02, ZONE_01)

        # Button 2
        if btn02State == "LONG":
            showColor(strip, COLOR_OFF, ZONE_02)
        elif btn02State == "SHORT" and btn02ShortCnt == 0:
            btn02ShortCnt += 1
            setColor(strip, COLOR_OFF, ZONE_02)
            showColor(strip, COLOR_STAGE01, ZONE_02[60:])
        elif btn02State == "SHORT" and btn02ShortCnt == 1:
            btn02ShortCnt = 0
            setColor(strip, COLOR_OFF, ZONE_02)
            showColor(strip, COLOR_STAGE02, ZONE_02)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
********************************************************************************
* FILENAME:    led_animations.py
*
* AUTHORS:
*       Bernhard Reiter
*
* DATE:
*       Tue Oct 06 20:39:02 2020
*
* DESCRIPTION:
*       Functions which animate LEDs in various ways.
*
********************************************************************************
"""


import time
import rpi_ws281x as neopixel


def setColor(strip, color, strip_range=[]):
    """Set color across display."""
    if strip_range == [] or strip_range is None:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
    else:
        for i in strip_range:
            strip.setPixelColor(i, color)


def showColor(strip, color, strip_range=[]):
    """Set color across display."""
    if strip_range == [] or strip_range is None:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
    else:
        for i in strip_range:
            strip.setPixelColor(i, color)
    strip.show()


def colorWipe(strip, color, strip_range=[], direction="up", wait_ms=50):
    """Wipe color across display a pixel at a time."""
    if strip_range == [] or strip_range is None:
        if direction == "up":
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, color)
                strip.show()
                time.sleep(wait_ms/1000.0)
        else:
            for i in reversed(range(strip.numPixels())):
                strip.setPixelColor(i, color)
                strip.show()
                time.sleep(wait_ms/1000.0)
    else:
        if direction == "up":
            for i in strip_range:
                strip.setPixelColor(i, color)
                strip.show()
                time.sleep(wait_ms/1000.0)
        else:
            for i in reversed(strip_range):
                strip.setPixelColor(i, color)
                strip.show()
                time.sleep(wait_ms/1000.0)

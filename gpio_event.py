#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
********************************************************************************
* FILENAME:    gpio_event.py
*
* AUTHORS:
*       Bernhard Reiter
*
* DATE:
*       Mon Sep 28 20:39:02 2020
*
* DESCRIPTION:
*       Initialize a GPIO as a button.
*       Events:
*        - HIGH
*        - LOW
*        - SHORT PRESS
*        - LONG PRESS
*
********************************************************************************
"""


import pigpio


class GPIO:
    """Enable GPIO's."""

    def __init__(self, pgpio_instance, gpio_number, time_long_press=1500, *args, **kwargs):
        self.pi = pgpio_instance
        self.pin = gpio_number
        self.pullup = pigpio.PUD_UP

        self.time_long_press = time_long_press * 1000  # 1500 ms
        self.gpio_state = "LOW"
        self.gpio_calltime = 0

        self.pi.set_mode(self.pin, pigpio.INPUT)
        self.pi.set_pull_up_down(self.pin, self.pullup)
        self.pi.callback(self.pin, pigpio.EITHER_EDGE, self.gpio_event)
        self.pi.set_watchdog(self.pin, self.time_long_press/1000*4)

    # Mode-button callback: Start data aquisition
    def gpio_event(self, gpio, level, tick):
        if gpio == self.pin:
            # Falling Edge
            if level == 0:
                self.gpio_calltime = tick
                self.gpio_state = "HIGH"
            # Rising Edge
            elif level == 1:
                if self.gpio_calltime and (tick - self.gpio_calltime) > self.time_long_press:
                    self.gpio_state = "LONG"
                elif self.gpio_calltime:
                    self.gpio_state = "SHORT"
                else:
                    self.gpio_state = "LOW"
                self.gpio_calltime = 0
            else:
                self.gpio_state = "LOW"
                self.gpio_calltime = 0

    def state(self):
        if self.gpio_state == "SHORT":
            self.gpio_state = "LOW"
            return "SHORT"
        if self.gpio_state == "LONG":
            self.gpio_state = "LOW"
            return "LONG"
        return self.gpio_state

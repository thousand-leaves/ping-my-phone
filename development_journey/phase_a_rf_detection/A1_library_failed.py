#!/usr/bin/env python3
"""
A1: Failed Library Approach
======================================================================

This was my first attempt at RF signal detection using the rpi_rf library.
I thought using a high-level library would be the easiest approach.

PROBLEMS ENCOUNTERED:
1. **Installation Issues**: The rpi_rf library wasn't available by default
2. **Runtime Errors**: "RuntimeError: Failed to add edge detection" 
3. **Protocol Limitations**: Designed for specific RF protocols, not generic 433MHz
4. **Lack of Control**: Couldn't see raw signal data or understand what was happening

WHY THIS APPROACH FAILED:
- The library's edge detection failed on my hardware setup
- I couldn't debug issues because the library hid the low-level details

DECISION MADE:
- Abandoned the rpi_rf library approach
- Decided to go lower-level with direct GPIO control
- This led to A2_gpio_pulse_count.py (simple pulse counting approach)
"""

import time
import os
from rpi_rf import RFDevice
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# GPIO pin from environment variable (configured in .env file)
# Try different pins to see if edge detection works
GPIO_PIN = int(os.getenv('GPIO_DATA_PIN', '5'))

# Clean up any existing GPIO state first
import RPi.GPIO as GPIO
GPIO.cleanup()

# The rpi_rf library provides a high-level interface
# It handles protocol detection and code extraction automatically
rfdevice = RFDevice(GPIO_PIN)
rfdevice.enable_rx()

print(f"Listening for RF codes on GPIO {GPIO_PIN}...")
print("Press Ctrl+C to exit.")

try:
    while True:
        # The library checks if a new code was received
        # rx_code_timestamp gets updated when a new signal is detected
        if rfdevice.rx_code_timestamp != 0:
            print(f"Received RF code: {rfdevice.rx_code} "
                  f"(pulse length: {rfdevice.rx_pulselength} µs, "
                  f"protocol: {rfdevice.rx_proto})")
            # Small delay to avoid duplicate prints
            # The library might trigger multiple times for the same signal
            time.sleep(0.2)
except KeyboardInterrupt:
    print("\nExiting...")
finally:
    # Always cleanup GPIO resources when exiting
    rfdevice.cleanup()

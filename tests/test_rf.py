#!/usr/bin/env python3
"""
RF Test
==============

Basic test to see if we can detect any RF signals at all.
"""

import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN)

print("RF Detection Test")
print("Press your button and watch for state changes...")
print("Press Ctrl+C to exit.")
print()

# Track state changes
last_state = GPIO.input(5)
state_changes = 0
start_time = time.time()

try:
    while True:
        current_state = GPIO.input(5)
        
        # Detect state changes
        if current_state != last_state:
            state_changes += 1
            timestamp = time.time() - start_time
            print(f"State change #{state_changes}: {last_state} -> {current_state} at {timestamp:.2f}s")
            last_state = current_state
        
        time.sleep(0.001)  # 1ms polling

except KeyboardInterrupt:
    print(f"\nTest complete. Total state changes detected: {state_changes}")
    GPIO.cleanup()

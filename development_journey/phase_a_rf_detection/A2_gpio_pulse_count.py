#!/usr/bin/env python3
"""
A2: GPIO Pulse Counting System
==============================================

A basic RF signal detection system that polls GPIO pins to capture digital pulses
from an RF receiver module. This approach counts HIGH pulses to identify different
RF button codes, though it's limited in accuracy due to simple polling method.
"""

import RPi.GPIO as GPIO
import time
import os
from collections import Counter
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables (configured in .env file)
GPIO_DATA_PIN = os.getenv('GPIO_DATA_PIN')
MIN_PULSES_STR = os.getenv('MIN_PULSES')
GAP_THRESHOLD_STR = os.getenv('GAP_THRESHOLD')

if not GPIO_DATA_PIN:
    raise ValueError("GPIO_DATA_PIN must be set in .env file")
if not MIN_PULSES_STR:
    raise ValueError("MIN_PULSES must be set in .env file")
if not GAP_THRESHOLD_STR:
    raise ValueError("GAP_THRESHOLD must be set in .env file")

DATA_PIN = int(GPIO_DATA_PIN)
MIN_PULSES = int(MIN_PULSES_STR)  # ignore very short noise
GAP_THRESHOLD = float(GAP_THRESHOLD_STR)  # 10 ms gap between packets

# Direct GPIO setup
GPIO.setmode(GPIO.BCM)  # Use Broadcom chip pin numbering (GPIO channel numbers)
GPIO.setup(DATA_PIN, GPIO.IN)  # Configure pin as input to read RF receiver signals

print("Listening for RF codes (polling + counting)...")
print("Press Ctrl+C to exit.")

# Track the previous state to detect transitions
last_state = GPIO.input(DATA_PIN) # Get the initial state of the pin (HIGH or LOW)
last_time = time.time()
pulse_times = []
codes_counter = Counter()

def decode_pulses(pulses):
    # Each button produces a consistent number of HIGH pulses
    # Count HIGH pulses as "code"
    high_count = len([p for p in pulses if p[0] == 1])
    return high_count

try:
    while True:
        # Direct GPIO polling
        state = GPIO.input(DATA_PIN)
        print(f"State: {state}")
        now = time.time()
        
        # Detect state changes to capture pulse timing
        if state != last_state:
            duration = now - last_time
            pulse_times.append((last_state, duration))
            last_state = state
            last_time = now

        # Detect end of packet using gap threshold
        if pulse_times and (now - last_time) > GAP_THRESHOLD:
            if len(pulse_times) >= MIN_PULSES:
                code = decode_pulses(pulse_times)
                codes_counter[code] += 1
                print(f"RF Code: {code} | seen {codes_counter[code]} times | pulses: {len(pulse_times)}")
            pulse_times = []

        # Fast polling for responsive detection
        time.sleep(0.0001)  # poll fast

except KeyboardInterrupt:
    # Graceful shutdown: show summary and cleanup GPIO resources
    print("\n--- Summary of codes ---")
    for code, count in codes_counter.most_common():
        print(f"Code: {code} | seen {count} times")
    # Always cleanup GPIO resources
    GPIO.cleanup()

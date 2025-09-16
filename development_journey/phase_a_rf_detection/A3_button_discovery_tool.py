#!/usr/bin/env python3
"""
Button Discovery & Configuration Tool
====================================

A dedicated tool to discover and configure your specific RF button code.
Run this once to find your button, then it updates your main app configuration.

Usage:
1. Run this tool
2. Press your RF button several times
3. Tool identifies your button code and updates configuration
4. Main app will then monitor only your button
"""

import RPi.GPIO as GPIO
import time
import json
import os
from collections import Counter
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables (configured in .env file)
DATA_PIN = int(os.getenv('GPIO_DATA_PIN', '5'))
MIN_PULSES = int(os.getenv('MIN_PULSES', '10'))
GAP_THRESHOLD = float(os.getenv('GAP_THRESHOLD', '0.01'))

# Direct GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.IN)

print("=== Button Discovery Tool ===")
print("Press your RF button several times...")
print("Tool will identify your button code and update configuration.")
print("Press Ctrl+C when done.")

# State tracking for pulse detection
last_state = GPIO.input(DATA_PIN)
last_time = time.time()
pulse_times = []
codes_counter = Counter()  # Track frequency to identify your button

def decode_pulses(pulses):
    """Count HIGH pulses to generate button code"""
    high_count = len([p for p in pulses if p[0] == 1])
    return high_count

try:
    while True:
        state = GPIO.input(DATA_PIN)
        now = time.time()
        if state != last_state:
            duration = now - last_time
            pulse_times.append((last_state, duration))
            last_state = state
            last_time = now

        # Detect end of packet and count button presses
        if pulse_times and (now - last_time) > GAP_THRESHOLD:
            if len(pulse_times) >= MIN_PULSES:
                code = decode_pulses(pulse_times)
                codes_counter[code] += 1
                print(f"Detected code: {code} (seen {codes_counter[code]} times)")
            pulse_times = []

        time.sleep(0.0001)

except KeyboardInterrupt:
    print("\n=== Discovery Results ===")
    
    if not codes_counter:
        print("No button codes detected. Make sure your RF button is working.")
    else:
        # Find the most frequently detected code (likely your button)
        most_common = codes_counter.most_common(1)[0]
        button_code = most_common[0]
        count = most_common[1]
        
        print(f"Most frequent code: {button_code} (detected {count} times)")
        print(f"This is likely your button code!")
        
        # Update configuration file for main app
        config = {"BUTTON_CODE": button_code}
        with open("button_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print(f"Configuration saved to button_config.json")
        print(f"Your main app will now monitor for code: {button_code}")
    
    # Always cleanup GPIO resources
    GPIO.cleanup()

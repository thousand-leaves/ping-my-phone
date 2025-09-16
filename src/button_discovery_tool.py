#!/usr/bin/env python3
"""
Button Discovery & Configuration Tool
====================================

A tool to discover and configure your specific RF button code.
Run this once to find your button, then it updates your main app configuration.

What are button codes?
- Button codes are the actual digital signal patterns your RF button transmits
- Each button sends a unique number of HIGH pulses (e.g., 25 pulses = code 25)
- Different RF devices send different pulse counts (neighbor's garage door might be code 7)
- Your button's code is its unique "fingerprint" in the RF spectrum

Usage:
1. Run this tool
2. Press your RF button several times
3. Tool identifies your button code and updates configuration
4. Main app will then monitor only your button
"""

# Standard library imports
import time
import json
import os
from collections import Counter

# Third-party imports for Raspberry Pi GPIO and environment variables
import RPi.GPIO as GPIO  # Controls GPIO pins on Raspberry Pi
from dotenv import load_dotenv  # Loads configuration from .env file

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables (configured in .env file)
# These values control how sensitive our RF detection is
DATA_PIN = int(os.getenv('GPIO_DATA_PIN', '5'))  # Which GPIO pin the RF receiver is connected to
MIN_PULSES = int(os.getenv('MIN_PULSES', '10'))  # Minimum pulses to consider a valid signal (filters noise)
GAP_THRESHOLD = float(os.getenv('GAP_THRESHOLD', '0.01'))  # Time gap (10ms) that indicates end of transmission

# GPIO Setup - Configure the Raspberry Pi to read digital signals
GPIO.setmode(GPIO.BCM)  # Use Broadcom chip pin numbering (GPIO channel numbers)
GPIO.setup(DATA_PIN, GPIO.IN)  # Configure pin as INPUT to read RF receiver signals

print("=== Button Discovery Tool ===")
print("Press your RF button several times...")
print("Tool will identify your button code and update configuration.")
print("Press Ctrl+C when done.")

# State tracking variables for pulse detection
last_state = GPIO.input(DATA_PIN)  # Previous HIGH/LOW state to detect changes
last_time = time.time()  # Timestamp of last state change
pulse_times = []  # List to store (state, duration) pairs for current transmission
codes_counter = Counter()  # Counts how many times each code appears (helps identify YOUR button)

def decode_pulses(pulses):
    """
    Convert pulse pattern into a button code.
    
    Args:
        pulses: List of (state, duration) tuples from GPIO readings
        
    Returns:
        int: Button code (number of HIGH pulses)
        
    Example:
        If pulses = [(1, 0.001), (0, 0.002), (1, 0.001), ...]
        This counts the HIGH pulses (state=1) to generate the code
    """
    # Count only HIGH pulses (state=1) - these represent the actual signal
    high_count = len([p for p in pulses if p[0] == 1])
    return high_count

try:
    # Main detection loop - continuously poll GPIO pin for signal changes
    while True:
        # Read current state of GPIO pin (HIGH=1 or LOW=0)
        state = GPIO.input(DATA_PIN)
        now = time.time()
        
        # Detect state changes (HIGH->LOW or LOW->HIGH) to capture pulse timing
        if state != last_state:
            # Calculate how long the previous state lasted
            duration = now - last_time
            # Store the state and its duration
            pulse_times.append((last_state, duration))
            # Update tracking variables for next iteration
            last_state = state
            last_time = now

        # Detect end of transmission using gap threshold
        # If no state change for GAP_THRESHOLD seconds, transmission is complete
        if pulse_times and (now - last_time) > GAP_THRESHOLD:
            # Only process if we have enough pulses (filters out noise)
            if len(pulse_times) >= MIN_PULSES:
                # Convert pulse pattern to button code
                code = decode_pulses(pulse_times)
                # Count this code (helps identify which is YOUR button)
                codes_counter[code] += 1
                print(f"Detected code: {code} (seen {codes_counter[code]} times)")
            # Reset for next transmission
            pulse_times = []

        # Fast polling for responsive detection (0.1ms delay)
        time.sleep(0.0001)

except KeyboardInterrupt:
    # Graceful shutdown when user presses Ctrl+C
    print("\n=== Discovery Results ===")
    
    if not codes_counter:
        print("No button codes detected. Make sure your RF button is working.")
    else:
        # Find the most frequently detected code (likely your button)
        # The assumption: you pressed YOUR button more than other devices
        most_common = codes_counter.most_common(1)[0]  # Get (code, count) tuple
        button_code = most_common[0]  # The code number
        count = most_common[1]  # How many times it was detected
        
        print(f"Most frequent code: {button_code} (detected {count} times)")
        print(f"This is likely your button code!")
        
        # Save configuration for main application
        config = {"BUTTON_CODE": button_code}
        with open("button_config.json", "w") as f:
            json.dump(config, f, indent=2)  # Pretty-print JSON
        
        print(f"Configuration saved to button_config.json")
        print(f"Your main app will now monitor for code: {button_code}")
    
    # CRITICAL: Always cleanup GPIO resources to prevent hardware conflicts
    GPIO.cleanup()

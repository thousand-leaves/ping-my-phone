#!/usr/bin/env python3
"""
Button Discovery & Configuration Tool
====================================

A tool to discover and configure your specific RF button code.
Run this once to find your button, then it updates your main app configuration.

What are button codes?
- Button codes are the actual RF signal codes transmitted by your RF button
- Each button sends a unique RF code (e.g., 6965825)
- Different RF devices send different codes (neighbor's garage door might be a different code)
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
import signal
import sys
from collections import Counter
from rpi_rf import RFDevice

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)

# GPIO pin configuration (default to GPIO 27 as used in rf-receiver)
GPIO_PIN = int(os.getenv('GPIO_DATA_PIN', '27'))

print("=== Button Discovery Tool ===")
print("Press your RF button several times...")
print("Tool will identify your button code and update configuration.")
print("Press Ctrl+C when done.\n")

# Initialize RF device
rfdevice = None

def cleanup():
    """Clean up GPIO resources - releases GPIO pins so they can be used again"""
    global rfdevice
    if rfdevice:
        rfdevice.cleanup()
    print("Discovery stopped.")

def signal_handler(signum, frame):
    """Handle SIGTERM signal - ensures cleanup runs before exit"""
    cleanup()
    sys.exit(0)

# Register signal handler so cleanup runs if process is stopped externally
signal.signal(signal.SIGTERM, signal_handler)

try:
    # Initialize RF device
    rfdevice = RFDevice(GPIO_PIN)
    rfdevice.enable_rx()
    print("RF device ready! Listening for signals...\n")
    
    codes_counter = Counter()  # Counts how many times each code appears
    timestamp = None
    
    # Main detection loop
    while True:
        # Check if a new RF code was received
        if rfdevice.rx_code_timestamp != timestamp:
            timestamp = rfdevice.rx_code_timestamp
            code = rfdevice.rx_code
            protocol = rfdevice.rx_proto
            pulselength = rfdevice.rx_pulselength
            
            # Count this code (helps identify which is YOUR button)
            codes_counter[code] += 1
            print(f"Detected code: {code} [protocol: {protocol}, pulselength: {pulselength}] (seen {codes_counter[code]} times)")
        
        time.sleep(0.01)

except KeyboardInterrupt:
    # Ctrl+C pressed - show results and cleanup GPIO
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
        
        # Save configuration for main application
        config = {"BUTTON_CODE": button_code}
        with open("button_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print(f"Configuration saved to button_config.json")
        print(f"Your main app will now monitor for code: {button_code}")
    
    cleanup()

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()  # Print full traceback for debugging
    if "GPIO busy" in str(e):
        print("\n💡 Tip: GPIO is busy. Run: sudo python3 cleanup-gpio.py")
    cleanup()
    sys.exit(1)

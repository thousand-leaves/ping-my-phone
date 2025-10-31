#!/usr/bin/env python3
"""
Doorbell System
===============

Simple doorbell system that monitors for your configured RF button
and sends Telegram notifications when pressed.

Usage:
1. Run button discovery tool first: python3 src/button_discovery_tool.py
2. Set Telegram credentials in .env file
3. Run this: python3 src/doorbell.py
"""

# Standard library imports
import time
import os
import signal
import sys

# Third-party imports for RF signal detection
import RPi.GPIO as GPIO
from rpi_rf import RFDevice

# Local imports
from config import DoorbellConfig
from telegram_notifier import TelegramNotifier

# Load all configuration from .env file and button_config.json
config = DoorbellConfig()

print(f"🔔 Doorbell System - Monitoring button code {config.button_code}")
print("Press Ctrl+C to exit.")

# Initialize Telegram notifier
notifier = TelegramNotifier(config.bot_token, config.chat_id)

# Initialize RF device
rfdevice = None

def cleanup():
    """Clean up GPIO resources - releases GPIO pins so they can be used again"""
    global rfdevice
    if rfdevice:
        rfdevice.cleanup()
    print("Doorbell stopped.")

def signal_handler(signum, frame):
    """Handle SIGTERM (sent by systemd) - ensures cleanup runs before exit"""
    cleanup()
    sys.exit(0)

# Register signal handler so cleanup runs when systemd stops the service
signal.signal(signal.SIGTERM, signal_handler)

try:
    # Initialize RF device
    # RFDevice handles GPIO setup internally
    rfdevice = RFDevice(config.gpio_pin)
    rfdevice.enable_rx()
    
    # Debouncing variables to prevent multiple notifications
    last_notification_time = 0
    DEBOUNCE_TIME = 2.0  # Minimum seconds between notifications
    
    timestamp = None
    
    # Main detection loop
    while True:
        # Check if a new RF code was received
        if rfdevice.rx_code_timestamp != timestamp:
            timestamp = rfdevice.rx_code_timestamp
            code = rfdevice.rx_code
            
            # Only send notification for our configured button code
            if code == config.button_code:
                # Check if enough time has passed since last notification (debouncing)
                now = time.time()
                if (now - last_notification_time) >= DEBOUNCE_TIME:
                    notifier.notify_doorbell()
                    last_notification_time = now
        
        time.sleep(0.01)

except KeyboardInterrupt:
    # Ctrl+C pressed - cleanup GPIO before exiting
    cleanup()
except Exception as e:
    # Error occurred - cleanup GPIO to prevent pins from getting stuck
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()  # Print full traceback for debugging
    if "GPIO busy" in str(e) or "edge detection" in str(e):
        print("💡 Tip: GPIO is still busy or edge detection failed. Try running: sudo python3 cleanup-gpio.py")
    cleanup()
    sys.exit(1)

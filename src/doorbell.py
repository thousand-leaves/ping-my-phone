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
import signal
import sys

# Local imports
from config import DoorbellConfig
from telegram_notifier import TelegramNotifier
from rf_monitor import RFMonitor

# Load all configuration from .env file and button_config.json
config = DoorbellConfig()

print(f"🔔 Doorbell System - Monitoring button code {config.button_code}")
print("Press Ctrl+C to exit.")

# Initialize Telegram notifier
notifier = TelegramNotifier(config.bot_token, config.chat_id)

# Initialize RF monitor
rfmonitor = RFMonitor(config.gpio_pin)

def signal_handler(signum, frame):
    """Handle SIGTERM (sent by systemd) - ensures cleanup runs before exit"""
    rfmonitor.cleanup()
    print("Doorbell stopped.")
    sys.exit(0)

# Register signal handler so cleanup runs when systemd stops the service
signal.signal(signal.SIGTERM, signal_handler)

try:
    # Start RF monitoring
    rfmonitor.start()
    
    # Debouncing variables to prevent multiple notifications
    last_notification_time = 0
    DEBOUNCE_TIME = 2.0  # Minimum seconds between notifications
    
    # Main detection loop
    while True:
        # Check for newly detected RF code
        code = rfmonitor.check_for_code()
        
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
    rfmonitor.cleanup()
    print("Doorbell stopped.")
except Exception as e:
    # Error occurred - cleanup GPIO to prevent pins from getting stuck
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()  # Print full traceback for debugging
    if "GPIO busy" in str(e) or "edge detection" in str(e):
        print("💡 Tip: GPIO is still busy or edge detection failed. Try running: sudo python3 cleanup-gpio.py")
    rfmonitor.cleanup()
    sys.exit(1)

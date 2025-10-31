#!/usr/bin/env python3
"""
Doorbell System
===============

Simple doorbell system that monitors for your configured RF button
and sends Telegram notifications when pressed.

Usage:
1. Run button discovery tool first: python3 src/button_discovery_tool.py
2. Set Telegram credentials in .env file
3. Run this: python3 src/main.py
"""

# Standard library imports
import signal
import sys

# Local imports
from config import DoorbellConfig
from telegram_notifier import TelegramNotifier
from rf_monitor import RFMonitor
from doorbell_service import DoorbellService

# Load all configuration from .env file and button_config.json
config = DoorbellConfig()

print(f"🔔 Doorbell System - Monitoring button code {config.button_code}")
print("Press Ctrl+C to exit.")

# Initialize components
notifier = TelegramNotifier(config.bot_token, config.chat_id)
rf_monitor = RFMonitor(config.gpio_pin)

# Create doorbell service
service = DoorbellService(config, notifier, rf_monitor)

def signal_handler(signum, frame):
    """Handle SIGTERM (sent by systemd) - ensures cleanup runs before exit"""
    service.stop()
    print("Doorbell stopped.")
    sys.exit(0)

# Register signal handler so cleanup runs when systemd stops the service
signal.signal(signal.SIGTERM, signal_handler)

try:
    # Start the service (initializes RF monitor)
    service.start()
    
    # Run the main monitoring loop
    service.run()

except KeyboardInterrupt:
    # Ctrl+C pressed - cleanup GPIO before exiting
    service.stop()
    print("Doorbell stopped.")
except Exception as e:
    # Error occurred - cleanup GPIO to prevent pins from getting stuck
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()  # Print full traceback for debugging
    if "GPIO busy" in str(e) or "edge detection" in str(e):
        print("💡 Tip: GPIO is still busy or edge detection failed. Try running: sudo python3 cleanup-gpio.py")
    service.stop()
    sys.exit(1)


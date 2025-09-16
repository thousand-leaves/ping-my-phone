#!/usr/bin/env python3
"""
B1: First Telegram Integration - Basic Notification System
========================================================

This was my first attempt at integrating Telegram notifications.
I combined the successful RF detection with Telegram messaging.

PROBLEM ENCOUNTERED:
- Sends notifications for ALL detected signals
- This resulted in hundreds of notifications (spam!)
- No filtering meant every RF device in range triggered alerts
- Made the system unusable for daily use

DECISION MADE:
- Realized I needed filtering to avoid spam
- Decided to only send notifications for specific, important codes
- This led to B2_rf_receiver_telegram_filtered.py
"""

import RPi.GPIO as GPIO
import time
import os
from collections import Counter
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ---------------------------
# CONFIG
# ---------------------------
# Configuration from environment variables (configured in .env file)
# No fallback values - these must be configured in .env for security
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
MIN_PULSES = int(MIN_PULSES_STR)     # Ignore very short noise
GAP_THRESHOLD = float(GAP_THRESHOLD_STR)  # 10 ms gap between packets

# Telegram Bot API configuration from environment variables
# BOT_TOKEN: Get this from @BotFather on Telegram
# CHAT_ID: Your personal chat ID for receiving messages
# These are sensitive and MUST be configured in .env file
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN must be set in .env file")
if not CHAT_ID:
    raise ValueError("CHAT_ID must be set in .env file")

# ---------------------------
# SETUP
# ---------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setup(DATA_PIN, GPIO.IN)

print("Listening for RF codes (polling + counting + Telegram)...")
print("Press Ctrl+C to exit.")

last_state = GPIO.input(DATA_PIN)
last_time = time.time()
pulse_times = []
codes_counter = Counter()

# ---------------------------
# FUNCTIONS
# ---------------------------
def decode_pulses(pulses):
    """Very simple decoding: count HIGH pulses as “code”"""
    high_count = len([p for p in pulses if p[0] == 1])
    return high_count

def send_telegram_message(text):
    """
    Telegram Bot API integration.
    Uses HTTP POST to send messages via the Telegram API.
    
    PROBLEM: This sends ALL signals, causing notification spam!
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=payload)
        print(f"Telegram sent: {text}")
    except Exception as e:
        print("Failed to send Telegram message:", e)

# ---------------------------
# MAIN LOOP
# ---------------------------
try:
    while True:
        state = GPIO.input(DATA_PIN)
        now = time.time()

        if state != last_state:
            duration = now - last_time
            pulse_times.append((last_state, duration))
            last_state = state
            last_time = now

        # Check for end of packet
        if pulse_times and (now - last_time) > GAP_THRESHOLD:
            if len(pulse_times) >= MIN_PULSES:
                code = decode_pulses(pulse_times)
                codes_counter[code] += 1
                msg = f"RF Code: {code} | seen {codes_counter[code]} times | pulses: {len(pulse_times)}"
                print(msg)
                # PROBLEM - This sends ALL signals!
                # This caused notification spam and made the system unusable
                send_telegram_message(msg)
            pulse_times = []

        time.sleep(0.0001)  # poll fast

except KeyboardInterrupt:
    print("\n--- Summary of codes ---")
    for code, count in codes_counter.most_common():
        print(f"Code: {code} | seen {count} times")
    GPIO.cleanup()

#!/usr/bin/env python3
"""
Test Telegram Integration
========================

Simple test to verify Telegram notifications are working.
This simulates a button press without needing the actual RF hardware.
"""

import requests
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Telegram credentials
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def send_test_notification():
    """Send a test doorbell notification"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    message = f"🔔 TEST DOORBELL NOTIFICATION 🔔\nTime: {timestamp}\nButton Code: 25 (SIMULATED)"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    
    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ Test notification sent successfully at {timestamp}")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Telegram failed: {response.status_code} {response.text}")
    except Exception as e:
        print(f"❌ Failed to send test notification: {e}")

if __name__ == "__main__":
    print("Testing Telegram integration...")
    print(f"Bot Token: {BOT_TOKEN[:10]}..." if BOT_TOKEN else "❌ No bot token")
    print(f"Chat ID: {CHAT_ID}")
    print()
    
    send_test_notification()
